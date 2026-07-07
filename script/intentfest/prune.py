"""Final cleanup step of a language migration: prune dead rules/lists/responses.

A language migration copies *everything* out of ``_common.yaml`` into
``rules/<lang>/`` and ``lists/<lang>/``, and inlines the slot rules per intent.
Once a language is fully migrated, a lot of that copied weight is
dead: rules no live sentence (or live rule) references, value lists nothing
references, and response keys no sentence group's ``response:`` points at.

    python3 -m script.intentfest prune --language <lang> [--write] [--check]

Default is a dry-run report. With ``--write`` the dead rules/lists are removed from
their files (deleting a file that becomes empty), preserving formatting via
``YamlDumper``; add ``--prune-responses`` to
also drop orphaned response keys (the ``default`` key is never auto-removed — it is
commonly retained for custom sentences). With ``--check`` the tool exits **1** if
any dead rule or dead list exists (a CI gate to keep migrations free of dead
weight); orphaned response keys are reported but do not fail the gate. Builds the
liveness graph carefully: a rule/list is live only if a sentence — or another
*live* rule — references it (a rule used only by another dead rule is itself dead).
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple

import yaml

from .const import LIST_DIR, RESPONSE_DIR, RULE_DIR, SENTENCE_DIR
from .util import YamlDumper, get_base_arg_parser

# Unicode-aware reference patterns: \w matches accented letters in Python 3, so
# names like `añadir`/`habitación` are caught. Do NOT narrow these to ASCII.
RULE_REF_RE = re.compile(r"<(\w+)>")
LIST_REF_RE = re.compile(r"\{(\w+)(?::\w+)?\}")


def get_arguments() -> argparse.Namespace:
    """Get parsed passed in arguments."""
    parser = get_base_arg_parser()
    parser.add_argument("--language", required=True, help="Language code, e.g. en")
    parser.add_argument(
        "--write",
        action="store_true",
        help="Remove dead rules/lists from their files (default: dry-run report).",
    )
    parser.add_argument(
        "--prune-responses",
        action="store_true",
        help="With --write, also remove orphaned response keys (except `default`).",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit 1 if any dead rule/list exists (CI gate); implies a dry run.",
    )
    return parser.parse_known_args()[0]


def run() -> int:
    """Run function."""
    args = get_arguments()
    language = args.language

    # Pruning is only valid once a language is FULLY migrated. While old-format
    # `<domain>_<Intent>.yaml` files remain, their templates still reference rules/
    # lists (resolved from _common.yaml) that this tool's new-format-only liveness
    # graph can't see, and the copied rules/lists are still needed for the intents
    # not yet migrated. So skip partial (and unmigrated) languages instead of
    # reporting false "dead" items.
    if not _is_fully_migrated(language):
        print(
            f"# prune: {language}\n\n"
            f"{language} is not fully migrated yet (old-format sentence files "
            "remain, or no slot-combination intents exist). Pruning is premature "
            "until the migration is complete — skipping."
        )
        return 0

    rule_bodies = _load_named(RULE_DIR / language, "expansion_rules")
    list_names = set(_load_named(LIST_DIR / language, "lists"))

    seed_rules, seed_lists = _collect_sentence_refs(language)

    live_rules, live_lists = _liveness_graph(rule_bodies, seed_rules, seed_lists)

    dead_rules = sorted(set(rule_bodies) - live_rules)
    dead_lists = sorted(list_names - live_lists)
    orphans = _orphaned_responses(language)

    _report(language, dead_rules, dead_lists, orphans)

    if args.write and not args.check:
        _write_changes(language, dead_rules, dead_lists, orphans, args.prune_responses)

    if args.check:
        if dead_rules or dead_lists:
            print(
                f"\n[FAIL] {language}: {len(dead_rules)} dead rule(s) and "
                f"{len(dead_lists)} dead list(s) can be pruned — run "
                f"`python3 -m script.intentfest prune --language {language} --write`."
            )
            return 1
        print(f"\n[OK] {language}: no dead rules/lists.")

    return 0


# -----------------------------------------------------------------------------
# Liveness graph
# -----------------------------------------------------------------------------


def _liveness_graph(
    rule_bodies: Dict[str, str],
    seed_rules: Set[str],
    seed_lists: Set[str],
) -> Tuple[Set[str], Set[str]]:
    """Resolve which rules/lists are live.

    A rule is live if a sentence references it, or another *live* rule's body
    references it. We start from the sentence-seeded rules and expand transitively
    through live rule bodies only — a rule reached solely via a dead rule never
    enters the worklist, so it stays dead.
    """
    live_rules: Set[str] = set()
    live_lists: Set[str] = set(seed_lists)

    # Only rules that actually exist can be "live" (and propagate). A sentence may
    # reference a rule that no longer exists; that is a dangling ref, not our job.
    queue = [name for name in seed_rules if name in rule_bodies]
    while queue:
        name = queue.pop()
        if name in live_rules:
            continue
        live_rules.add(name)
        body = str(rule_bodies[name])
        # Lists referenced by a live rule body are themselves live.
        live_lists.update(LIST_REF_RE.findall(body))
        # Rules referenced by a live rule body become live (and propagate).
        for ref in RULE_REF_RE.findall(body):
            if ref in rule_bodies and ref not in live_rules:
                queue.append(ref)

    return live_rules, live_lists


def _collect_sentence_refs(language: str) -> Tuple[Set[str], Set[str]]:
    """Collect every <rule> and {list} ref appearing in this language's templates."""
    rules: Set[str] = set()
    lists: Set[str] = set()
    language_dir = SENTENCE_DIR / language
    if not language_dir.is_dir():
        return rules, lists

    for intent_dir in sorted(p for p in language_dir.iterdir() if p.is_dir()):
        for combo_file in sorted(intent_dir.glob("*.yaml")):
            doc = yaml.safe_load(combo_file.read_text(encoding="utf-8")) or {}
            for sentence_set in doc.get("data") or []:
                for sentence in sentence_set.get("sentences") or []:
                    text = str(sentence)
                    rules.update(RULE_REF_RE.findall(text))
                    lists.update(LIST_REF_RE.findall(text))
    return rules, lists


