"""
Generates a JSON file listing the slot combinations that are still missing for
every language.

For each language, a combination declared in intents.yaml is considered missing
if there is no sentences/<lang>/<intent>/<combo>.yaml file with a non-empty
"data" block. The output is structured so that a future agent can pick a
language, see exactly which combinations are unimplemented, and knows the file
to create (with the canonical English example and the slots involved).
"""

import argparse
import json
import sys
from pathlib import Path

import yaml

SCRIPT_DIR = Path(__file__).parent
INTENTS_DIR = SCRIPT_DIR.parent
SENTENCE_DIR = INTENTS_DIR / "sentences"
INTENTS_FILE = INTENTS_DIR / "intents.yaml"
LANGUAGES_FILE = INTENTS_DIR / "languages.yaml"


def _first_example(example):
    """Normalize an intents.yaml example (str or list) to a single string."""
    if isinstance(example, list):
        return example[0] if example else None
    return example


def _is_required(combo_info: dict) -> bool:
    """A slot combination is required if its importance is required, or any of
    its name/inferred domains are required (matches validation rules)."""
    if combo_info.get("importance") == "required":
        return True
    name_domains = combo_info.get("name_domains") or {}
    inferred_domains = combo_info.get("inferred_domains") or {}
    return ("required" in name_domains) or ("required" in inferred_domains)


def _is_supported(language: str, intent_name: str, combo_name: str) -> bool:
    """A combination is supported if its sentence file exists and has data."""
    combo_path = SENTENCE_DIR / language / intent_name / f"{combo_name}.yaml"
    if not combo_path.exists():
        return False
    combo_data = yaml.safe_load(combo_path.read_text()) or {}
    return bool(combo_data.get("data"))


def main() -> None:
    """Writes missing slot combinations JSON to stdout."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--language", help="Only generate output for one language (debugging)"
    )
    args = parser.parse_args()

    intent_info = yaml.safe_load(INTENTS_FILE.read_text())
    language_info = yaml.safe_load(LANGUAGES_FILE.read_text())

    # Slot combinations declared in intents.yaml, per intent (sorted for stable
    # output). Each entry carries everything needed to author the sentence file.
    declared_combos = []
    for intent_name, info in sorted(intent_info.items()):
        slot_combinations = info.get("slot_combinations") or {}
        for combo_name, combo_info in slot_combinations.items():
            declared_combos.append(
                {
                    "intent": intent_name,
                    "combo": combo_name,
                    "required": _is_required(combo_info),
                    "slots": combo_info.get("slots", []),
                    "description": combo_info.get("description"),
                    "example": _first_example(combo_info.get("example")),
                }
            )

    languages = sorted(p.name for p in SENTENCE_DIR.iterdir() if p.is_dir())

    languages_out = {}
    for language in languages:
        if args.language and (language != args.language):
            continue

        missing = []
        for combo in declared_combos:
            if _is_supported(language, combo["intent"], combo["combo"]):
                continue
            missing.append(
                {
                    "intent": combo["intent"],
                    "combo": combo["combo"],
                    "required": combo["required"],
                    "slots": combo["slots"],
                    "description": combo["description"],
                    "example": combo["example"],
                    "expected_file": (
                        f"sentences/{language}/{combo['intent']}/{combo['combo']}.yaml"
                    ),
                }
            )

        languages_out[language] = {
            "native_name": language_info.get(language, {}).get("nativeName", language),
            "missing_required_count": sum(1 for m in missing if m["required"]),
            "missing_total_count": len(missing),
            "missing": missing,
        }

    output = {
        "description": (
            "Slot combinations declared in intents.yaml that are not yet "
            "implemented for each language. For each entry, create the file at "
            "'expected_file' with a 'data' block containing sentences (and "
            "responses/expansion rules as needed) covering the listed slots. "
            "Use 'example' (canonical English) and 'description' as guidance for "
            "the meaning of the combination. 'required' entries are the "
            "highest-priority must-haves."
        ),
        "total_declared_combinations": len(declared_combos),
        "languages": languages_out,
    }

    json.dump(output, sys.stdout, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
