"""Translation utils."""

import argparse
from typing import Any, Dict, Tuple

import yaml
from hassil import merge_dict

from .const import (
    INTENTS_FILE,
    LIST_DIR,
    RESPONSE_DIR,
    RULE_DIR,
    SENTENCE_DIR,
    TESTS_DIR,
)


# pylint:disable=too-many-ancestors
class YamlDumper(yaml.Dumper):
    """Subclassed dumper to ensure correct indentation."""

    def increase_indent(self, flow=False, indentless=False):
        return super().increase_indent(flow, False)


def get_base_arg_parser() -> argparse.ArgumentParser:
    """Get a base argument parser."""
    parser = argparse.ArgumentParser(description="Home Assistant Translations")
    parser.add_argument(
        "action",
        type=str,
        choices=[
            "add_language",
            "check_overmatch",
            "check_slot_combinations",
            "codeowners",
            "count_sentences",
            "language_table",
            "llm_template",
            "merged_output",
            "parse",
            "prune",
            "report_unparsed_examples",
            "sample_template",
            "sample",
            "slot_combination_summary",
            "transliterate",
            "validate",
            "website_summary",
        ],
    )
    parser.add_argument("--debug", action="store_true", help="Enable log output")
    return parser


def load_merged_sentences(language: str) -> dict:
    merged_sentences: dict = {}
    language_dir = SENTENCE_DIR / language

    # Language-level config (errors, skip words, ...) lives in top-level files
    # such as _common.yaml.
    for sentence_file in sorted(language_dir.glob("*.yaml")):
        merge_dict(merged_sentences, yaml.safe_load(sentence_file.read_text()))

    # Since the slot-combination migration, each intent's sentences live in
    # sentences/<lang>/<intent>/<slot_combination>.yaml, with the file rooted at
    # `data:` (the intent comes from the directory name). Reconstruct the
    # `intents: <Intent>: data:` shape that downstream code expects.
    intents: dict = merged_sentences.setdefault("intents", {})
    for intent_dir in sorted(p for p in language_dir.iterdir() if p.is_dir()):
        intent_name = intent_dir.name
        for combo_file in sorted(intent_dir.glob("*.yaml")):
            combo_data = yaml.safe_load(combo_file.read_text()) or {}
            for sentence_set in combo_data.get("data", []):
                intents.setdefault(intent_name, {}).setdefault("data", []).append(
                    sentence_set
                )

    return merged_sentences


def load_intents_dict(language: str) -> Dict[str, Any]:
    """Assemble a complete, hassil-ready intents dict for a language.

    Handles both the legacy flat format
    (``sentences/<lang>/<domain>_<Intent>.yaml``) and the per-slot-combination
    format (``sentences/<lang>/<Intent>/<combo>.yaml``). Lists and expansion
    rules are pulled from their post-migration homes (``lists/``, ``lists/<lang>/``,
    ``rules/<lang>/``), and the migration shorthands (``name_domains`` /
    ``inferred_domain`` / ``context_area``) are translated into hassil's
    ``slots`` / ``requires_context``. A partially migrated language works too:
    legacy files and combo files are merged.

    The returned dict is suitable for ``hassil.Intents.from_dict``.
    """
    language_dir = SENTENCE_DIR / language
    intents_dict: Dict[str, Any] = {"language": language, "intents": {}}

    # Legacy flat sentence files (also provides language-level config such as
    # skip_words / responses.errors via _common.yaml).
    for intent_path in language_dir.glob("*.yaml"):
        merge_dict(intents_dict, yaml.safe_load(intent_path.read_text()) or {})

    intents_dict.setdefault("intents", {})

    # Lists: shared (lists/*.yaml) + language-specific (lists/<lang>/*.yaml)
    lists_dict: Dict[str, Any] = intents_dict.setdefault("lists", {})
    for list_path in (
        *LIST_DIR.glob("*.yaml"),
        *(LIST_DIR / language).glob("*.yaml"),
    ):
        lists_dict.update(
            (yaml.safe_load(list_path.read_text()) or {}).get("lists", {})
        )

    # Expansion rules: language-specific (rules/<lang>/*.yaml)
    rules_dict: Dict[str, Any] = intents_dict.setdefault("expansion_rules", {})
    for rule_path in (RULE_DIR / language).glob("*.yaml"):
        rules_dict.update(
            (yaml.safe_load(rule_path.read_text()) or {}).get("expansion_rules", {})
        )

    # Per-slot-combination sentence files (new format)
    intent_info = yaml.safe_load(INTENTS_FILE.read_text())
    for intent_name, info in intent_info.items():
        for combo_name, combo_info in (info.get("slot_combinations") or {}).items():
            combo_path = language_dir / intent_name / f"{combo_name}.yaml"
            if not combo_path.exists():
                continue

            combo_dict = yaml.safe_load(combo_path.read_text()) or {}
            intent_data = intents_dict["intents"].setdefault(intent_name, {"data": []})[
                "data"
            ]
            for data in combo_dict.get("data", []):
                slots, requires_context = resolve_domain_context(data, combo_info)
                intent_data.append(
                    {
                        "sentences": data["sentences"],
                        "slots": slots,
                        "requires_context": requires_context,
                        "response": data["response"],
                    }
                )

    return intents_dict


