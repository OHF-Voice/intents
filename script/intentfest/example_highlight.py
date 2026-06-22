"""Highlight slot values inside example sentences.

Uses hassil to parse an example sentence against the language's intents and the
slot lists built from the matching test fixtures. Each matched entity exposes a
``text_span`` (start/end offsets into the original sentence), which we wrap in a
``<span class="slot slot-<category>">`` so the website can colour-code names,
areas, floors, numbers, wildcards, etc.

Everything here is best-effort: if a language's intents fail to build or a
sentence does not recognise, we fall back to the plain (HTML-escaped) text.
"""

from __future__ import annotations

import html
from typing import Any, Dict, Optional

import yaml

from .const import INTENTS_FILE, LIST_DIR, RULE_DIR, SENTENCE_DIR, TESTS_DIR

# Map each slot name to a colour category. Slots not listed fall back to
# "number" (numeric/range slots) or "other".
_SLOT_CATEGORY: Dict[str, str] = {
    "name": "name",
    "area": "area",
    "floor": "floor",
    "domain": "class",
    "device_class": "class",
    "media_class": "class",
    "color": "color",
    "state": "state",
    "message": "text",
    "search_query": "text",
    "conversation_command": "text",
    "item": "text",
}
# Placeholder current-area name passed as intent context so templates that
# reference the current area (e.g. "turn on the lights in here") recognize.
_CONTEXT_AREA_NAME = "__context_area__"

_NUMBER_SLOTS = {
    "brightness",
    "percentage",
    "position",
    "temperature",
    "volume_level",
    "volume_step",
    "hours",
    "minutes",
    "seconds",
    "start_hours",
    "start_minutes",
    "start_seconds",
}


def _slot_category(slot_name: str, is_wildcard: bool) -> str:
    if is_wildcard:
        return "text"
    if slot_name in _SLOT_CATEGORY:
        return _SLOT_CATEGORY[slot_name]
    if slot_name in _NUMBER_SLOTS:
        return "number"
    return "other"


# Lazily-built hassil Intents per language (None if the language fails to build).
_LANG_INTENTS_CACHE: Dict[str, Any] = {}
# hassil symbols are imported lazily so the summary still runs if hassil changes.
_HASSIL: Dict[str, Any] = {}


def _load_hassil() -> bool:
    if _HASSIL:
        return _HASSIL.get("ok", False)
    try:
        from hassil import Intents, TextSlotList, recognize_best

        _HASSIL.update(
            ok=True,
            Intents=Intents,
            TextSlotList=TextSlotList,
            recognize_best=recognize_best,
        )
    except Exception:  # pylint: disable=broad-except
        _HASSIL["ok"] = False
    return _HASSIL["ok"]


def _build_language_intents(language: str, intent_info: dict) -> Optional[Any]:
    """Build a hassil Intents for the language from its sentences/lists/rules.

    Mirrors the slot-combination test harness, but only loads what recognition
    needs. Returns None if anything is missing or fails to parse.
    """
    if not _load_hassil():
        return None

    lang_dict: Dict[str, Any] = {
        "language": language,
        "intents": {},
        "lists": {},
        "expansion_rules": {},
        "skip_words": [],
    }

    try:
        common_path = SENTENCE_DIR / language / "_common.yaml"
        if common_path.exists():
            common_dict = yaml.safe_load(common_path.read_text()) or {}
            lang_dict["skip_words"] = common_dict.get("skip_words", [])

        for rule_path in (RULE_DIR / language).glob("*.yaml"):
            rule_dict = yaml.safe_load(rule_path.read_text()) or {}
            lang_dict["expansion_rules"].update(rule_dict.get("expansion_rules", {}))

        # Shared (cross-language) lists first, then language-specific lists.
        for list_path in LIST_DIR.glob("*.yaml"):
            list_dict = yaml.safe_load(list_path.read_text()) or {}
            lang_dict["lists"].update(list_dict.get("lists", {}))
        for list_path in (LIST_DIR / language).glob("*.yaml"):
            list_dict = yaml.safe_load(list_path.read_text()) or {}
            lang_dict["lists"].update(list_dict.get("lists", {}))

        for intent_name, info in intent_info.items():
            data: list = []
            for combo_name, combo_info in (info.get("slot_combinations") or {}).items():
                sentences_path = (
                    SENTENCE_DIR / language / intent_name / f"{combo_name}.yaml"
                )
                if not sentences_path.exists():
                    continue
                combo_data = yaml.safe_load(sentences_path.read_text()) or {}
                for group in combo_data.get("data", []):
                    slots = dict(group.get("slots", {}))
                    requires_context = dict(group.get("requires_context", {}))
                    if name_domains := group.get("name_domains"):
                        requires_context["domain"] = name_domains
                    elif inferred_domain := group.get("inferred_domain"):
                        slots["domain"] = inferred_domain
                    if combo_info.get("context_area"):
                        requires_context["area"] = {"slot": True}
                    data.append(
                        {
                            "sentences": group["sentences"],
                            "slots": slots,
                            "requires_context": requires_context,
                            "response": group.get("response", "default"),
                            "metadata": {"slot_combination": combo_name},
                        }
                    )
            if data:
                lang_dict["intents"][intent_name] = {"data": data}

        if not lang_dict["intents"]:
            return None

        return _HASSIL["Intents"].from_dict(lang_dict)
    except Exception:  # pylint: disable=broad-except
        return None


