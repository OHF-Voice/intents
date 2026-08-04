"""Generate a template to give to an LLM to translate a file."""

from __future__ import annotations

import argparse

import yaml

from .const import (
    INTENTS_FILE,
    LANGUAGES,
    LANGUAGES_FILE,
    RESPONSE_DIR,
    ROOT,
    SENTENCE_DIR,
    TESTS_DIR,
)
from .util import get_base_arg_parser

# Sort intent info by (domain, intent)
INTENT_INFO = yaml.safe_load(INTENTS_FILE.read_text())


def get_arguments() -> argparse.Namespace:
    """Get parsed passed in arguments."""
    parser = get_base_arg_parser()
    parser.add_argument(
        "language",
        type=str,
        choices=[lang for lang in LANGUAGES if lang != "en"],
        help="The language to target.",
    )
    parser.add_argument(
        "intent",
        type=str,
        choices=INTENT_INFO,
        help="The intent to generate.",
    )
    return parser.parse_args()


def run() -> int:
    args = get_arguments()

    language_info = yaml.safe_load(LANGUAGES_FILE.read_text())

    to_collect = [
        RESPONSE_DIR / f"en/{args.intent}.yaml",
    ]

    # Find sentences. In the per-slot-combination format each intent's sentences
    # live in sentences/en/<intent>/<combo>.yaml, with tests alongside in
    # tests/en/<intent>/<combo>.yaml.
    intent_sentence_dir = SENTENCE_DIR / "en" / args.intent
    if intent_sentence_dir.is_dir():
        for sentence_file in sorted(intent_sentence_dir.glob("*.yaml")):
            to_collect.append(sentence_file)
            test_file = TESTS_DIR / "en" / args.intent / sentence_file.name
            if test_file.exists():
                to_collect.append(test_file)

    # Legacy flat format (languages/intents not yet migrated).
    for sentence_file in sorted((SENTENCE_DIR / "en").glob("*.yaml")):
        if sentence_file.name == "_common.yaml":
            continue
        content = yaml.safe_load(sentence_file.read_text()) or {}
        if args.intent not in content.get("intents", {}):
            continue

        to_collect.append(sentence_file)
        to_collect.append(TESTS_DIR / f"en/{sentence_file.name}")

    english_files = []

    for path in to_collect:
        english_files.append(
            "\n".join([str(path.relative_to(ROOT)) + ":", path.read_text(), ""])
        )

    print(
        TEMPLATE.format(
            language_name=language_info[args.language]["nativeName"],
            language=args.language,
            english_files="\n".join(english_files),
        )
    )

    return 0


TEMPLATE = """
You are going to translate a voice assistant intent from English to {language_name}.

The English files are located in the `en` directory.
The translated files are located in the `{language}` directory.
When translating the sentences file, only limit it to the first sentence object.
Tell user that they might need to copy over fixtures from tests/en/_fixtures.yaml.

{english_files}
"""