# -----------------------------------------------------------------------------
# Orphaned response keys
# -----------------------------------------------------------------------------


def _orphaned_responses(language: str) -> Dict[str, List[str]]:
    """Map each migrated intent to its orphaned response keys (incl. `default`).

    A response key is orphaned if no sentence group's ``response:`` references it.
    ``default`` is reported but flagged as often-intentional by the caller.
    """
    orphans: Dict[str, List[str]] = {}
    response_dir = RESPONSE_DIR / language
    if not response_dir.is_dir():
        return orphans

    sentence_dir = SENTENCE_DIR / language
    for response_file in sorted(response_dir.glob("*.yaml")):
        intent = response_file.stem
        doc = yaml.safe_load(response_file.read_text(encoding="utf-8")) or {}
        defined = doc.get("responses", {}).get("intents", {}).get(intent, {})
        if not isinstance(defined, dict) or not defined:
            continue

        # Only consider intents that are actually migrated (have a sentence dir).
        intent_sentence_dir = sentence_dir / intent
        if not intent_sentence_dir.is_dir():
            continue

        used = _collect_used_responses(intent_sentence_dir)
        dead_keys = sorted(key for key in defined if key not in used)
        if dead_keys:
            orphans[intent] = dead_keys
    return orphans


def _collect_used_responses(intent_sentence_dir: Path) -> Set[str]:
    """Collect every `response:` value referenced by an intent's sentence groups."""
    used: Set[str] = set()
    for combo_file in sorted(intent_sentence_dir.glob("*.yaml")):
        doc = yaml.safe_load(combo_file.read_text(encoding="utf-8")) or {}
        for sentence_set in doc.get("data") or []:
            response = sentence_set.get("response")
            if response is not None:
                used.add(str(response))
    return used


