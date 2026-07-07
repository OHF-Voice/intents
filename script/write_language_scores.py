"""
Generates a JSON file with scores for each language.
These are based on the languages.yaml file in the intents repo.
"""

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Set, Tuple

import yaml

_LOGGER = logging.getLogger(__name__)


def main() -> None:
    """Writes language scores JSON to stdout."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--language", help="Only generate scores for one language (debugging)"
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    script_dir = Path(__file__).parent
    intents_dir = script_dir.parent

    language_scores = {}

    with open(intents_dir / "languages.yaml", "r", encoding="utf-8") as languages_file:
        languages = yaml.safe_load(languages_file)

    with open(intents_dir / "intents.yaml", "r", encoding="utf-8") as intents_file:
        intents = yaml.safe_load(intents_file)

    required_combos: Set[Tuple[str, str]] = set()
    usable_combos: Set[Tuple[str, str]] = set()
    complete_combos: Set[Tuple[str, str]] = set()

    for intent_name, intent_info in intents.items():
        if not intent_info.get("supported"):
            # Skip intents that are not supported in Home Assistant
            continue

        for combo_name, combo_info in intent_info["slot_combinations"].items():
            importance_levels = set()
            if importance := combo_info.get("importance"):
                importance_levels.add(importance)
            elif name_domains := combo_info.get("name_domains"):
                importance_levels.update(name_domains.keys())
            elif inferred_domains := combo_info.get("inferred_domains"):
                importance_levels.update(inferred_domains.keys())

            combo_key = (intent_name, combo_name)
            if "required" in importance_levels:
                required_combos.add(combo_key)
            elif "usable" in importance_levels:
                usable_combos.add(combo_key)
            elif "complete" in importance_levels:
                complete_combos.add(combo_key)

    for lang_key, lang_info in languages.items():
        if args.language and (lang_key != args.language):
            continue

        if "-" in lang_key:
            # de-CH -> de
            lang_family = lang_key.split("-", maxsplit=1)[0]
        else:
            lang_family = lang_key

        lang_support = lang_info.get("support")
        if not lang_support:
            _LOGGER.warning("Missing support info for language: %s", lang_key)
            continue

        supported_combos: Set[Tuple[str, str]] = set()
        sentences_dir = intents_dir / "sentences" / lang_key

        for combo_yaml_path in sentences_dir.glob("*/*.yaml"):
            intent_name = combo_yaml_path.parent.name
            combo_name = combo_yaml_path.stem
            combo_key = (intent_name, combo_name)
            if combo_key in supported_combos:
                # Already supported
                continue

            with open(combo_yaml_path, "r", encoding="utf-8") as combo_yaml_file:
                combo_yaml = yaml.safe_load(combo_yaml_file)
                for combo_data in combo_yaml.get("data", []):
                    if len(combo_data.get("sentences", [])) > 0:
                        supported_combos.add(combo_key)
                        break

        has_required_intents = required_combos.issubset(supported_combos)
        has_usable_intents = usable_combos.issubset(supported_combos)
        has_complete_intents = complete_combos.issubset(supported_combos)

        if args.language:
            # For debugging
            missing_required_combos = required_combos - supported_combos
            if missing_required_combos:
                _LOGGER.info(
                    "Missing required slot combinations: %s",
                    sorted(missing_required_combos),
                )

            missing_usable_combos = usable_combos - supported_combos
            if missing_usable_combos:
                _LOGGER.info(
                    "Missing usable slot combinations: %s",
                    sorted(missing_usable_combos),
                )

            missing_complete_combos = complete_combos - supported_combos
            if missing_complete_combos:
                _LOGGER.info(
                    "Missing complete slot combinations: %s",
                    sorted(missing_complete_combos),
                )

        for region, region_support in lang_support.items():
            locale = f"{lang_family}-{region}"
            stt = region_support.get("speech-to-text", {})
            tts = region_support.get("text-to-speech", {})

            cloud_score = 0
            focused_local_score = 0
            full_local_score = 0

            if stt.get("cloud") and tts.get("cloud"):
                if has_complete_intents:
                    cloud_score = 3
                elif has_usable_intents:
                    cloud_score = 2
                elif has_required_intents:
                    cloud_score = 1

            if stt.get("speech-to-phrase") and tts.get("piper"):
                if has_complete_intents:
                    focused_local_score = 2  # cannot be perfect
                elif has_usable_intents:
                    focused_local_score = 2
                elif has_required_intents:
                    focused_local_score = 1

            if stt.get("whisper") and tts.get("piper"):
                if has_complete_intents:
                    full_local_score = 3
                elif has_usable_intents:
                    full_local_score = 2
                elif has_required_intents:
                    full_local_score = 1

            language_scores[locale] = {
                "cloud": cloud_score,
                "focused_local": focused_local_score,
                "full_local": full_local_score,
            }

    json.dump(language_scores, sys.stdout, indent=2)


if __name__ == "__main__":
    main()