def get_language_intents(language: str, intent_info: dict) -> Optional[Any]:
    if language not in _LANG_INTENTS_CACHE:
        _LANG_INTENTS_CACHE[language] = _build_language_intents(language, intent_info)
    return _LANG_INTENTS_CACHE[language]


def _slug(name: str) -> str:
    return name.strip().lower().replace(" ", "_")


def combo_slot_lists(language: str, intent_name: str, combo_name: str) -> dict:
    """Build name/area/floor slot lists from a slot combination's test fixtures."""
    if not _load_hassil():
        return {}

    test_path = TESTS_DIR / language / intent_name / f"{combo_name}.yaml"
    if not test_path.exists():
        return {}

    try:
        test_dict = yaml.safe_load(test_path.read_text()) or {}
    except Exception:  # pylint: disable=broad-except
        return {}

    text_slot_list = _HASSIL["TextSlotList"]
    return {
        "name": text_slot_list.from_tuples(
            [
                (e["name"], e["name"], {"domain": e.get("domain")})
                for e in test_dict.get("entities", [])
                if e.get("name")
            ],
            name="name",
        ),
        "area": text_slot_list.from_strings(
            [a["name"] for a in test_dict.get("areas", []) if a.get("name")],
            name="area",
        ),
        "floor": text_slot_list.from_strings(
            [f["name"] for f in test_dict.get("floors", []) if f.get("name")],
            name="floor",
        ),
    }


def recognize_example(
    example: str, intents: Optional[Any], slot_lists: dict
) -> Optional[Any]:
    """Recognize an example sentence, returning the hassil result (or None).

    Supplies a current-area context so "in here" / context-area templates
    recognize, mirroring the slot-combination test harness.
    """
    if intents is None or not _load_hassil():
        return None
    try:
        return _HASSIL["recognize_best"](
            example,
            intents,
            slot_lists=slot_lists,
            intent_context={"area": _CONTEXT_AREA_NAME},
            best_slot_name="name",
        )
    except Exception:  # pylint: disable=broad-except
        return None


def highlight_example(example: str, intents: Optional[Any], slot_lists: dict) -> str:
    """Return the example as HTML with recognised slot values wrapped in spans.

    Falls back to the plain HTML-escaped sentence when recognition is
    unavailable or fails.
    """
    plain = html.escape(example)
    result = recognize_example(example, intents, slot_lists)
    if result is None:
        return plain

    # Collect valid, in-range spans.
    spans = []
    length = len(example)
    for entity in result.entities.values():
        text_span = getattr(entity, "text_span", None)
        if not text_span:
            continue
        start, end = text_span
        if start is None or end is None:
            continue
        if not (0 <= start < end <= length):
            continue
        # Trim surrounding whitespace so the highlight hugs the value
        # (wildcards in particular can capture a trailing space).
        while start < end and example[start].isspace():
            start += 1
        while end > start and example[end - 1].isspace():
            end -= 1
        if start >= end:
            continue
        spans.append((start, end, entity.name, bool(entity.is_wildcard)))

    if not spans:
        return plain

    spans.sort(key=lambda s: s[0])

    parts = []
    pos = 0
    for start, end, slot_name, is_wildcard in spans:
        if start < pos:
            # Overlapping match; skip to keep output well-formed.
            continue
        parts.append(html.escape(example[pos:start]))
        category = _slot_category(slot_name, is_wildcard)
        parts.append(
            f'<span class="slot slot-{category}" title="{html.escape(slot_name)}">'
            f"{html.escape(example[start:end])}</span>"
        )
        pos = end
    parts.append(html.escape(example[pos:]))
    return "".join(parts)


# Re-export for callers that want the schemas without re-reading the file.
def load_intent_info() -> dict:
    return yaml.safe_load(INTENTS_FILE.read_text())
