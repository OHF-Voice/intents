"""Slot combination tests."""

import itertools
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from functools import lru_cache, partial
from typing import Any, Optional

import pytest
import yaml
from hassil import (
    Intents,
    RecognizeResult,
    SlotList,
    TextSlotList,
    normalize_whitespace,
    recognize_best,
)
from jinja2 import BaseLoader, Environment, StrictUndefined

from shared import get_areas, get_floors, get_matched_states, get_states, state_attr

from . import (
    BASE_DIR,
    INTENTS_FILE,
    LISTS_DIR,
    RESPONSES_DIR,
    RULES_DIR,
    SENTENCES_DIR,
    TESTS_DIR,
)


def _slug(name: str) -> str:
    """Synthesize an id from a human name."""
    return name.strip().casefold().replace(" ", "_")


def _build_fixtures(test_dict: dict[str, Any]) -> dict[str, Any]:
    """Convert a self-contained slot-combination test file into a fixtures dict
    compatible with the shared get_states/get_areas/get_floors helpers."""
    floors = [
        {"id": _slug(f["name"]), "name": f["name"]} for f in test_dict.get("floors", [])
    ]
    areas = [
        {
            "id": _slug(a["name"]),
            "name": a["name"],
            **({"floor": _slug(a["floor"])} if a.get("floor") else {}),
        }
        for a in test_dict.get("areas", [])
    ]
    entities = []
    for e in test_dict.get("entities", []):
        entity = {
            "id": f"{e['domain']}.{_slug(e['name'])}",
            "name": e["name"],
        }
        if "state" in e:
            entity["state"] = e["state"]
        elif "state_with_unit" in e:
            # No raw state given; use the human state_with_unit for rendering.
            entity["state"] = e["state_with_unit"]
        if e.get("area"):
            entity["area"] = _slug(e["area"])
        if e.get("attributes"):
            entity["attributes"] = e["attributes"]
        if "is_exposed" in e:
            entity["is_exposed"] = e["is_exposed"]
        entities.append(entity)
    return {
        "entities": entities,
        "areas": areas,
        "floors": floors,
        "timers": test_dict.get("timers", []),
        "media": test_dict.get("media", []),
    }


CONTEXT_AREA_NAME = "__context_area__"
TEST_DATETIME = datetime(year=2013, month=9, day=17, hour=1, minute=2)


@lru_cache(maxsize=None)
def is_fully_migrated(language: str) -> bool:
    """Return True if a language has fully migrated to the slot-combination format.

    A language is considered fully migrated once its sentences live in per-intent
    slot-combination subdirectories (``sentences/<lang>/<Intent>/<combo>.yaml``) and
    no legacy flat ``sentences/<lang>/<domain>_<intent>.yaml`` files remain (only
    ``_common.yaml`` is allowed alongside the subdirectories).

    The required-combo coverage gate is only enforced for fully migrated languages,
    so this is detected automatically instead of maintaining a hand-kept list.
    """
    lang_dir = SENTENCES_DIR / language
    has_combo_dirs = any(child.is_dir() for child in lang_dir.iterdir())
    has_legacy_files = any(
        path.name != "_common.yaml" for path in lang_dir.glob("*.yaml")
    )
    return has_combo_dirs and not has_legacy_files


@dataclass
class LanguageResources:
    language: str
    """Language code."""

    intents: Intents
    """Compiled intents for language."""

    responses: dict[str, dict[str, str]]
    """Response by intent -> key"""

    template_env: Environment = field(
        default_factory=lambda: Environment(
            loader=BaseLoader(), undefined=StrictUndefined
        )
    )


