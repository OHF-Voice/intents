"""Generate a per-language slot combination coverage summary for the website."""

from __future__ import annotations

import json

import yaml

from .const import INTENTS_FILE, LANGUAGES, LANGUAGES_FILE, SENTENCE_DIR
from .example_highlight import combo_slot_lists, get_language_intents, highlight_example

# Ordered grouping of intents for the per-language breakdown. Each group has a
# display name, a URL-friendly slug (used for the table-of-contents anchors),
# and the intents that belong to it. Intents not listed here fall into "Other".
INTENT_GROUPS: list[tuple[str, str, list[str]]] = [
    (
        "Lights, Switches & Devices",
        "devices",
        [
            "HassTurnOn",
            "HassTurnOff",
            "HassLightSet",
            "HassFanSetSpeed",
            "HassSetPosition",
        ],
    ),
    (
        "Climate & Weather",
        "climate",
        [
            "HassClimateGetTemperature",
            "HassClimateSetTemperature",
            "HassGetWeather",
        ],
    ),
    (
        "Media & Volume",
        "media",
        [
            "HassMediaSearchAndPlay",
            "HassMediaPause",
            "HassMediaUnpause",
            "HassMediaNext",
            "HassMediaPrevious",
            "HassSetVolume",
            "HassSetVolumeRelative",
            "HassMediaPlayerMute",
            "HassMediaPlayerUnmute",
        ],
    ),
    (
        "Timers",
        "timers",
        [
            "HassStartTimer",
            "HassPauseTimer",
            "HassUnpauseTimer",
            "HassIncreaseTimer",
            "HassDecreaseTimer",
            "HassCancelTimer",
            "HassCancelAllTimers",
            "HassTimerStatus",
        ],
    ),
    (
        "Lists & To-do",
        "lists",
        [
            "HassListAddItem",
            "HassListCompleteItem",
            "HassListRemoveItem",
            "HassShoppingListAddItem",
            "HassShoppingListCompleteItem",
        ],
    ),
    (
        "Vacuum & Lawn Mower",
        "cleaning",
        [
            "HassVacuumStart",
            "HassVacuumCleanArea",
            "HassVacuumReturnToBase",
            "HassLawnMowerStartMowing",
            "HassLawnMowerDock",
        ],
    ),
    (
        "Date & Time",
        "datetime",
        [
            "HassGetCurrentTime",
            "HassGetCurrentDate",
        ],
    ),
    (
        "State & Information",
        "state",
        [
            "HassGetState",
        ],
    ),
    (
        "Miscellaneous",
        "assist",
        [
            "HassBroadcast",
            "HassRespond",
            "HassNevermind",
        ],
    ),
]

# Fallback group for any intent not explicitly placed above.
_OTHER_GROUP = ("Other", "other")


def _group_for_intent(intent_name: str) -> tuple[str, str]:
    """Return the (name, slug) of the group an intent belongs to."""
    for name, slug, members in INTENT_GROUPS:
        if intent_name in members:
            return name, slug
    return _OTHER_GROUP


def _intent_sort_key(intent_name: str) -> tuple[int, int, str]:
    """Sort intents by group order, then by the within-group order declared in
    INTENT_GROUPS (roughly how likely/early each intent is encountered).
    Ungrouped intents fall after all groups, ordered alphabetically."""
    for group_index, (_name, _slug, members) in enumerate(INTENT_GROUPS):
        if intent_name in members:
            return (group_index, members.index(intent_name), intent_name)
    return (len(INTENT_GROUPS), 0, intent_name)


def _first_example(example) -> str | None:
    """Normalize an intents.yaml example (str or list) to a single string."""
    if isinstance(example, list):
        return example[0] if example else None
    return example


def _is_required(combo_info: dict) -> bool:
    """A slot combination is required if its importance is required, or any of
    its name/inferred domains are required (matches validation rules)."""
    if combo_info.get("importance") == "required":
        return True
    name_domains = combo_info.get("name_domains") or {}
    inferred_domains = combo_info.get("inferred_domains") or {}
    return ("required" in name_domains) or ("required" in inferred_domains)


