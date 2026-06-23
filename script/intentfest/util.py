"""Translation utils."""

import argparse

import yaml
from hassil import merge_dict

from .const import RESPONSE_DIR, SENTENCE_DIR


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
            "check_slot_combinations",
            "codeowners",
            "count_sentences",
            "language_table",
            "llm_template",
            "merged_output",
            "migrate_common",
            "migrate_language",
            "parse",
            "report_unparsed_examples",
            "sample_template",
            "sample",
            "slot_combination_summary",
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


def load_merged_responses(language: str) -> dict:
    merged_responses: dict = {}
    for response_file in (RESPONSE_DIR / language).glob("*.yaml"):
        merge_dict(merged_responses, yaml.safe_load(response_file.read_text()))
    return merged_responses
