"""Step 0 of a language migration: copy lists/rules out of ``_common.yaml``.

The slot-combination format resolves expansion rules from ``rules/<lang>/`` and
lists from ``lists/`` and ``lists/<lang>/`` — never from
``sentences/<lang>/_common.yaml``. So before migrating a language's intents, the
shared rules and lists must be **copied** into those locations.

This is a *copy*, not a move: the old ``_common.yaml`` is left untouched so the
not-yet-migrated old-format sentence files keep resolving their rules/lists. Once
every intent for the language is migrated, the now-unused blocks in
``_common.yaml`` can be deleted (see docs/syntax_migration_guide.md).

    python3 -m script.intentfest migrate_common --language <lang>

Grouping mirrors ``rules/en/`` / ``lists/en/`` where a name matches, and falls
back to a keyword heuristic otherwise. Grouping is purely organizational — the
test harness merges every file in ``rules/<lang>/`` — so the output is safe to
re-group by hand afterwards. Range/wildcard lists that already exist as shared
top-level ``lists/*.yaml`` are skipped (they are language-independent).
"""

from __future__ import annotations

import argparse
import re
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import voluptuous as vol
import yaml

from .const import LIST_DIR, RULE_DIR, SENTENCE_DIR
from .util import YamlDumper, get_base_arg_parser
from .validate import no_list_or_rule_references, not_optional

# Keyword -> group file, used when a name isn't already grouped by en.
KEYWORD_GROUPS: List[Tuple[str, str]] = [
    ("timer", "timers"),
    ("brightness", "light"),
    ("color_temp", "light"),
    ("light", "light"),
    ("lamp", "light"),
    ("fan", "fans"),
    ("volume", "media"),
    ("media", "media"),
    ("position", "covers"),
    ("cover", "covers"),
    ("open", "covers"),
    ("close", "covers"),
    ("blind", "covers"),
    ("curtain", "covers"),
    ("shutter", "covers"),
    ("shade", "covers"),
    ("awning", "covers"),
    ("garage", "covers"),
    ("door", "covers"),
    ("gate", "covers"),
    ("window", "covers"),
    ("temp", "climate"),
    ("warm", "climate"),
    ("degree", "climate"),
    ("sensor", "sensors"),
    ("detect", "sensors"),
    ("lock", "lock"),
    ("what_is", "getstate"),
    ("state", "getstate"),
    ("class", "getstate"),
]


def get_arguments() -> argparse.Namespace:
    """Get parsed passed in arguments."""
    parser = get_base_arg_parser()
    parser.add_argument("--language", required=True, help="Language code, e.g. nl")
    parser.add_argument(
        "--force", action="store_true", help="Overwrite existing rules/lists files."
    )
    return parser.parse_known_args()[0]


def run() -> int:
    """Run function."""
    args = get_arguments()
    language = args.language

    common_path = SENTENCE_DIR / language / "_common.yaml"
    if not common_path.exists():
        print(f"No {common_path}")
        return 1

    common = yaml.safe_load(common_path.read_text(encoding="utf-8")) or {}
    rules = common.get("expansion_rules") or {}
    lists = common.get("lists") or {}

    flags: List[str] = []
    written: List[Path] = []

    written += _copy_rules(language, rules, flags, args.force)
    written += _copy_lists(language, lists, flags, args.force)

    print(f"# migrate_common: {language}\n")
    print(f"Wrote {len(written)} file(s):")
    for path in written:
        print(f"  - {path}")
    print(f"\nFlags ({len(flags)}):")
    for flag in flags:
        print(f"  - {flag}")
    print(
        "\nReminder: _common.yaml is left intact (copy, not move). Inline the "
        "flagged list-bearing rules and flatten nested rules in the new files, "
        "then migrate intents. Delete the _common.yaml blocks only once the whole "
        "language is migrated."
    )
    return 0


# -----------------------------------------------------------------------------
# Rules
# -----------------------------------------------------------------------------


