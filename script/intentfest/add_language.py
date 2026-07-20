"""Script to add a new language."""

import argparse

import yaml

from .const import LANGUAGES_FILE, RESPONSE_DIR, ROOT, SENTENCE_DIR, TESTS_DIR
from .util import YamlDumper, get_base_arg_parser


def get_arguments() -> argparse.Namespace:
    """Get parsed passed in arguments."""
    parser = get_base_arg_parser()
    parser.add_argument(
        "language",
        type=str,
        help="ISO 639 code of the language.",
    )
    parser.add_argument(
        "native_name",
        type=str,
        help="Name of the language in its own language.",
    )
    parser.add_argument(
        "--rtl",
        action="store_true",
        help="Specify if the language is right-to-left.",
    )
    return parser.parse_args()


def run() -> int:
    args = get_arguments()

    language = args.language

    def yaml_dump(obj: object) -> str:
        """Dump YAML for `obj` with consistent options and return a string."""
        return yaml.dump(obj, sort_keys=False, allow_unicode=True, Dumper=YamlDumper)

    # Create language directory
    sentence_dir = SENTENCE_DIR / language
    tests_dir = TESTS_DIR / language
    response_dir = RESPONSE_DIR / language

    try:
        sentence_dir.mkdir()
        response_dir.mkdir()
        tests_dir.mkdir()
    except FileExistsError:
        print(f"Language '{language}' already exists")
        return 1

    # Create sentence files based off English. Sentences live in the
    # per-slot-combination format: sentences/<lang>/<Intent>/<combo>.yaml. Each
    # English combo file is copied with its sentence lists emptied — the
    # language-independent scaffolding (slots, name/inferred domains, response
    # keys, and the example hint) is kept for the translator to work from.
    english_sentences = SENTENCE_DIR / "en"

    for intent_dir in sorted(p for p in english_sentences.iterdir() if p.is_dir()):
        target_intent_dir = sentence_dir / intent_dir.name
        target_intent_dir.mkdir(parents=True, exist_ok=True)

        for combo_file in sorted(intent_dir.glob("*.yaml")):
            combo = yaml.safe_load(combo_file.read_text(encoding="utf-8")) or {}
            combo["language"] = language
            for sentence_info in combo.get("data", []):
                sentence_info["sentences"] = []

            (target_intent_dir / combo_file.name).write_text(yaml_dump(combo))

    (sentence_dir / "_common.yaml").write_text(
        yaml_dump(
            {
                "language": language,
                "responses": {
                    "errors": {
                        # General errors
                        "no_intent": "TODO Sorry, I couldn't understand that",
                        "handle_error": "TODO An unexpected error occurred",
                        # Errors for when user is not logged in
                        "no_area": "TODO Sorry, I am not aware of any area called {{ area }}",
                        "no_floor": "TODO: Sorry, I am not aware of any floor called {{ floor }}",
                        "no_domain": "TODO Sorry, I am not aware of any {{ domain }}",
                        "no_domain_in_area": "TODO Sorry, I am not aware of any {{ domain }} in the {{ area }} area",
                        "no_domain_in_floor": "TODO: Sorry, I am not aware of any {{ domain }} on the {{ floor }} floor",
                        "no_device_class": "TODO Sorry, I am not aware of any {{ device_class }}",
                        "no_device_class_in_area": "TODO Sorry, I am not aware of any {{ device_class }} in the {{ area }} area",
                        "no_device_class_in_floor": "TODO: Sorry, I am not aware of any {{ device_class }} in the {{ floor }} floor",
                        "no_entity": "TODO Sorry, I am not aware of any device called {{ entity }}",
                        "no_entity_in_area": "TODO Sorry, I am not aware of any device called {{ entity }} in the {{ area }} area",
                        "no_entity_in_floor": "TODO: Sorry, I am not aware of any device called {{ entity }} in the {{ floor }} floor",
                        "entity_wrong_state": "TODO: Sorry, no device is {{ state | lower }}",
                        "feature_not_supported": "TODO: Sorry, no device supports the required features",
                        # Errors for when user is logged in and we can give more information
                        "no_entity_exposed": "TODO Sorry, {{ entity }} is not exposed",
                        "no_entity_in_area_exposed": "TODO Sorry, {{ entity }} in the {{ area }} area is not exposed",
                        "no_entity_in_floor_exposed": "TODO: Sorry, {{ entity }} in the {{ floor }} floor is not exposed",
                        "no_domain_exposed": "TODO Sorry, no {{ domain }} is exposed",
                        "no_domain_in_area_exposed": "TODO Sorry, no {{ domain }} in the {{ area }} area is exposed",
                        "no_domain_in_floor_exposed": "TODO: Sorry, no {{ domain }} in the {{ floor }} floor is exposed",
                        "no_device_class_exposed": "TODO Sorry, no {{ device_class }} is exposed",
                        "no_device_class_in_area_exposed": "TODO Sorry, no {{ device_class }} in the {{ area }} area is exposed",
                        "no_device_class_in_floor_exposed": "TODO: Sorry, no {{ device_class }} in the {{ floor }} floor is exposed",
                        # Used when multiple (exposed) devices have the same name
                        "duplicate_entities": "TODO Sorry, there are multiple devices called {{ entity }}",
                        "duplicate_entities_in_area": "TODO Sorry, there are multiple devices called {{ entity }} in the {{ area }} area",
                        "duplicate_entities_in_floor": "TODO: Sorry, there are multiple devices called {{ entity }} in the {{ floor }} floor",
                        # Errors for timers
                        "timer_not_found": "TODO: Sorry, I couldn't find that timer",
                        "multiple_timers_matched": "TODO: Sorry, I am unable to target multiple timers",
                        "no_timer_support": "TODO: Sorry, timers are not supported on this device",
                    },
                },
                "lists": {},
                "expansion_rules": {},
                "skip_words": [],
            },
        )
    )

    # Create tests files based off English. Tests mirror the sentence layout:
    # tests/<lang>/<Intent>/<combo>.yaml. Each English test file is copied with
    # its test sentences emptied — the entities/areas/floors fixtures, expected
    # slots and rendered responses stay as a reference for the translator to
    # localize.
    english_tests = TESTS_DIR / "en"

    for intent_dir in sorted(p for p in english_tests.iterdir() if p.is_dir()):
        target_intent_dir = tests_dir / intent_dir.name
        target_intent_dir.mkdir(parents=True, exist_ok=True)

        for combo_file in sorted(intent_dir.glob("*.yaml")):
            combo = yaml.safe_load(combo_file.read_text(encoding="utf-8")) or {}
            combo["language"] = language
            for test_group in combo.get("tests", []):
                test_group["sentences"] = []

            (target_intent_dir / combo_file.name).write_text(yaml_dump(combo))

    # Copy the fixtures (areas/floors/entities) as a starting point.
    fixtures = yaml.safe_load(
        (english_tests / "_fixtures.yaml").read_text(encoding="utf-8")
    )
    fixtures["language"] = language
    (tests_dir / "_fixtures.yaml").write_text(yaml_dump(fixtures))

    # Create response files based off English
    english_responses = RESPONSE_DIR / "en"

    for english_filename in english_responses.glob("*.yaml"):
        with open(english_filename, "r", encoding="utf-8") as english_file:
            responses = yaml.safe_load(english_file)["responses"]

        # Mark responses as needing translation
        for intent_responses in responses["intents"].values():
            for response_key, response_text in intent_responses.items():
                intent_responses[response_key] = f"TODO: {response_text}"

        (response_dir / english_filename.name).write_text(
            yaml_dump(
                {
                    "language": language,
                    "responses": responses,
                },
            )
        )

    # Update languages.yaml
    languages = yaml.safe_load(LANGUAGES_FILE.read_text(encoding="utf-8"))
    languages[language] = {
        "nativeName": args.native_name,
    }
    if args.rtl:
        languages[language]["isRTL"] = True

    LANGUAGES_FILE.write_text(
        yaml_dump(
            # Sort the languages by code.
            dict(sorted(languages.items())),
        )
    )

    rel_sentence_dir = sentence_dir.relative_to(ROOT)
    rel_test_dir = tests_dir.relative_to(ROOT)

    print()
    print(f"Language '{language}' added!")
    print()
    print("See the README.md files in the sentences, responses and tests dir ")
    print("for the formats. Use the English files as examples.")
    print()
    print()
    print("New folders added:")
    print()
    print(f"{rel_sentence_dir} - Sentences")
    print(f"{response_dir.relative_to(ROOT)} - Responses")
    print(f"{rel_test_dir} - Tests")
    print()
    print()
    print("Limit your first contribution to:")
    print()
    print(
        f"{rel_sentence_dir / '_common.yaml'} - Update error strings and add skip words"
    )
    print()
    print(
        f"{rel_sentence_dir / 'HassTurnOn' / 'name_only.yaml'} - Add some basic sentences"
    )
    print(
        f"{rel_sentence_dir / 'HassTurnOff' / 'name_only.yaml'} - Add some basic sentences"
    )
    print()
    print(f"{rel_test_dir / 'HassTurnOn' / 'name_only.yaml'} - Add test sentences")
    print(f"{rel_test_dir / 'HassTurnOff' / 'name_only.yaml'} - Add test sentences")

    return 0