@pytest.fixture(name="lang_resources", scope="session")
def lang_resources_fixture(language: str, intent_schemas: dict[str, Any]):
    lang_intents_dict: dict[str, Any] = {
        "language": language,
        "intents": {},
        "lists": {},
        "expansion_rules": {},
        "skip_words": [],
    }

    # Load skip words (Home Assistant applies these at runtime, from _common.yaml)
    common_path = SENTENCES_DIR / language / "_common.yaml"
    if common_path.exists():
        with open(common_path, "r", encoding="utf-8") as common_file:
            common_dict = yaml.safe_load(common_file) or {}
        lang_intents_dict["skip_words"] = common_dict.get("skip_words", [])

    # Load expansion rules
    rules_dict: dict[str, Any] = lang_intents_dict["expansion_rules"]
    for rule_path in (RULES_DIR / language).glob("*.yaml"):
        with open(rule_path, "r", encoding="utf-8") as rule_file:
            rule_dict = yaml.safe_load(rule_file)
            rules_dict.update(rule_dict["expansion_rules"])

    # Load shared lists
    lists_dict: dict[str, Any] = lang_intents_dict["lists"]
    for list_path in LISTS_DIR.glob("*.yaml"):
        with open(list_path, "r", encoding="utf-8") as list_file:
            list_dict = yaml.safe_load(list_file)
            lists_dict.update(list_dict["lists"])

    # Load language-specific lists
    for list_path in (LISTS_DIR / language).glob("*.yaml"):
        with open(list_path, "r", encoding="utf-8") as list_file:
            list_dict = yaml.safe_load(list_file)
            lists_dict.update(list_dict["lists"])

    responses: dict[str, dict[str, str]] = {}
    for intent_name, intent_info in intent_schemas.items():
        intent_dict = lang_intents_dict["intents"].get(intent_name, {"data": []})
        intent_data = intent_dict["data"]

        responses_path = RESPONSES_DIR / language / f"{intent_name}.yaml"
        if responses_path.exists():
            with open(responses_path, "r", encoding="utf-8") as responses_file:
                responses_dict = yaml.safe_load(responses_file)

            responses[intent_name] = responses_dict["responses"]["intents"][intent_name]
        else:
            responses[intent_name] = {}  # no responses

        for combo_name, combo_info in intent_info["slot_combinations"].items():
            sentences_path = (
                SENTENCES_DIR / language / intent_name / f"{combo_name}.yaml"
            )
            if not sentences_path.exists():
                continue

            with open(sentences_path, "r", encoding="utf-8") as sentences_file:
                test_data_dict = yaml.safe_load(sentences_file)

                # All sentence templates for this slot combination, across every
                # group, so coverage is checked for the whole file (not just the
                # first group a test sentence happens to match).
                combo_templates = [
                    sentence
                    for group in test_data_dict["data"]
                    for sentence in group["sentences"]
                ]

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

                    # Attach metadata so we can check the slot combination later
                    test_metadata["slot_combination"] = combo_name
                    test_metadata["sentence_templates"] = combo_templates

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

    return LanguageResources(
        language=language,
        intents=Intents.from_dict(lang_intents_dict),
        responses=responses,
    )