def _copy_rules(
    language: str, rules: Dict[str, str], flags: List[str], force: bool
) -> List[Path]:
    if not rules:
        return []

    en_groups = _name_to_stem(RULE_DIR / "en", "expansion_rules")
    grouped: Dict[str, Dict[str, str]] = defaultdict(dict)
    # name -> body for rules skipped because they are fully optional. These are
    # inlined into the copied rules that reference them (see below) so no copied
    # rule is left with a dangling reference to a non-existent rule.
    skipped_optional: Dict[str, str] = {}
    for name, body in rules.items():
        try:
            not_optional(str(body))
        except vol.Invalid:
            skipped_optional[name] = str(body)
            continue

        group = en_groups.get(name) or _keyword_group(name) or "common"
        grouped[group][name] = body

        if re.search(r"\{[^}]+\}", str(body)):
            flags.append(f"rule `<{name}>` references a list — inline it (see §4).")
        if re.search(r"<[^>]+>", str(body)):
            flags.append(f"rule `<{name}>` references another rule — flatten it (§4).")

    # Inline each skipped fully-optional rule into every copied rule body that
    # references it, so the latent break the migration guide warns about (a
    # copied rule referencing a rule that was never copied) cannot happen.
    inlined_into = _inline_optional_rules(grouped, skipped_optional)
    for ref, targets in sorted(inlined_into.items()):
        flags.append(
            f"inlined fully-optional `<{ref}>` into "
            + ", ".join(f"<{name}>" for name in sorted(targets))
            + " (it cannot be a standalone rule in the new format)."
        )
    for name in sorted(set(skipped_optional) - set(inlined_into)):
        flags.append(
            f"rule `<{name}>` is fully optional — cannot be a standalone "
            "rule in the new format; inline it in templates instead."
        )

    # A copied rule that still references a rule that was not copied (and was not
    # an inlinable fully-optional rule, e.g. a nested non-optional rule that got
    # skipped) is a dangling reference: it resolves fine in the old _common.yaml
    # but breaks the moment a new-format sentence reaches it. Flag it.
    copied = {name for group in grouped.values() for name in group}
    for group_rules in grouped.values():
        for name, body in group_rules.items():
            for ref in sorted(set(re.findall(r"<(\w+)>", str(body)))):
                if ref not in copied:
                    flags.append(
                        f"rule `<{name}>` references `<{ref}>`, which was NOT copied "
                        f"into rules/{language}/ (likely skipped as fully-optional) — "
                        f"inline `<{ref}>`, or drop `<{name}>` if no sentence uses it."
                    )

    written: List[Path] = []
    for group, group_rules in sorted(grouped.items()):
        path = RULE_DIR / language / f"{group}.yaml"
        if path.exists() and not force:
            flags.append(f"{path} exists; skipped (use --force).")
            continue
        doc = {"language": language, "expansion_rules": group_rules}
        written.append(_write_yaml(path, doc))
    return written


# -----------------------------------------------------------------------------
# Lists
# -----------------------------------------------------------------------------


def _copy_lists(
    language: str, lists: Dict[str, dict], flags: List[str], force: bool
) -> List[Path]:
    if not lists:
        return []

    shared_names = _name_to_stem(LIST_DIR, "lists")  # top-level shared lists
    en_groups = _name_to_stem(LIST_DIR / "en", "lists")

    grouped: Dict[str, Dict[str, dict]] = defaultdict(dict)
    for name, body in lists.items():
        is_shareable = isinstance(body, dict) and (
            "range" in body or "wildcard" in body
        )
        if is_shareable:
            if name in shared_names:
                flags.append(
                    f"list `{{{name}}}` is already shared in "
                    f"lists/{shared_names[name]}.yaml — skipped (use the shared one)."
                )
                continue
            flags.append(
                f"list `{{{name}}}` is a range/wildcard not yet shared — consider "
                f"adding it to a top-level lists/<group>.yaml instead."
            )

        if isinstance(body, dict) and "values" in body:
            if _values_have_references(body["values"]):
                flags.append(
                    f"list `{{{name}}}` has values containing <rule>/{{list}} "
                    "references, which the new format forbids — inline them first."
                )
                continue

        group = en_groups.get(name) or _keyword_group(name) or "common"
        grouped[group][name] = body

    written: List[Path] = []
    for group, group_lists in sorted(grouped.items()):
        path = LIST_DIR / language / f"{group}.yaml"
        if path.exists() and not force:
            flags.append(f"{path} exists; skipped (use --force).")
            continue
        doc = {"language": language, "lists": group_lists}
        written.append(_write_yaml(path, doc))
    return written


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------