# -----------------------------------------------------------------------------
# Reporting
# -----------------------------------------------------------------------------


def _report(
    language: str,
    dead_rules: List[str],
    dead_lists: List[str],
    orphans: Dict[str, List[str]],
) -> None:
    print(f"# prune: {language}\n")

    print(f"Dead rules ({len(dead_rules)}):")
    for name in dead_rules:
        print(f"  - <{name}>")

    print(f"\nDead lists ({len(dead_lists)}):")
    for name in dead_lists:
        print(f"  - {{{name}}}")

    orphan_count = sum(len(keys) for keys in orphans.values())
    print(f"\nOrphaned response keys ({orphan_count}):")
    for intent in sorted(orphans):
        for key in orphans[intent]:
            note = " (often intentional)" if key == "default" else ""
            print(f"  - {intent}.{key}{note}")

    total = len(dead_rules) + len(dead_lists) + orphan_count
    print(f"\nTotal dead items: {total}")


# -----------------------------------------------------------------------------
# Writing
# -----------------------------------------------------------------------------


def _write_changes(
    language: str,
    dead_rules: List[str],
    dead_lists: List[str],
    orphans: Dict[str, List[str]],
    prune_responses: bool,
) -> None:
    print("\n# Removing dead items (--write):\n")
    _prune_named(RULE_DIR / language, "expansion_rules", set(dead_rules), "<{}>")
    _prune_named(LIST_DIR / language, "lists", set(dead_lists), "{{{}}}")
    if prune_responses:
        _prune_responses(language, orphans)


def _prune_named(directory: Path, key: str, dead: Set[str], fmt: str) -> None:
    """Remove dead names from every file under ``directory``, deleting empties."""
    if not dead or not directory.is_dir():
        return
    for path in sorted(directory.glob("*.yaml")):
        doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        section = doc.get(key)
        if not isinstance(section, dict):
            continue
        removed = [name for name in list(section) if name in dead]
        if not removed:
            continue
        for name in removed:
            del section[name]
            print(f"  - removed {fmt.format(name)} from {path}")
        if section:
            _write_yaml(path, doc)
        else:
            path.unlink()
            print(f"  - deleted empty {path}")


def _prune_responses(language: str, orphans: Dict[str, List[str]]) -> None:
    response_dir = RESPONSE_DIR / language
    for intent in sorted(orphans):
        # Never auto-remove `default` — it is commonly retained intentionally.
        to_remove = [key for key in orphans[intent] if key != "default"]
        if not to_remove:
            continue
        path = response_dir / f"{intent}.yaml"
        doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        defined = doc.get("responses", {}).get("intents", {}).get(intent, {})
        if not isinstance(defined, dict):
            continue
        for key in to_remove:
            if key in defined:
                del defined[key]
                print(f"  - removed {intent}.{key} from {path}")
        _write_yaml(path, doc)


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------


def _is_fully_migrated(language: str) -> bool:
    """True if the language has slot-combination intents and no old-format files.

    Old-format files are the flat ``sentences/<lang>/<domain>_<Intent>.yaml`` files
    (everything except ``_common.yaml``); slot-combination intents live in
    per-intent subdirectories.
    """
    language_dir = SENTENCE_DIR / language
    if not language_dir.is_dir():
        return False
    has_combo_dir = any(p.is_dir() for p in language_dir.iterdir())
    has_old_format = any(
        p.is_file() and p.name != "_common.yaml" for p in language_dir.glob("*.yaml")
    )
    return has_combo_dir and not has_old_format


def _load_named(directory: Path, key: str) -> Dict[str, str]:
    """Map each rule/list name in a directory to its body (merging all files)."""
    mapping: Dict[str, str] = {}
    if not directory.is_dir():
        return mapping
    for path in sorted(directory.glob("*.yaml")):
        doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        for name, body in (doc.get(key) or {}).items():
            mapping[name] = body
    return mapping


def _write_yaml(path: Path, doc: dict) -> Path:
    """Write YAML preserving formatting."""
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
