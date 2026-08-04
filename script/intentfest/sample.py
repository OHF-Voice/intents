"""Sample sentences using language intent files."""

from __future__ import annotations

import argparse
import json
import sys

from hassil import Intents, sample_intents

from shared import get_slot_lists

from .const import LANGUAGES
from .util import get_base_arg_parser, load_fixtures, load_intents_dict


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
        "-n",
        "--max-sentences-per-intent",
        type=int,
        help="Limit number of sentences per intent",
    )
    parser.add_argument(
        "--intents", nargs="+", help="Only sample sentences from these intents"
    )
    return parser.parse_args()


def run() -> int:
    args = get_arguments()

    # Load test areas and entities for language (from _fixtures.yaml when
    # present, else aggregated from the per-slot-combination test files).
    test_names = load_fixtures(args.language)
    slot_lists = get_slot_lists(test_names)

    # Load intents (legacy flat + per-slot-combination format)
    intents_dict = load_intents_dict(args.language)

    assert intents_dict["intents"], "No intents loaded"
    intents = Intents.from_dict(intents_dict)

    # Sample sentences
    intents_and_texts = sample_intents(
        intents,
        slot_lists,
        max_sentences_per_intent=args.max_sentences_per_intent,
        intent_names=set(args.intents) if args.intents else None,
    )
    for intent_name, sentence_text in intents_and_texts:
        json.dump(
            {"intent": intent_name, "text": sentence_text.strip()},
            sys.stdout,
            ensure_ascii=False,
        )
        print("")

    return 0
