# Migration report: de / HassVacuumStart

## Declared slot combinations
- `name_only` slots: {name} — scaffolded
- `area_only` slots: {area} — EMPTY — non-required, safe to skip
- `floor_only` slots: {floor} — EMPTY — non-required, safe to skip

## Scaffold files written
- /home/user/intents/sentences/de/HassVacuumStart/name_only.yaml
- /home/user/intents/tests/de/HassVacuumStart/name_only.yaml

## Old files to delete when done
(this intent may span several domain files — delete ALL of them)
- /home/user/intents/sentences/de/vacuum_HassVacuumStart.yaml
- /home/user/intents/tests/de/vacuum_HassVacuumStart.yaml

## Flags needing attention (2)

### response default (1)
- `name_only`: old sentences had no `response`; defaulted to `default` — confirm the right response.

### unresolved rule (1)
- `<cleaning>` is not in rules/de/ — inline it into the templates or move it there (the test harness ignores _common.yaml).

## Reminders (see docs/syntax_migration_guide.md)
- Inline list-bearing rules in templates (e.g. `<name>` -> `[de|het] {name}`).
- Flatten nested `<rule>` references.
- Add an `example:` taken from the matching test sentences.
- Delete the old `*_HassVacuumStart.yaml` sentence/test files once done.
- Run `python3 -m script.intentfest validate --language de` and the tests.
