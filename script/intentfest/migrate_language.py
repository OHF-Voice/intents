"""Scaffold a per-intent migration to the slot-combination format.

This is a *support tool* for the migration described in
``docs/syntax_migration_guide.md``. It does the deterministic, mechanical part
of migrating a single intent for a single language and emits a flag report that
lists everything that still needs human/AI judgement.

The intended workflow is one (sub-)agent per intent:

1. Run ``python3 -m script.intentfest migrate_language --language <lang> --intent <Intent>``
2. The tool writes scaffold files under ``sentences/<lang>/<Intent>/`` and
   ``tests/<lang>/<Intent>/`` for everything it can map unambiguously, and
   prints a report of what it could not.
3. The agent finishes the flagged items, deletes the old files, and runs
   ``script/intentfest validate`` + the test suite.

The tool never deletes the old ``*_<Intent>.yaml`` files and never touches
``_common.yaml`` (lists/rules), so a half-finished run is always recoverable.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import yaml
from hassil import Intents

from .check_slot_combinations import CONTEXT_AREA_SLOT, _flatten, _get_slots
from .const import INTENTS_FILE, LIST_DIR, RULE_DIR, SENTENCE_DIR, TESTS_DIR
from .util import YamlDumper, get_base_arg_parser

Signature = Tuple[str, ...]

# Slot lists that the test harness always provides from the fixtures, so they
# never need to live in lists/<lang>/.
BUILTIN_LISTS = {"name", "area", "floor"}


@dataclass
class ComboSpec:
    """A single declared slot combination from intents.yaml."""

    name: str
    signature: Signature
    # "name" (name_domains), "inferred" (inferred_domains) or None
    domain_kind: Optional[str]
    domains: Set[str]
    example: Optional[str]
    required: bool


@dataclass
class Flag:
    """Something that needs human/AI attention."""

    category: str
    detail: str


@dataclass
class MigrationResult:
    """Outcome of scaffolding one intent."""

    written: List[Path] = field(default_factory=list)
    flags: List[Flag] = field(default_factory=list)
    # combo name -> list of data entries (dicts ready to render)
    combos: Dict[str, List[dict]] = field(default_factory=dict)
    # rule/list names referenced by the placed sentences
    rule_refs: Set[str] = field(default_factory=set)
    list_refs: Set[str] = field(default_factory=set)


# -----------------------------------------------------------------------------


def get_arguments() -> argparse.Namespace:
    """Get parsed passed in arguments."""
    parser = get_base_arg_parser()
    parser.add_argument("--language", required=True, help="Language code, e.g. nl")
    parser.add_argument("--intent", required=True, help="Intent name, e.g. HassTurnOn")
    parser.add_argument(
        "--report",
        help="Path to write the flag report (default: alongside the intent dir)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing scaffold files if they already exist.",
    )
    return parser.parse_known_args()[0]


def run() -> int:
    """Run function."""
    args = get_arguments()

    intents_yaml = yaml.safe_load(INTENTS_FILE.read_text(encoding="utf-8"))
    intent_info = intents_yaml.get(args.intent)
    if intent_info is None:
        print(f"Unknown intent: {args.intent}")
        return 1

    combos = _build_combo_specs(intent_info)
    if not combos:
        print(f"Intent {args.intent} has no slot_combinations in intents.yaml")
        return 1

    lang_intents = Intents.from_files((SENTENCE_DIR / args.language).glob("*.yaml"))
    intent = lang_intents.intents.get(args.intent)
    if intent is None:
        print(f"Language {args.language} has no sentences for {args.intent}")
        return 1

    result = MigrationResult()
    _migrate_sentences(args, intent, lang_intents, combos, result)
    _migrate_tests(args, combos, result)
    _check_required_coverage(intent_info, result)

    for combo_name in result.combos:
        if not (
            TESTS_DIR / args.language / args.intent / f"{combo_name}.yaml"
        ).exists():
            result.flags.append(
                Flag(
                    "test coverage",
                    f"`{combo_name}` has scaffolded sentences but no test file — "
                    "add a test (old tests may have collapsed into another combo).",
                )
            )

    _check_references_resolve(args.language, result)

    report = _render_report(args, combos, result)
    report_path = (
        Path(args.report)
        if args.report
        else INTENTS_FILE.parent
        / "migration_reports"
        / args.language
        / f"{args.intent}.md"
    )
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding="utf-8")

    print(report)
    print(f"\nWrote {len(result.written)} scaffold file(s).")
    print(f"Report: {report_path}")
    print(f"Flags needing attention: {len(result.flags)}")
    return 0


# -----------------------------------------------------------------------------
# Combo index
# -----------------------------------------------------------------------------


def _build_combo_specs(intent_info: dict) -> List[ComboSpec]:
    specs: List[ComboSpec] = []
    for name, combo in (intent_info.get("slot_combinations") or {}).items():
        slots = combo.get("slots") or []
        if isinstance(slots, str):
            slots = [slots]
        slots = list(slots)
        if combo.get("context_area"):
            slots.append(CONTEXT_AREA_SLOT)

        domain_kind: Optional[str] = None
        domains: Set[str] = set()
        required = combo.get("importance") == "required"
        for key, kind in (("name_domains", "name"), ("inferred_domains", "inferred")):
            block = combo.get(key)
            if block:
                domain_kind = kind
                for importance, importance_list in block.items():
                    domains.update(importance_list)
                    if importance == "required":
                        required = True

        example = combo.get("example")
        if isinstance(example, list):
            example = example[0] if example else None

        specs.append(
            ComboSpec(
                name=name,
                signature=tuple(sorted(slots)),
                domain_kind=domain_kind,
                domains=domains,
                example=example,
                required=required,
            )
        )
    return specs


def _map_combo(
    specs: List[ComboSpec], signature: Signature, domain_values: List[str]
) -> Optional[ComboSpec]:
    """Map a (signature, domain) to a single combo, or None if ambiguous."""
    candidates = [s for s in specs if s.signature == signature]
    if len(candidates) == 1:
        return candidates[0]
    if not candidates:
        return None

    # Disambiguate combos that share a signature (e.g. name_only/name_scene) by
    # which one declares the domain used by the sentence.
    if domain_values:
        matches = [c for c in candidates if c.domains & set(domain_values)]
        if len(matches) == 1:
            return matches[0]
    return None


# -----------------------------------------------------------------------------
# Sentences
# -----------------------------------------------------------------------------


def _signatures_for_sentence(
    expression: Any,
    data: Any,
    lang_intents: Intents,
    auto_slots: Set[str],
    cache: dict,
) -> Set[Signature]:
    slot_options = list(_get_slots(expression, data, lang_intents, cache))
    if not slot_options:
        # No list references in the template: only the auto slots count.
        return {tuple(sorted(auto_slots))}

    signatures: Set[Signature] = set()
    for _has_slot, combo in slot_options:
        extra = set(_flatten(combo)) if combo is not None else set()
        signatures.add(tuple(sorted(auto_slots | extra)))
    return signatures


def _domain_values(data: Any) -> List[str]:
    raw = data.slots.get("domain") if data.slots else None
    if raw is None:
        raw = data.requires_context.get("domain")
    if raw is None:
        return []
    return [raw] if isinstance(raw, str) else list(raw)


def _migrate_sentences(
    args: argparse.Namespace,
    intent: Any,
    lang_intents: Intents,
    combos: List[ComboSpec],
    result: MigrationResult,
) -> None:
    cache: dict = {}
    combo_by_name = {c.name: c for c in combos}

    # combo name -> source group index -> list of sentence strings
    placed: Dict[str, Dict[int, List[str]]] = defaultdict(lambda: defaultdict(list))
    # remember metadata per (combo, group)
    group_meta: Dict[Tuple[str, int], dict] = {}

    for group_index, data in enumerate(intent.data):
        auto_slots: Set[str] = set(data.slots or {})
        # Domain/device_class are matched via context, not as signature slots,
        # when they come from requires_context.
        auto_slots.discard("domain")
        if data.requires_context.get("area", {}).get("slot"):
            auto_slots.add(CONTEXT_AREA_SLOT)

        domain_values = _domain_values(data)

        for sentence in data.sentences:
            signatures = _signatures_for_sentence(
                sentence.expression, data, lang_intents, auto_slots, cache
            )

            mapped = {sig: _map_combo(combos, sig, domain_values) for sig in signatures}
            clean = {sig: c for sig, c in mapped.items() if c is not None}

            if len(signatures) > 1:
                result.flags.append(
                    Flag(
                        "multi-combo template",
                        f"`{sentence.text}` matches "
                        f"{sorted(c.name if c else f'?{list(s)}' for s, c in mapped.items())}"
                        " — split into one template per combo.",
                    )
                )
                continue

            sig = next(iter(signatures))
            combo = clean.get(sig)
            if combo is None:
                result.flags.append(
                    Flag(
                        "unmapped signature",
                        f"`{sentence.text}` has slots {list(sig)} which match no "
                        "single declared combo — check intents.yaml / domain.",
                    )
                )
                continue

            placed[combo.name][group_index].append(sentence.text)
            group_meta[(combo.name, group_index)] = {
                "response": data.response,
                "domain_values": domain_values,
            }
            _collect_refs(
                sentence.expression,
                lang_intents.expansion_rules,
                result.rule_refs,
                result.list_refs,
            )

            if _has_list_in_alt_or_optional(sentence.expression):
                result.flags.append(
                    Flag(
                        "list in alternative/optional",
                        f"`{sentence.text}` — placed in `{combo.name}`, but a list "
                        "reference sits inside `(...)`/`[...]`; split it in two.",
                    )
                )

    # Build the data entries per combo.
    for combo_name, groups in placed.items():
        combo = combo_by_name[combo_name]
        entries: List[dict] = []
        for group_index in sorted(groups):
            meta = group_meta[(combo_name, group_index)]
            entry: dict = {"sentences": groups[group_index]}
            if combo.example:
                entry["example"] = combo.example
            if combo.domain_kind == "name":
                entry["name_domains"] = meta["domain_values"] or sorted(combo.domains)
            elif combo.domain_kind == "inferred":
                values = meta["domain_values"] or sorted(combo.domains)
                entry["inferred_domain"] = values[0] if values else None
            entry["response"] = meta["response"] or "default"
            if meta["response"] is None:
                result.flags.append(
                    Flag(
                        "response default",
                        f"`{combo_name}`: old sentences had no `response`; "
                        "defaulted to `default` — confirm the right response.",
                    )
                )
            entries.append(entry)
        result.combos[combo_name] = entries

    _write_sentence_files(args, combos, result)


def _collect_refs(
    expression: Any,
    rules: Dict[str, Any],
    rule_refs: Set[str],
    list_refs: Set[str],
    seen: Optional[Set[str]] = None,
) -> None:
    """Collect rule and list names referenced by an expression (transitively)."""
    from hassil import Group, ListReference, RuleReference

    seen = seen if seen is not None else set()
    if isinstance(expression, ListReference):
        list_refs.add(expression.list_name)
    elif isinstance(expression, RuleReference):
        rule_refs.add(expression.rule_name)
        if expression.rule_name not in seen:
            seen.add(expression.rule_name)
            body = rules.get(expression.rule_name)
            if body is not None:
                _collect_refs(body.expression, rules, rule_refs, list_refs, seen)
    elif isinstance(expression, Group):
        for item in expression.items:
            _collect_refs(item, rules, rule_refs, list_refs, seen)


def _has_list_in_alt_or_optional(expression: Any, inside: bool = False) -> bool:
    from hassil import Alternative, Group, ListReference

    if isinstance(expression, ListReference):
        return inside
    if isinstance(expression, Group):
        child_inside = inside or isinstance(expression, Alternative)
        return any(
            _has_list_in_alt_or_optional(item, child_inside)
            for item in expression.items
        )
    return False


def _write_sentence_files(
    args: argparse.Namespace, combos: List[ComboSpec], result: MigrationResult
) -> None:
    combo_by_name = {c.name: c for c in combos}
    out_dir = SENTENCE_DIR / args.language / args.intent
    for combo_name, entries in result.combos.items():
        path = out_dir / f"{combo_name}.yaml"
        if path.exists() and not args.force:
            result.flags.append(
                Flag("exists", f"{path} already exists; skipped (use --force).")
            )
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            _render_sentence_file(
                args.language, args.intent, combo_by_name[combo_name], entries
            ),
            encoding="utf-8",
        )
        result.written.append(path)


def _render_sentence_file(
    language: str, intent: str, combo: ComboSpec, entries: List[dict]
) -> str:
    lines = ["---", f"# {intent} - {combo.name}"]
    if combo.example:
        lines.append(f"# example: {combo.example}")
    slot_desc = _signature_comment(combo.signature)
    if slot_desc:
        lines.append(f"# {slot_desc}")
    lines += ["", f'language: "{language}"', "data:"]

    for entry in entries:
        lines.append("  - sentences:")
        for text in entry["sentences"]:
            lines.append(f'      - "{text}"')
        if entry.get("example"):
            lines.append(f'    example: "{entry["example"]}"')
        if "name_domains" in entry:
            lines.append("    name_domains:")
            for domain in entry["name_domains"]:
                lines.append(f'      - "{domain}"')
        if entry.get("inferred_domain"):
            lines.append(f'    inferred_domain: "{entry["inferred_domain"]}"')
        if entry.get("response"):
            lines.append(f'    response: "{entry["response"]}"')
    return "\n".join(lines) + "\n"


def _signature_comment(signature: Signature) -> str:
    parts = []
    has_context_area = CONTEXT_AREA_SLOT in signature
    slots = [s for s in signature if s != CONTEXT_AREA_SLOT]
    if slots:
        parts.append("slots: " + ", ".join(f"{{{s}}}" for s in slots))
    if has_context_area:
        parts.append("context_area: true")
    return "; ".join(parts)


# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------


def _migrate_tests(
    args: argparse.Namespace, combos: List[ComboSpec], result: MigrationResult
) -> None:
    fixtures_path = TESTS_DIR / args.language / "_fixtures.yaml"
    fixtures = (
        yaml.safe_load(fixtures_path.read_text(encoding="utf-8"))
        if fixtures_path.exists()
        else {}
    )
    area_id_to_name = {a["id"]: a["name"] for a in (fixtures.get("areas") or [])}
    floor_id_to_name = {f["id"]: f["name"] for f in (fixtures.get("floors") or [])}

    def to_new_entity(entity: dict) -> dict:
        new: Dict[str, Any] = {"name": entity["name"]}
        entity_id = entity.get("id", "")
        if "." in entity_id:
            new["domain"] = entity_id.split(".", 1)[0]
        else:
            result.flags.append(
                Flag(
                    "fixture domain",
                    f"entity {entity['name']!r} has no domain in id {entity_id!r}; "
                    "set `domain:` manually.",
                )
            )
        for key in ("state", "state_with_unit", "attributes", "is_exposed"):
            if key in entity:
                new[key] = entity[key]
        if entity.get("area"):
            new["area"] = area_id_to_name.get(entity["area"], entity["area"])
        return new

    def to_new_area(area: dict) -> dict:
        new: Dict[str, Any] = {"name": area["name"]}
        if area.get("floor"):
            new["floor"] = floor_id_to_name.get(area["floor"], area["floor"])
        return new

    by_name = {
        "entities": {
            e["name"]: to_new_entity(e) for e in (fixtures.get("entities") or [])
        },
        "areas": {a["name"]: to_new_area(a) for a in (fixtures.get("areas") or [])},
        "floors": {
            f["name"]: {"name": f["name"]} for f in (fixtures.get("floors") or [])
        },
    }

    test_files = list((TESTS_DIR / args.language).glob(f"*_{args.intent}.yaml"))
    if not test_files:
        result.flags.append(
            Flag("tests", f"No old test file matching *_{args.intent}.yaml found.")
        )
        return

    combo_tests: Dict[str, List[dict]] = defaultdict(list)
    for test_file in test_files:
        doc = yaml.safe_load(test_file.read_text(encoding="utf-8")) or {}
        for test in doc.get("tests", []):
            intent_block = test.get("intent", {})
            slots = dict(intent_block.get("slots", {}))
            context = intent_block.get("context", {})

            # Every declared slot counts toward the signature (name, area, floor,
            # message, query, item, ...) — not just the entity slots.
            sig_slots: Set[str] = set(slots)
            if "device_class" in context:
                sig_slots.add("device_class")
            if "domain" in context:
                sig_slots.add("domain")
            if context.get("area"):
                sig_slots.add(CONTEXT_AREA_SLOT)
                sig_slots.discard("area")

            domain_values = []
            for source in (slots, context):
                raw = source.get("domain")
                if raw:
                    domain_values = [raw] if isinstance(raw, str) else list(raw)

            combo = _map_combo(combos, tuple(sorted(sig_slots)), domain_values)
            if combo is None:
                result.flags.append(
                    Flag(
                        "test unmapped",
                        f"Test {test.get('sentences', [''])[0]!r} has slots "
                        f"{sorted(sig_slots)} matching no single combo.",
                    )
                )
                continue
            combo_tests[combo.name].append(test)

    # Timer/media fixtures live in _fixtures.yaml and are matched against, not
    # named per test, so carry them verbatim (resolving area ids) into each file.
    carry: Dict[str, list] = {}
    if "Timer" in args.intent and fixtures.get("timers"):
        timers = []
        for timer in fixtures["timers"]:
            new_timer = dict(timer)
            if new_timer.get("area"):
                new_timer["area"] = area_id_to_name.get(
                    new_timer["area"], new_timer["area"]
                )
            timers.append(new_timer)
        carry["timers"] = timers
    if "Media" in args.intent and fixtures.get("media"):
        carry["media"] = list(fixtures["media"])

    _write_test_files(args, combo_tests, by_name, carry, result)


def _write_test_files(
    args: argparse.Namespace,
    combo_tests: Dict[str, List[dict]],
    fixtures_by_name: Dict[str, Dict[str, dict]],
    carry: Dict[str, list],
    result: MigrationResult,
) -> None:
    out_dir = TESTS_DIR / args.language / args.intent
    for combo_name, tests in combo_tests.items():
        path = out_dir / f"{combo_name}.yaml"
        if path.exists() and not args.force:
            result.flags.append(
                Flag("exists", f"{path} already exists; skipped (use --force).")
            )
            continue

        used = {"entities": [], "areas": [], "floors": []}
        seen = {"entities": set(), "areas": set(), "floors": set()}
        for test in tests:
            slots = test.get("intent", {}).get("slots", {})
            context = test.get("intent", {}).get("context", {})
            for kind, key in (
                ("entities", "name"),
                ("areas", "area"),
                ("floors", "floor"),
            ):
                for source in (slots, context):
                    raw = source.get(key)
                    if not raw:
                        continue
                    # A slot value may be a list of acceptable strings.
                    for value in raw if isinstance(raw, list) else [raw]:
                        if not value or value in seen[kind]:
                            continue
                        fixture = fixtures_by_name[kind].get(value)
                        if fixture is None:
                            result.flags.append(
                                Flag(
                                    "fixture missing",
                                    f"{combo_name}: no {kind[:-1]} fixture named "
                                    f"{value!r} in _fixtures.yaml.",
                                )
                            )
                        else:
                            used[kind].append(fixture)
                            seen[kind].add(value)

        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            _render_test_file(
                args.language, args.intent, combo_name, used, carry, tests
            ),
            encoding="utf-8",
        )
        result.written.append(path)


def _render_test_file(
    language: str,
    intent: str,
    combo_name: str,
    fixtures: Dict[str, List[dict]],
    carry: Dict[str, list],
    tests: List[dict],
) -> str:
    doc: Dict[str, Any] = {"language": language}
    for kind in ("floors", "areas", "entities"):
        if fixtures[kind]:
            doc[kind] = fixtures[kind]
    for kind in ("timers", "media"):
        if carry.get(kind):
            doc[kind] = carry[kind]

    new_tests = []
    for test in tests:
        new_test: Dict[str, Any] = {"sentences": test.get("sentences", [])}
        slots = test.get("intent", {}).get("slots")
        if slots:
            new_test["slots"] = slots
        if "response" in test:
            new_test["response"] = test["response"]
        new_tests.append(new_test)
    doc["tests"] = new_tests

    header = f"---\n# {intent} - {combo_name}\n\n"
    return header + yaml.dump(
        doc,
        Dumper=YamlDumper,
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
    )


# -----------------------------------------------------------------------------
# Coverage + report
# -----------------------------------------------------------------------------


def _check_references_resolve(language: str, result: MigrationResult) -> None:
    """Flag rule/list refs that the slot-combination test harness can't resolve.

    The harness loads expansion rules only from ``rules/<lang>/`` and lists only
    from ``lists/`` and ``lists/<lang>/`` — it never reads ``_common.yaml``. So a
    migrated template referencing a rule/list that doesn't live there yet will
    fail to compile in tests. Such refs must be inlined or moved.
    """
    rule_names: Set[str] = set()
    for rule_file in (RULE_DIR / language).glob("*.yaml"):
        doc = yaml.safe_load(rule_file.read_text(encoding="utf-8")) or {}
        rule_names.update((doc.get("expansion_rules") or {}).keys())

    list_names: Set[str] = set(BUILTIN_LISTS)
    for list_dir in (LIST_DIR, LIST_DIR / language):
        for list_file in list_dir.glob("*.yaml"):
            doc = yaml.safe_load(list_file.read_text(encoding="utf-8")) or {}
            list_names.update((doc.get("lists") or {}).keys())

    for missing in sorted(result.rule_refs - rule_names):
        result.flags.append(
            Flag(
                "unresolved rule",
                f"`<{missing}>` is not in rules/{language}/ — inline it into the "
                "templates or move it there (the test harness ignores _common.yaml).",
            )
        )
    for missing in sorted(result.list_refs - list_names):
        result.flags.append(
            Flag(
                "unresolved list",
                f"`{{{missing}}}` is not in lists/{language}/ or lists/ — move it "
                "there (the test harness ignores _common.yaml).",
            )
        )


def _check_required_coverage(intent_info: dict, result: MigrationResult) -> None:
    for name, combo in (intent_info.get("slot_combinations") or {}).items():
        covered = name in result.combos
        for key in ("name_domains", "inferred_domains"):
            required = (combo.get(key) or {}).get("required")
            if required and not covered:
                result.flags.append(
                    Flag(
                        "missing required coverage",
                        f"combo `{name}` declares required {key} {required} "
                        "but no sentences were placed there.",
                    )
                )


def _render_report(
    args: argparse.Namespace, combos: List[ComboSpec], result: MigrationResult
) -> str:
    lines = [
        f"# Migration report: {args.language} / {args.intent}",
        "",
        "## Declared slot combinations",
    ]
    for combo in combos:
        if combo.name in result.combos:
            status = "scaffolded"
        elif combo.required:
            status = "EMPTY — REQUIRED, must be filled"
        else:
            status = "EMPTY — non-required, safe to skip"
        lines.append(
            f"- `{combo.name}` {_signature_comment(combo.signature) or '(no slots)'}"
            f" — {status}"
        )

    lines += ["", "## Scaffold files written"]
    lines += [f"- {p}" for p in result.written] or ["- (none)"]

    old_files = sorted(
        (SENTENCE_DIR / args.language).glob(f"*_{args.intent}.yaml")
    ) + sorted((TESTS_DIR / args.language).glob(f"*_{args.intent}.yaml"))
    lines += [
        "",
        "## Old files to delete when done",
        "(this intent may span several domain files — delete ALL of them)",
    ]
    lines += [f"- {p}" for p in old_files] or ["- (none)"]

    lines += ["", f"## Flags needing attention ({len(result.flags)})"]
    if not result.flags:
        lines.append("- none — review the scaffold and run `validate` + tests.")
    else:
        by_cat: Dict[str, List[str]] = defaultdict(list)
        for flag in result.flags:
            by_cat[flag.category].append(flag.detail)
        for category in sorted(by_cat):
            lines.append(f"\n### {category} ({len(by_cat[category])})")
            lines += [f"- {detail}" for detail in by_cat[category]]

    lines += [
        "",
        "## Reminders (see docs/syntax_migration_guide.md)",
        "- Inline list-bearing rules in templates (e.g. `<name>` -> `[de|het] {name}`).",
        "- Flatten nested `<rule>` references.",
        "- Add an `example:` taken from the matching test sentences.",
        "- Delete the old `*_" + args.intent + ".yaml` sentence/test files once done.",
        "- Run `python3 -m script.intentfest validate --language "
        + args.language
        + "` and the tests.",
    ]
    return "\n".join(lines) + "\n"
