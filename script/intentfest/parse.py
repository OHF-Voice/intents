"""Parse sentences using language intent files."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Iterable
from typing import Optional

from hassil import (
    Intents,
    RecognizeResult,
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

from .const import LANGUAGES
from .util import (
    get_base_arg_parser,
    load_fixtures,
    load_intents_dict,
    load_merged_responses,
)


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

    # Load test areas and entities for language (from _fixtures.yaml when
    # present, else aggregated from the per-slot-combination test files).
    fixtures = load_fixtures(args.language)
    slot_lists = get_slot_lists(fixtures)
    states = get_states(fixtures)
    areas = get_areas(fixtures)
    floors = get_floors(fixtures)

    # Load intents. This supports both the legacy flat format
    # (sentences/<lang>/<domain>_<Intent>.yaml) and the per-slot-combination
    # format (sentences/<lang>/<Intent>/<combo>.yaml).
    intents_dict = load_intents_dict(args.language)

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
