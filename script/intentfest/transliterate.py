"""Generate a transliterated language from a script-sharing source language.

Some languages are identical in content to another language but written in a
different script (e.g. ``sr`` is Serbian Cyrillic and ``sr-Latn`` is the same
language in Latin script). Rather than hand-maintaining both, ``sr-Latn`` (and
any future pair registered in ``TRANSLITERATIONS``) is fully generated from its
source language's ``sentences/``, ``responses/``, ``tests/``, ``rules/`` and
``lists/`` directories.

    python3 -m script.intentfest transliterate [--check]

Default regenerates the target language directories from the source language,
deleting any stale/hand-edited content in the target first. With ``--check``,
the same content is generated in-memory and compared against what's on disk;
the tool exits 1 on any mismatch (a CI gate that also catches direct edits to
the generated language, which should only ever be made in the source).
"""

from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path
from typing import Callable, Dict

from .const import LIST_DIR, RESPONSE_DIR, ROOT, RULE_DIR, SENTENCE_DIR, TESTS_DIR
from .util import get_base_arg_parser

# -----------------------------------------------------------------------------
# Serbian Cyrillic -> Latin
# -----------------------------------------------------------------------------

# Single-character mappings (lowercase; uppercase is derived below).
_SR_SINGLE_LOWER = {
    "а": "a",
    "б": "b",
    "в": "v",
    "г": "g",
    "д": "d",
    "ђ": "đ",
    "е": "e",
    "ж": "ž",
    "з": "z",
    "и": "i",
    "ј": "j",
    "к": "k",
    "л": "l",
    "м": "m",
    "н": "n",
    "о": "o",
    "п": "p",
    "р": "r",
    "с": "s",
    "т": "t",
    "ћ": "ć",
    "у": "u",
    "ф": "f",
    "х": "h",
    "ц": "c",
    "ч": "č",
    "ш": "š",
}
_SR_SINGLE = {
    **_SR_SINGLE_LOWER,
    **{k.upper(): v.upper() for k, v in _SR_SINGLE_LOWER.items()},
}

# љ/њ/џ are digraphs in Latin. Lowercase is always the lowercase digraph;
# uppercase is Title-case (`Nj`) mid/start-of-word but ALL-CAPS (`NJ`) when the
# rest of the word is also capitalized (decided by looking at the next char).
_SR_DIGRAPH_LOWER = {"љ": "lj", "њ": "nj", "џ": "dž"}
_SR_DIGRAPH_TITLE = {"Љ": "Lj", "Њ": "Nj", "Џ": "Dž"}
_SR_DIGRAPH_UPPER = {"Љ": "LJ", "Њ": "NJ", "Џ": "DŽ"}
_SR_LOWER_LETTERS = set(_SR_SINGLE_LOWER) | set(_SR_DIGRAPH_LOWER)


def _transliterate_sr(text: str) -> str:
    """Transliterate Serbian Cyrillic text to Latin script."""
    chars = []
    length = len(text)
    for i, char in enumerate(text):
        if char in _SR_DIGRAPH_LOWER:
            chars.append(_SR_DIGRAPH_LOWER[char])
        elif char in _SR_DIGRAPH_TITLE:
            next_char = text[i + 1] if i + 1 < length else ""
            if next_char in _SR_LOWER_LETTERS:
                chars.append(_SR_DIGRAPH_TITLE[char])
            else:
                chars.append(_SR_DIGRAPH_UPPER[char])
        else:
            chars.append(_SR_SINGLE.get(char, char))
    return "".join(chars)


# -----------------------------------------------------------------------------
# Registry: source language -> (target language, transliterator)
# -----------------------------------------------------------------------------

TRANSLITERATIONS: Dict[str, "tuple[str, Callable[[str], str]]"] = {
    "sr": ("sr-Latn", _transliterate_sr),
}

# Directories mirrored/transliterated for each pair. Not every language has
# rules/lists (only migrated ones do), so missing source dirs are skipped.
_LANGUAGE_DIRS = (SENTENCE_DIR, RESPONSE_DIR, TESTS_DIR, RULE_DIR, LIST_DIR)


def get_arguments() -> argparse.Namespace:
    """Get parsed passed in arguments."""
    parser = get_base_arg_parser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit 1 if generated content doesn't match what's on disk (CI gate).",
    )
    return parser.parse_known_args()[0]


def run() -> int:
    """Run function."""
    args = get_arguments()

    ok = True
    for source_lang, (target_lang, translit_fn) in TRANSLITERATIONS.items():
        generated = _generate_all(source_lang, target_lang, translit_fn)
        if args.check:
            ok = _check(target_lang, generated) and ok
        else:
            _write(target_lang, generated)
            print(f"Regenerated {target_lang} from {source_lang}.")

    return 0 if ok else 1


# -----------------------------------------------------------------------------
# Generation
# -----------------------------------------------------------------------------


def _generate_all(
    source_lang: str, target_lang: str, translit_fn: Callable[[str], str]
) -> Dict[Path, str]:
    """Map every generated file's absolute path to its transliterated content."""
    generated: Dict[Path, str] = {}
    language_line_re = re.compile(
        rf'^(language:\s*"?){re.escape(source_lang)}("?\s*)$', re.MULTILINE
    )

    for base_dir in _LANGUAGE_DIRS:
        source_dir = base_dir / source_lang
        if not source_dir.is_dir():
            continue
        target_dir = base_dir / target_lang
        for source_path in sorted(source_dir.rglob("*.yaml")):
            text = translit_fn(source_path.read_text(encoding="utf-8"))
            text = language_line_re.sub(rf"\g<1>{target_lang}\g<2>", text)
            relative = source_path.relative_to(source_dir)
            generated[target_dir / relative] = text

    return generated


# -----------------------------------------------------------------------------
# Write / check
# -----------------------------------------------------------------------------


def _write(target_lang: str, generated: Dict[Path, str]) -> None:
    """Replace every generated directory for target_lang with fresh content."""
    for base_dir in _LANGUAGE_DIRS:
        target_dir = base_dir / target_lang
        if target_dir.is_dir():
            shutil.rmtree(target_dir)

    for path, text in generated.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")


def _check(target_lang: str, generated: Dict[Path, str]) -> bool:
    """Compare generated content against what's committed for target_lang."""
    existing: Dict[Path, str] = {}
    for base_dir in _LANGUAGE_DIRS:
        target_dir = base_dir / target_lang
        if not target_dir.is_dir():
            continue
        for path in target_dir.rglob("*.yaml"):
            existing[path] = path.read_text(encoding="utf-8")

    missing = sorted(p for p in generated if p not in existing)
    extra = sorted(p for p in existing if p not in generated)
    changed = sorted(
        p for p in generated if p in existing and existing[p] != generated[p]
    )

    if not missing and not extra and not changed:
        print(f"[OK] {target_lang}: matches transliteration of its source.")
        return True

    print(f"[FAIL] {target_lang} is out of date with its source language.")
    for path in missing:
        print(f"  - missing: {path.relative_to(ROOT)}")
    for path in extra:
        print(f"  - stale (should not exist): {path.relative_to(ROOT)}")
    for path in changed:
        print(f"  - outdated content: {path.relative_to(ROOT)}")
    print("Regenerate with: python3 -m script.intentfest transliterate")
    return False
