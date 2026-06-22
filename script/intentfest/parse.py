"""Parse sentences using language intent files."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Iterable
from typing import Any, Dict, Optional

import yaml
from hassil import (
    Intents,
    RecognizeResult,
    merge_dict,
    normalize_whitespace,
    recognize_all,
    recognize_best,
)

from shared import (
    get_areas,
    get_floors,
    get_matched_states,
    get_slot_lists,
    get_states,
    render_response,
)

from .const import INTENTS_FILE, LANGUAGES, LIST_DIR, RULE_DIR, SENTENCE_DIR, TESTS_DIR
from .util import get_base_arg_parser, load_merged_responses


def get_arguments() -> argparse.Namespace:
    """Get parsed passed in arguments."""
    parser = get_base_arg_parser()
    parser.add_argument(
        "--language",
        required=True,
        type=str,
        choices=LANGUAGES,
        help="The language to validate.",
    )
    parser.add_argument(
        "--sentence",
        required=True,
        action="append",
        type=str,
        help="Sentence(s) to parse",
    )
    parser.add_argument(
        "--context",
        action="append",
        nargs=2,
        default=[],
        metavar=("key", "value"),
        help="Add key/value pair to context",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="List all possible matches instead of just the best one",
    )
    return parser.parse_args()


def run() -> int:
    args = get_arguments()

    language_dir = SENTENCE_DIR / args.language
    tests_dir = TESTS_DIR / args.language

    # Load test areas and entities for language
    fixtures = yaml.safe_load((tests_dir / "_fixtures.yaml").read_text())
    slot_lists = get_slot_lists(fixtures)
    states = get_states(fixtures)
    areas = get_areas(fixtures)
    floors = get_floors(fixtures)

    # Load intents. This supports both the legacy flat format
    # (sentences/<lang>/<domain>_<Intent>.yaml) and the per-slot-combination
    # format (sentences/<lang>/<Intent>/<combo>.yaml). A fully migrated language
    # has only the latter, so we also load lists/rules from their new homes.
    intents_dict: Dict[str, Any] = {"language": args.language, "intents": {}}

    # Legacy flat sentence files (also provides skip_words via _common.yaml)
    for intent_path in language_dir.glob("*.yaml"):
        with open(intent_path, "r", encoding="utf-8") as intent_file:
            merge_dict(intents_dict, yaml.safe_load(intent_file))

    intents_dict.setdefault("intents", {})

    # Lists: shared (lists/*.yaml) + language-specific (lists/<lang>/*.yaml)
    lists_dict: Dict[str, Any] = intents_dict.setdefault("lists", {})
    for list_path in (
        *LIST_DIR.glob("*.yaml"),
        *(LIST_DIR / args.language).glob("*.yaml"),
    ):
        lists_dict.update(
            (yaml.safe_load(list_path.read_text()) or {}).get("lists", {})
        )

    # Expansion rules: language-specific (rules/<lang>/*.yaml)
    rules_dict: Dict[str, Any] = intents_dict.setdefault("expansion_rules", {})
    for rule_path in (RULE_DIR / args.language).glob("*.yaml"):
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
                slots = dict(data.get("slots", {}))
                requires_context = dict(data.get("requires_context", {}))
                if name_domains := data.get("name_domains"):
                    requires_context["domain"] = name_domains
                elif inferred_domain := data.get("inferred_domain"):
                    slots["domain"] = inferred_domain

                if combo_info.get("context_area"):
                    requires_context["area"] = {"slot": True}

                intent_data.append(
                    {
                        "sentences": data["sentences"],
                        "slots": slots,
                        "requires_context": requires_context,
                        "response": data["response"],
                    }
                )

    assert intents_dict["intents"], "No intents loaded"
    intents = Intents.from_dict(intents_dict)

    responses = (
        load_merged_responses(args.language).get("responses", {}).get("intents", {})
    )

    intent_context = dict(args.context)

    # Parse sentences
    for sentence in args.sentence:
        if args.all:
            results: Iterable[Optional[RecognizeResult]] = recognize_all(
                sentence, intents, slot_lists=slot_lists, intent_context=intent_context
            )
        else:
            results = [
                recognize_best(
                    sentence,
                    intents,
                    slot_lists=slot_lists,
                    intent_context=intent_context,
                    best_slot_name="name",
                )
            ]

        for result in results:
            if result is None:
                continue

            output_dict = {"text": sentence, "match": result is not None}
            if result is not None:
                output_dict["intent"] = result.intent.name
                output_dict["slots"] = {
                    entity.name: entity.value for entity in result.entities_list
                }
                output_dict["context"] = result.context
                output_dict["text_chunks_matched"] = result.text_chunks_matched

                # Response
                matched, unmatched = get_matched_states(states, areas, floors, result)
                output_dict["response_key"] = result.response
                response_template = responses.get(result.intent.name, {}).get(
                    result.response
                )
                output_dict["response"] = normalize_whitespace(
                    render_response(response_template, result, matched, unmatched)
                ).strip()

                if result.intent_sentence is not None:
                    output_dict["template"] = result.intent_sentence.text

            json.dump(output_dict, sys.stdout, ensure_ascii=False, indent=2)
            print("")

        print("")

    return 0