def do_test_slot_combination(
    lang_resources: LanguageResources,
    intent_name: str,
    combo_name: str,
    combo_info: dict[str, Any],
) -> None:
    test_file_path = (
        TESTS_DIR / lang_resources.language / intent_name / f"{combo_name}.yaml"
    )
    error_info = (
        f"language={lang_resources.language}, "
        f"intent={intent_name}, "
        f"slot_combination={combo_name}, "
        f"file={test_file_path.relative_to(BASE_DIR)}"
    )

    if is_fully_migrated(lang_resources.language) and (
        (combo_info.get("importance") == "required")
        or (
            "required" in combo_info.get("name_domains", {})
            or ("required" in combo_info.get("inferred_domains", {}))
        )
    ):
        # Fail if slot combination is required
        assert test_file_path.exists(), f"Required test file is missing: {error_info}"

    if not test_file_path.exists():
        return

    with open(test_file_path, "r", encoding="utf-8") as test_file:
        test_dict = yaml.safe_load(test_file)

    # Load test fixtures
    slot_lists: dict[str, SlotList] = {
        "name": TextSlotList.from_tuples(
            [
                # text in, value out, context, metadata
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

    # Full HA-like fixtures for response rendering (state/query/state_attr).
    fixtures = _build_fixtures(test_dict)
    states = get_states(fixtures)
    area_entries = get_areas(fixtures)
    floor_entries = get_floors(fixtures)

    timers: list[dict[str, Any]] = test_dict.get("timers", [])
    media: list[dict[str, Any]] = test_dict.get("media", [])
    shopping_list: list[dict[str, Any]] = test_dict.get("shopping_list", [])

    # For quick look-up during individual tests
    entity_domains_by_name: dict[str, set[str]] = defaultdict(set)
    for test_entity in test_dict.get("entities", []):
        entity_domains_by_name[test_entity["name"]].add(test_entity["domain"])

    possible_slot_names: set[str] = set(combo_info["slots"])
    name_domains: set[str] = set(
        itertools.chain.from_iterable(combo_info.get("name_domains", {}).values())
    )
    inferred_domains: set[str] = set(
        itertools.chain.from_iterable(combo_info.get("inferred_domains", {}).values())
    )

    # Retrieved from metadata
    untested_sentence_templates: Optional[set[str]] = None

    # sentence text -> matched template
    matching_sentence_templates: dict[str, str] = {}

    # TODO: add validation in script
    for test_group in test_dict["tests"]:
        expected_slots = test_group.get("slots", {})

        if inferred_domains:
            expected_slots["domain"] = inferred_domains

        expected_slot_names = expected_slots.keys()
        assert expected_slot_names == possible_slot_names

        expected_response = test_group["response"]
        group_timers = test_group.get("timers", timers)
        group_media = test_group.get("media", media)
        group_shopping_list = test_group.get("shopping_list", shopping_list)

        for test_sentence in test_group["sentences"]:
            sentence_error_info = f"sentence='{test_sentence}', {error_info}"
            result = recognize_best(
                test_sentence,
                lang_resources.intents,
                slot_lists=slot_lists,
                intent_context={"area": CONTEXT_AREA_NAME},
                best_slot_name="name",
            )
            assert (
                result is not None
            ), f"Sentence was not recognized: {sentence_error_info}"
            assert (
                result.intent.name == intent_name
            ), f"Test sentence did not match expected intent: {sentence_error_info}"
            assert result.intent_metadata is not None, sentence_error_info
            assert (
                result.intent_metadata.get("slot_combination") == combo_name
            ), f"Wrong slot combination was matched: {sentence_error_info}"
            assert result.intent_sentence is not None
            assert result.intent_sentence.text is not None

            if untested_sentence_templates is None:
                untested_sentence_templates = set(
                    result.intent_metadata["sentence_templates"]
                )

            untested_sentence_templates.discard(result.intent_sentence.text)
            matching_sentence_templates[test_sentence] = result.intent_sentence.text

            actual_response = _render_response(
                lang_resources,
                result,
                states,
                area_entries,
                floor_entries,
                template_slots={
                    "timers": group_timers,
                    "media": group_media[0] if group_media else None,
                    "completed_items": group_shopping_list,
                },
            )
            assert (
                actual_response == expected_response
            ), f"Wrong response: {sentence_error_info}"

            actual_slots = {e_name: e.value for e_name, e in result.entities.items()}

            if combo_info.get("context_area"):
                # Remove context area
                assert (
                    actual_slots.pop("area") == CONTEXT_AREA_NAME
                ), f"Expected context area: {sentence_error_info}"

            actual_slot_names = actual_slots.keys()

            if name_domains:
                actual_name = actual_slots["name"]
                assert (
                    actual_name in entity_domains_by_name
                ), f"Test entity name was not recognized: {sentence_error_info}"
                assert entity_domains_by_name[actual_name].issubset(
                    name_domains
                ), f"Entity does not have expected domain: name={actual_name}, {sentence_error_info}"
            elif inferred_domains:
                assert (
                    actual_slots.get("domain") in inferred_domains
                ), f"Wrong inferred domain: {sentence_error_info}"

            assert (
                expected_slot_names == actual_slot_names
            ), f"Slot names to not match expectations: {sentence_error_info}"

            for actual_slot_name in actual_slot_names:
                actual_slot_value = actual_slots[actual_slot_name]
                expected_slot_value = expected_slots[actual_slot_name]

                # Multiple values are possible for some slots.
                # For example, "open the curtains" may match shades as well.
                if isinstance(actual_slot_value, (list, set)):
                    if isinstance(expected_slot_value, (list, set)):
                        assert set(actual_slot_value).issubset(
                            expected_slot_value
                        ), f"Slot value is not a subset of expected values: {sentence_error_info}"
                    else:
                        assert (
                            expected_slot_value in actual_slot_value
                        ), f"Slot value is not in list of expected values: {sentence_error_info}"
                else:
                    if isinstance(expected_slot_value, (list, set)):
                        assert (
                            actual_slot_value in expected_slot_value
                        ), f"Slot value does not match any of expected values: {sentence_error_info}"
                    else:
                        assert (
                            expected_slot_value == actual_slot_value
                        ), f"Slot value does not match expected value: {sentence_error_info}"

    assert not untested_sentence_templates, (
        f"{len(untested_sentence_templates)} untested sentence template(s): {error_info}, "
        f"missing={untested_sentence_templates}, "
        f"matching={matching_sentence_templates}"
    )


def _render_response(  # pylint: disable=too-many-positional-arguments
    lang_resources: "LanguageResources",
    result: RecognizeResult,
    states: list,
    area_entries: list,
    floor_entries: list,
    template_slots: Optional[dict[str, Any]] = None,
) -> str:
    intent_name = result.intent.name
    response_key = result.response or "default"

    intent_responses = lang_resources.responses.get(intent_name)
    if not intent_responses:
        return ""

    response_template = intent_responses.get(response_key)
    if not response_template:
        return ""

    if template_slots is None:
        template_slots = {}

    # Numeric slots (from range lists) render via the spoken text (e.g. "1",
    # "30") so responses that branch on the text work as in Home Assistant;
    # non-numeric slots render via their `out` value (e.g. "garage", "red").
    def _slot_value(e):
        v = e.value
        if isinstance(v, bool):
            return v
        if isinstance(v, (int, float)) and e.text_clean:
            return e.text_clean
        return v

    template_slots.update(
        {e_name: _slot_value(e) for e_name, e in result.entities.items()}
    )
    template_args: dict[str, Any] = {"slots": template_slots}

    # Resolve matched/unmatched states for state/query/state_attr.
    # The {name} slot resolves a single entity leniently (ignoring area/floor);
    # otherwise match by area/floor/domain/device_class via shared logic.
    name_entity = result.entities.get("name")
    if name_entity is not None:
        norm_name = name_entity.value.strip().casefold()
        name_states = [s for s in states if s.name.strip().casefold() == norm_name]
        state_entity = result.entities.get("state")
        if state_entity is not None:
            matched = [s for s in name_states if s.hass_state == state_entity.value]
            unmatched = [s for s in name_states if s.hass_state != state_entity.value]
        else:
            matched, unmatched = name_states, []
    else:
        matched, unmatched = get_matched_states(
            states, area_entries, floor_entries, result
        )

    template_args["state"] = (
        matched[0] if matched else (unmatched[0] if unmatched else None)
    )
    template_args["query"] = {
        "matched": matched,
        "unmatched": unmatched,
        "total_results": len(matched) + len(unmatched),
    }
    template_args["state_attr"] = partial(state_attr, matched)

    if intent_name == "HassGetCurrentDate":
        template_slots["date"] = TEST_DATETIME.date()
    elif intent_name == "HassGetCurrentTime":
        template_slots["time"] = TEST_DATETIME.time()

    if timers := template_slots.get("timers"):
        # Add missing fields
        for timer_dict in timers:
            timer_dict.setdefault("name", "")
            timer_dict.setdefault("area", "")
            timer_dict.setdefault("is_active", False)
            timer_dict.setdefault("total_seconds_left", 0)
            timer_dict.setdefault("start_hours", 0)
            timer_dict.setdefault("start_minutes", 0)
            timer_dict.setdefault("start_seconds", 0)
            timer_dict.setdefault("rounded_hours_left", 0)
            timer_dict.setdefault("rounded_minutes_left", 0)
            timer_dict.setdefault("rounded_seconds_left", 0)
        template_slots["canceled"] = len(timers)
    else:
        template_slots["canceled"] = 0

    response_text = lang_resources.template_env.from_string(response_template).render(
        template_args
    )
    response_text = normalize_whitespace(response_text).strip()

    return response_text


def gen_test(intent_name: str, combo_name: str, combo_info: dict[str, Any]) -> None:
    def test_func(lang_resources) -> None:
        do_test_slot_combination(
            lang_resources,
            intent_name=intent_name,
            combo_name=combo_name,
            combo_info=combo_info,
        )

    test_func.__name__ = f"test_{intent_name}_{combo_name}"
    setattr(sys.modules[__name__], test_func.__name__, test_func)


def gen_tests() -> None:
    with open(INTENTS_FILE, "r", encoding="utf-8") as schemas_file:
        intent_schemas = yaml.safe_load(schemas_file)

    for intent_name, intent_info in sorted(intent_schemas.items()):
        for combo_name, combo_info in sorted(intent_info["slot_combinations"].items()):
            gen_test(intent_name, combo_name, combo_info)


gen_tests()