def _wrap_optional_body(body: str) -> str:
    """Return ``body`` safe to splice into another rule body.

    A fully-optional body is already a single bracketed/parenthesised group, so
    it can be spliced as-is. If it is not a single fully-enclosing ``[...]`` or
    ``(...)`` group, wrap it in ``(...)`` so surrounding precedence (e.g. an
    enclosing alternative) cannot change its meaning.
    """
    body = body.strip()
    if _is_single_enclosing_group(body):
        return body
    return f"({body})"


def _is_single_enclosing_group(body: str) -> bool:
    """True if ``body`` is one ``[...]``/``(...)`` group wrapping the whole text."""
    if len(body) < 2 or body[0] not in "[(":
        return False
    closer = "]" if body[0] == "[" else ")"
    depth = 0
    for index, char in enumerate(body):
        if char in "[(":
            depth += 1
        elif char in "])":
            depth -= 1
            if depth == 0:
                # The opening bracket only encloses everything if it closes at
                # the very end of the string.
                return index == len(body) - 1 and char == closer
    return False


def _inline_optional_rules(
    grouped: Dict[str, Dict[str, str]], skipped_optional: Dict[str, str]
) -> Dict[str, set]:
    """Inline skipped fully-optional rules into copied rule bodies in place.

    Substitutes ``<name>`` with the (wrapped) body of each skipped fully-optional
    rule in every grouped rule body that references it. Runs to a fixpoint so a
    chain of optional rules also resolves. Returns a map of
    ``{inlined_rule_name: {target_rule_name, ...}}`` for reporting.
    """
    inlined_into: Dict[str, set] = defaultdict(set)
    if not skipped_optional:
        return {}

    wrapped = {
        name: _wrap_optional_body(body) for name, body in skipped_optional.items()
    }

    # Bounded fixpoint: each pass inlines one more level of optional references.
    for _ in range(len(skipped_optional) + 1):
        changed = False
        for group_rules in grouped.values():
            for name, body in group_rules.items():
                new_body = body
                for ref, replacement in wrapped.items():
                    pattern = re.compile(rf"<{re.escape(ref)}>")
                    if pattern.search(new_body):
                        new_body = pattern.sub(replacement, new_body)
                        inlined_into[ref].add(name)
                if new_body != body:
                    group_rules[name] = new_body
                    changed = True
        if not changed:
            break

    return dict(inlined_into)


def _values_have_references(values: list) -> bool:
    """True if any list value's input text contains a <rule> or {list} reference."""
    for value in values:
        text = value["in"] if isinstance(value, dict) else value
        try:
            no_list_or_rule_references(str(text))
        except vol.Invalid:
            return True
    return False


def _name_to_stem(directory: Path, key: str) -> Dict[str, str]:
    """Map each rule/list name in a directory to the file stem it lives in."""
    mapping: Dict[str, str] = {}
    if not directory.is_dir():
        return mapping
    for path in directory.glob("*.yaml"):
        doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        for name in doc.get(key) or {}:
            mapping[name] = path.stem
    return mapping


def _keyword_group(name: str) -> Optional[str]:
    lowered = name.lower()
    for keyword, group in KEYWORD_GROUPS:
        if keyword in lowered:
            return group
    return None


def _write_yaml(path: Path, doc: dict) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = yaml.dump(
        doc,
        Dumper=YamlDumper,
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
        width=10_000,
    )
    path.write_text(text, encoding="utf-8")
    return path
