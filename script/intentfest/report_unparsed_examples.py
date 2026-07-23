"""Report example sentences that hassil cannot recognize.

Each slot combination sentence file may declare an ``example:`` per data block
(a human-readable hint, also used to highlight slot values on the website).
For the highlighting to work — and for the example to be trustworthy — it must
be a sentence the templates can actually produce, using values from the
combination's test fixtures.

This report parses every example with hassil and lists the ones that:

- do not recognize at all ("no match"), usually because the example uses a
  {name}/value not present in the test fixtures, or is not a sentence the
  templates can produce; or
- recognize as a *different* intent than the file they live in ("wrong intent").

Examples that recognize correctly but expose no highlightable slot (e.g.
"nevermind", or an inferred-domain "turn on the fans") are counted but not
listed, since there is nothing to fix.

Usage:
    python3 -m script.intentfest report_unparsed_examples [--language en]
"""

from __future__ import annotations

import argparse

import yaml

from .const import INTENTS_FILE, LANGUAGES, SENTENCE_DIR
from .example_highlight import combo_slot_lists, get_language_intents, recognize_example
from .util import get_base_arg_parser


def get_arguments() -> argparse.Namespace:
    """Get parsed passed in arguments."""
    parser = get_base_arg_parser()
    parser.add_argument(
        "--language",
        type=str,
        choices=LANGUAGES,
        help="Only report this language (default: all languages).",
    )
    return parser.parse_args()


def _has_highlightable_span(result) -> bool:
    return any(
        getattr(entity, "text_span", None) for entity in result.entities.values()
    )


def run() -> int:
    args = get_arguments()
    languages = [args.language] if args.language else LANGUAGES

    intent_info = yaml.safe_load(INTENTS_FILE.read_text())

    total_examples = 0
    total_no_match = 0
    total_wrong_intent = 0
    total_no_span = 0
    languages_reported = 0

    for language in languages:
        intents = get_language_intents(language, intent_info)

        problems: list[tuple[str, str, str, str]] = []
        lang_examples = 0
        lang_no_span = 0

        for intent_name, info in sorted(intent_info.items()):
            for combo_name in info.get("slot_combinations") or {}:
                combo_path = (
                    SENTENCE_DIR / language / intent_name / f"{combo_name}.yaml"
                )
                if not combo_path.exists():
                    continue

                combo_data = yaml.safe_load(combo_path.read_text()) or {}
                slot_lists = combo_slot_lists(language, intent_name, combo_name)

                for block in combo_data.get("data") or []:
                    example = block.get("example")
                    if not example:
                        continue

                    lang_examples += 1
                    result = recognize_example(example, intents, slot_lists)

                    if result is None:
                        problems.append((intent_name, combo_name, example, "no match"))
                    elif result.intent.name != intent_name:
                        problems.append(
                            (
                                intent_name,
                                combo_name,
                                example,
                                f"matched {result.intent.name}",
                            )
                        )
                    elif not _has_highlightable_span(result):
                        lang_no_span += 1

        total_examples += lang_examples
        total_no_span += lang_no_span
        total_no_match += sum(1 for p in problems if p[3] == "no match")
        total_wrong_intent += sum(1 for p in problems if p[3] != "no match")

        if not lang_examples:
            # Language has no slot-combination examples yet (not migrated).
            continue

        languages_reported += 1
        print(f"\n=== {language} ===")
        print(
            f"{lang_examples} examples: "
            f"{lang_examples - len(problems) - lang_no_span} highlighted, "
            f"{lang_no_span} no slot to highlight, "
            f"{len(problems)} problem(s)"
        )
        if problems:
            width = max(len(f"{p[0]}/{p[1]}") for p in problems)
            for intent_name, combo_name, example, reason in problems:
                location = f"{intent_name}/{combo_name}"
                print(f"  {location:<{width}}  [{reason}]  {example!r}")

    print(
        f"\nTotal: {total_examples} examples across {languages_reported} language(s) "
        f"with examples — {total_no_match} no match, "
        f"{total_wrong_intent} wrong intent, "
        f"{total_no_span} with no highlightable slot."
    )

    return 0