def resolve_domain_context(
    data: Dict[str, Any], combo_info: Dict[str, Any]
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Translate the slot-combination shorthands into hassil fragments.

    Given a sentence ``data`` group and its slot-combination ``combo_info`` (from
    ``intents.yaml``), return the ``(slots, requires_context)`` that hassil
    expects. This is the single place the ``name_domains`` / ``inferred_domain``
    / ``context_area`` shorthands are converted, so every consumer (the loader,
    the tests, and the intentfest scripts) stays in sync.

    ``name_domains`` may be an explicit list of domains or a string naming a
    reusable set defined in ``combo_info['name_domain_groups']``; the latter is
    resolved to its concrete list here.
    """
    slots = dict(data.get("slots", {}))
    requires_context = dict(data.get("requires_context", {}))

    if name_domains := data.get("name_domains"):
        if isinstance(name_domains, str):
            # Named group defined in intents.yaml (name_domain_groups)
            name_domains = combo_info["name_domain_groups"][name_domains]
        # {name} is restricted to entities with one of these domains
        requires_context["domain"] = name_domains
    elif inferred_domain := data.get("inferred_domain"):
        # Domain is inferred from the words in the sentence
        slots["domain"] = inferred_domain

    if combo_info.get("context_area"):
        # Area comes from the voice satellite's context
        requires_context["area"] = {"slot": True}

    return slots, requires_context


def _slug(name: str) -> str:
    """Synthesize an id from a human name (mirrors the test harness)."""
    return name.strip().casefold().replace(" ", "_")


def load_fixtures(language: str) -> Dict[str, Any]:
    """Load test fixtures (entities/areas/floors/timers/media) for a language.

    Prefers a monolithic ``tests/<lang>/_fixtures.yaml`` when present. Otherwise
    — the per-slot-combination format, where each test file carries its own
    inline fixtures — it aggregates the fixtures declared across every
    ``tests/<lang>/<Intent>/<combo>.yaml`` file, synthesizing the ids the test
    harness would (mirroring ``tests/test_slot_combinations.py``).

    The returned dict is compatible with ``shared.get_slot_lists`` /
    ``get_states`` / ``get_areas`` / ``get_floors``.
    """
    tests_dir = TESTS_DIR / language

    legacy_fixtures = tests_dir / "_fixtures.yaml"
    if legacy_fixtures.exists():
        return yaml.safe_load(legacy_fixtures.read_text()) or {}

    entities: Dict[str, Dict[str, Any]] = {}
    areas: Dict[str, Dict[str, Any]] = {}
    floors: Dict[str, Dict[str, Any]] = {}
    timers: list = []
    media: list = []

    for combo_file in sorted(tests_dir.glob("*/*.yaml")):
        test_dict = yaml.safe_load(combo_file.read_text()) or {}

        for floor in test_dict.get("floors", []):
            floor_id = _slug(floor["name"])
            floors.setdefault(floor_id, {"id": floor_id, "name": floor["name"]})

        for area in test_dict.get("areas", []):
            area_id = _slug(area["name"])
            entry = {"id": area_id, "name": area["name"]}
            if area.get("floor"):
                entry["floor"] = _slug(area["floor"])
            areas.setdefault(area_id, entry)

        for entity in test_dict.get("entities", []):
            entity_id = f"{entity['domain']}.{_slug(entity['name'])}"
            if entity_id in entities:
                continue
            entry = {"id": entity_id, "name": entity["name"]}
            if "state" in entity:
                entry["state"] = entity["state"]
            elif "state_with_unit" in entity:
                # No raw state given; use the human state_with_unit for rendering.
                entry["state"] = entity["state_with_unit"]
            if entity.get("area"):
                entry["area"] = _slug(entity["area"])
            if entity.get("attributes"):
                entry["attributes"] = entity["attributes"]
            if "is_exposed" in entity:
                entry["is_exposed"] = entity["is_exposed"]
            entities[entity_id] = entry

        timers.extend(test_dict.get("timers", []))
        media.extend(test_dict.get("media", []))

    return {
        "language": language,
        "entities": list(entities.values()),
        "areas": list(areas.values()),
        "floors": list(floors.values()),
        "timers": timers,
        "media": media,
    }


def load_merged_responses(language: str) -> dict:
    merged_responses: dict = {}
    for response_file in (RESPONSE_DIR / language).glob("*.yaml"):
        merge_dict(merged_responses, yaml.safe_load(response_file.read_text()))
    return merged_responses
