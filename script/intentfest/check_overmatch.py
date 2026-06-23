"""Check for cross-intent over-matching.

The per-test slot-combination suite (tests/test_slot_combinations.py) compiles
each language's intents into one `Intents` object but only asserts that a test
sentence matches its *own* intent. It can never observe one intent stealing
another intent's utterance, because every assertion is scoped to the directory
the test lives under.

This subcommand closes that gap. It compiles ALL of a language's migrated
intents into a single `Intents` object (exactly like the suite's
`lang_resources_fixture`), then for every test sentence in
`tests/<lang>/<Intent>/<combo>.yaml` runs `recognize_best` against the merged
set. If the winning intent is not the intent the test lives under, that is a
cross-intent false positive (e.g. the es bug where
"pon la luz al máximo" (HassLightSet) was stolen by HassMediaSearchAndPlay's
greedy `{search_query}` wildcard).

Exit code is 1 if any cross-intent mismatch is found, else 0, so it can be
wired into CI as a gate.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from typing import Any, Optional

import yaml
from hassil import Intents, SlotList, TextSlotList, recognize_best

from .const import INTENTS_FILE, LANGUAGES, LIST_DIR, RULE_DIR, SENTENCE_DIR, TESTS_DIR
from .util import get_base_arg_parser

# Sentinel area injected via intent_context, matching the slot-combination
# harness (tests/test_slot_combinations.py:CONTEXT_AREA_NAME).
CONTEXT_AREA_NAME = "__context_area__"


@dataclass
class OvermatchFinding:
    """A cross-intent over-match (or a no-match) for one test sentence."""

    language: str
    expected_intent: str
    expected_combo: str
    sentence: str
    # None kind == cross-intent mismatch; "no_match" == nothing recognized.
    kind: str = "mismatch"
    won_intent: Optional[str] = None
    won_combo: Optional[str] = None
    won_slots: dict[str, Any] = field(default_factory=dict)


def check_sentence(
    intents: Intents,
    slot_lists: dict[str, SlotList],
    language: str,
    expected_intent: str,
    expected_combo: str,
    sentence: str,
) -> Optional[OvermatchFinding]:
    """Recognize one sentence against the merged intents.

    Returns a finding if the winning intent is not the expected intent (a
    cross-intent over-match), or if nothing was recognized at all; otherwise
    returns None.
    """
    result = recognize_best(
        sentence,
        intents,
        slot_lists=slot_lists,
        intent_context={"area": CONTEXT_AREA_NAME},
        best_slot_name="name",
    )

    if result is None:
        return OvermatchFinding(
            language=language,
            expected_intent=expected_intent,
            expected_combo=expected_combo,
            sentence=sentence,
            kind="no_match",
        )

    won_intent = result.intent.name
    if won_intent == expected_intent:
        return None

    won_combo: Optional[str] = None
    if result.intent_metadata is not None:
        won_combo = result.intent_metadata.get("slot_combination")

    return OvermatchFinding(
        language=language,
        expected_intent=expected_intent,
        expected_combo=expected_combo,
        sentence=sentence,
        kind="mismatch",
        won_intent=won_intent,
        won_combo=won_combo,
        won_slots={e_name: e.value for e_name, e in result.entities.items()},
    )


def _slug(name: str) -> str:
    """Synthesize an id from a human name (mirrors the test harness)."""
    return name.strip().casefold().replace(" ", "_")


def get_arguments() -> argparse.Namespace:
    """Get parsed passed in arguments."""
    parser = get_base_arg_parser()
    parser.add_argument(
        "--language", type=str, choices=LANGUAGES, help="The language to check."
    )
    parser.add_argument(
        "--intent",
        help="Only check test sentences belonging to this intent.",
    )
    return parser.parse_args()


def _load_merged_intents(language: str, intent_schemas: dict[str, Any]) -> Intents:
    """Compile ALL of a language's migrated intents into one `Intents`.

    This faithfully mirrors tests/test_slot_combinations.py's
    `lang_resources_fixture` so the merged compiled set is identical to what the
    per-test suite runs against.
    """
    lang_intents_dict: dict[str, Any] = {
        "language": language,
        "intents": {},
        "lists": {},
        "expansion_rules": {},
        "skip_words": [],
    }

    # Load skip words (Home Assistant applies these at runtime, from _common.yaml)
    common_path = SENTENCE_DIR / language / "_common.yaml"
    if common_path.exists():
        with open(common_path, "r", encoding="utf-8") as common_file:
            common_dict = yaml.safe_load(common_file) or {}
        lang_intents_dict["skip_words"] = common_dict.get("skip_words", [])

    # Load expansion rules
    rules_dict: dict[str, Any] = lang_intents_dict["expansion_rules"]
    for rule_path in (RULE_DIR / language).glob("*.yaml"):
        with open(rule_path, "r", encoding="utf-8") as rule_file:
            rule_dict = yaml.safe_load(rule_file)
            rules_dict.update(rule_dict["expansion_rules"])

    # Load shared lists
    lists_dict: dict[str, Any] = lang_intents_dict["lists"]
    for list_path in LIST_DIR.glob("*.yaml"):
        with open(list_path, "r", encoding="utf-8") as list_file:
            list_dict = yaml.safe_load(list_file)
            lists_dict.update(list_dict["lists"])

    # Load language-specific lists
    for list_path in (LIST_DIR / language).glob("*.yaml"):
        with open(list_path, "r", encoding="utf-8") as list_file:
            list_dict = yaml.safe_load(list_file)
            lists_dict.update(list_dict["lists"])

    for intent_name, intent_info in intent_schemas.items():
        intent_dict = lang_intents_dict["intents"].get(intent_name, {"data": []})
        intent_data = intent_dict["data"]

        for combo_name, combo_info in intent_info["slot_combinations"].items():
            sentences_path = (
                SENTENCE_DIR / language / intent_name / f"{combo_name}.yaml"
            )
            if not sentences_path.exists():
                continue

            with open(sentences_path, "r", encoding="utf-8") as sentences_file:
                test_data_dict = yaml.safe_load(sentences_file)

                for test_sentences_dict in test_data_dict["data"]:
                    test_slots = test_sentences_dict.get("slots", {})
                    test_metadata = test_sentences_dict.get("metadata", {})
                    test_requires_context = test_sentences_dict.get(
                        "requires_context", {}
                    )

                    if name_domains := test_sentences_dict.get("name_domains"):
                        test_requires_context["domain"] = name_domains
                    elif inferred_domain := test_sentences_dict.get("inferred_domain"):
                        test_slots["domain"] = inferred_domain

                    # Add context area slot
                    if combo_info.get("context_area"):
                        test_requires_context["area"] = {"slot": True}

                    # Attach metadata so we can identify the slot combination of
                    # whichever intent ends up winning.
                    test_metadata["slot_combination"] = combo_name

                    # Convert to hassil format
                    intent_data.append(
                        {
                            "sentences": test_sentences_dict["sentences"],
                            "slots": test_slots,
                            "metadata": test_metadata,
                            "requires_context": test_requires_context,
                            "response": test_sentences_dict["response"],
                        }
                    )

        lang_intents_dict["intents"][intent_name] = intent_dict

    return Intents.from_dict(lang_intents_dict)


def _build_slot_lists(test_dict: dict[str, Any]) -> dict[str, SlotList]:
    """Build name/area/floor TextSlotLists from a test file, as the harness does."""
    return {
        "name": TextSlotList.from_tuples(
            [
                (
                    e["name"],
                    e["name"],
                    {"domain": e["domain"]},
                    {  # metadata
                        "domain": e["domain"],
                        "state": e.get("state"),
                        "state_with_unit": e.get("state_with_unit"),
                        "entity_id": f"{e['domain']}.{_slug(e['name'])}",
                        "attributes": e.get("attributes", {}),
                        "name": e["name"],
                    },
                )
                for e in test_dict.get("entities", [])
            ],
            name="name",
        ),
        "area": TextSlotList.from_strings(
            [a["name"] for a in test_dict.get("areas", [])], name="area"
        ),
        "floor": TextSlotList.from_strings(
            [f["name"] for f in test_dict.get("floors", [])], name="floor"
        ),
    }


def run() -> int:
    """Run function."""
    args = get_arguments()

    with open(INTENTS_FILE, "r", encoding="utf-8") as intents_file:
        intent_schemas = yaml.safe_load(intents_file)

    if args.language is None:
        languages = LANGUAGES
    else:
        languages = [args.language]

    total_mismatches = 0
    total_no_match = 0
    total_sentences = 0

    for language in languages:
        merged_intents = _load_merged_intents(language, intent_schemas)

        lang_tests_dir = TESTS_DIR / language
        if not lang_tests_dir.is_dir():
            continue

        for intent_name, intent_info in intent_schemas.items():
            if args.intent and (intent_name != args.intent):
                continue

            for combo_name in intent_info["slot_combinations"]:
                test_file_path = (
                    TESTS_DIR / language / intent_name / f"{combo_name}.yaml"
                )
                if not test_file_path.exists():
                    continue

                with open(test_file_path, "r", encoding="utf-8") as test_file:
                    test_dict = yaml.safe_load(test_file)

                slot_lists = _build_slot_lists(test_dict)

                for test_group in test_dict.get("tests", []):
                    for test_sentence in test_group.get("sentences", []):
                        total_sentences += 1
                        finding = check_sentence(
                            merged_intents,
                            slot_lists,
                            language,
                            intent_name,
                            combo_name,
                            test_sentence,
                        )
                        if finding is None:
                            continue

                        if finding.kind == "no_match":
                            total_no_match += 1
                            print(
                                f"[WARN] No match against merged intents: "
                                f"language={finding.language}, "
                                f"expected_intent={finding.expected_intent}, "
                                f"combo={finding.expected_combo}, "
                                f"sentence='{finding.sentence}'"
                            )
                            continue

                        total_mismatches += 1
                        print(
                            f"[WARN] Cross-intent over-match: "
                            f"language={finding.language}, "
                            f"expected_intent={finding.expected_intent}, "
                            f"expected_combo={finding.expected_combo}, "
                            f"sentence='{finding.sentence}' "
                            f"-> won_intent={finding.won_intent}, "
                            f"won_combo={finding.won_combo}, "
                            f"won_slots={finding.won_slots}"
                        )

    print()
    print(
        f"Checked {total_sentences} test sentence(s) across "
        f"{len(languages)} language(s)."
    )
    print(f"Cross-intent over-matches: {total_mismatches}")
    print(f"No-match sentences: {total_no_match}")

    return 1 if total_mismatches else 0