def run() -> int:
    intent_info = yaml.safe_load(INTENTS_FILE.read_text())
    language_info = yaml.safe_load(LANGUAGES_FILE.read_text())

    # Slot combinations declared in intents.yaml, per intent (sorted for stable output).
    intents_out = []
    for intent_name, info in sorted(intent_info.items()):
        slot_combinations = info.get("slot_combinations") or {}
        if not slot_combinations:
            continue

        combos = [
            {
                "name": combo_name,
                "slots": combo_info.get("slots", []),
                "example": _first_example(combo_info.get("example")),
                "required": _is_required(combo_info),
            }
            for combo_name, combo_info in slot_combinations.items()
        ]

        # support[language][combo_name] = {"supported": bool, "examples": [str, ...]}
        support: dict[str, dict[str, dict]] = {}
        for language in LANGUAGES:
            lang_support: dict[str, dict] = {}
            for combo in combos:
                combo_path = (
                    SENTENCE_DIR / language / intent_name / f"{combo['name']}.yaml"
                )
                entry = {"supported": False, "examples": []}
                if combo_path.exists():
                    combo_data = yaml.safe_load(combo_path.read_text()) or {}
                    data_blocks = combo_data.get("data") or []
                    if data_blocks:
                        entry["supported"] = True
                        raw_examples = [
                            block["example"]
                            for block in data_blocks
                            if block.get("example")
                        ]
                        if raw_examples:
                            # Highlight slot values (name/area/floor/numbers/...)
                            # by parsing each example with hassil.
                            lang_intents = get_language_intents(language, intent_info)
                            slot_lists = combo_slot_lists(
                                language, intent_name, combo["name"]
                            )
                            entry["examples"] = [
                                highlight_example(example, lang_intents, slot_lists)
                                for example in raw_examples
                            ]
                lang_support[combo["name"]] = entry
            support[language] = lang_support

        group_name, group_slug = _group_for_intent(intent_name)
        intents_out.append(
            {
                "intent": intent_name,
                "domain": info.get("domain"),
                "group": group_name,
                "group_slug": group_slug,
                "combos": combos,
                "support": support,
            }
        )

    # Order intents by group, then by likely encounter order within the group,
    # so the per-language sections read top-down rather than alphabetically.
    intents_out.sort(key=lambda intent: _intent_sort_key(intent["intent"]))

    # Ordered list of groups present in the output, used to render the
    # per-language table of contents and grouped sections.
    present_intents = {intent["intent"] for intent in intents_out}
    groups_out = []
    for name, slug, members in INTENT_GROUPS:
        group_members = [m for m in members if m in present_intents]
        if group_members:
            groups_out.append({"name": name, "slug": slug, "intents": group_members})
    other_members = [
        intent["intent"] for intent in intents_out if intent["group"] == _OTHER_GROUP[0]
    ]
    if other_members:
        groups_out.append(
            {
                "name": _OTHER_GROUP[0],
                "slug": _OTHER_GROUP[1],
                "intents": other_members,
            }
        )

    # Totals across every intent.
    total_required = sum(
        1 for intent in intents_out for combo in intent["combos"] if combo["required"]
    )
    total_combos = sum(len(intent["combos"]) for intent in intents_out)

    # Per-language coverage scores.
    languages_out = []
    for language in LANGUAGES:
        covered_required = 0
        covered_total = 0
        for intent in intents_out:
            lang_support = intent["support"][language]
            for combo in intent["combos"]:
                if lang_support[combo["name"]]["supported"]:
                    covered_total += 1
                    if combo["required"]:
                        covered_required += 1

        score = round(100 * covered_required / total_required) if total_required else 0
        score_total = round(100 * covered_total / total_combos) if total_combos else 0
        languages_out.append(
            {
                "code": language,
                "native_name": language_info.get(language, {}).get(
                    "nativeName", language
                ),
                "leaders": language_info.get(language, {}).get("leaders"),
                "covered_required": covered_required,
                "total_required": total_required,
                "covered_total": covered_total,
                "total_combos": total_combos,
                "score": score,
                "score_total": score_total,
            }
        )

    # Leaderboard order: most required coverage first, then most total coverage,
    # then alphabetical.
    languages_out.sort(
        key=lambda lang: (-lang["score"], -lang["score_total"], lang["code"])
    )

    print(
        json.dumps(
            {
                "languages": languages_out,
                "groups": groups_out,
                "intents": intents_out,
            },
            indent=2,
            ensure_ascii=False,
        )
    )

    return 0
