"""Generate codeowners."""

from __future__ import annotations

import argparse

import yaml

from .const import LANGUAGES_FILE, ROOT
from .util import get_base_arg_parser

CODEOWNERS_FILE = ROOT / "CODEOWNERS"


def get_arguments() -> argparse.Namespace:
    """Get parsed passed in arguments."""
    parser = get_base_arg_parser()
    parser.add_argument(
        "--check",
        required=False,
        action="store_true",
        help="Check if the file is correct format instead of writing it.",
    )
    return parser.parse_args()


def run() -> int:
    args = get_arguments()

    if not args.check:
        write_codeowners()
        return 0

    if not is_codeowners_correct():
        print("Codeowners file is not up to date")
        print("Update with: python3 -m script.intentfest codeowners")
        return 1

    return 0


def is_codeowners_correct() -> bool:
    """Check if the codeowners file is up to date."""
    return CODEOWNERS_FILE.read_text() == _generate_codeowners()


def write_codeowners() -> None:
    """Write the codeowners file."""
    CODEOWNERS_FILE.write_text(_generate_codeowners())


def _generate_codeowners():
    """Generate the text of the CODEOWNERS file."""
    languages = yaml.safe_load(LANGUAGES_FILE.read_text())

    # Files that apply to every language at once, so they are owned by the core
    # team rather than by any language's leaders. The guard_core_files workflow
    # is what actually blocks the change; this entry only routes the review.
    #
    # @OHF-Voice/admin is deliberately absent: CODEOWNERS rejects secret teams
    # with "Unknown owner", and admins can approve without being asked anyway.
    # The guard still allows them, since it checks the repository role rather
    # than team membership.
    parts = [
        "# Shared across all languages: reviewed by the core team.",
        "/intents.yaml @OHF-Voice/voice-ohf",
        "",
    ]

    for language, info in languages.items():
        if not info.get("leaders"):
            continue

        leaders = " ".join(f"@{leader}" for leader in sorted(info["leaders"]))
        parts.extend(
            [
                f"sentences/{language}/ {leaders}",
                f"responses/{language}/ {leaders}",
                f"tests/{language}/ {leaders}",
                f"rules/{language}/ {leaders}",
                f"lists/{language}/ {leaders}",
                "",
            ]
        )

    return "\n".join(parts)
