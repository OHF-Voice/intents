# Migration report: de / HassVacuumCleanArea

## Declared slot combinations
- `context_area` context_area: true — scaffolded
- `area_only` slots: {area} — scaffolded
- `name_area` slots: {area}, {name} — scaffolded

## Scaffold files written
- /home/user/intents/sentences/de/HassVacuumCleanArea/area_only.yaml
- /home/user/intents/sentences/de/HassVacuumCleanArea/context_area.yaml
- /home/user/intents/sentences/de/HassVacuumCleanArea/name_area.yaml
- /home/user/intents/tests/de/HassVacuumCleanArea/area_only.yaml
- /home/user/intents/tests/de/HassVacuumCleanArea/context_area.yaml
- /home/user/intents/tests/de/HassVacuumCleanArea/name_area.yaml

## Old files to delete when done
(this intent may span several domain files — delete ALL of them)
- /home/user/intents/sentences/de/vacuum_HassVacuumCleanArea.yaml
- /home/user/intents/tests/de/vacuum_HassVacuumCleanArea.yaml

## Flags needing attention (5)

### complex template (1)
- `lass[e] <name> <area> (reinigen|putzen|[staub[ ]]saugen|wischen)` has too many slot combinations to analyze — split it by hand from the reference language.

### response default (3)
- `area_only`: old sentences had no `response`; defaulted to `default` — confirm the right response.
- `context_area`: old sentences had no `response`; defaulted to `default` — confirm the right response.
- `name_area`: old sentences had no `response`; defaulted to `default` — confirm the right response.

### unresolved rule (1)
- `<cleaning>` is not in rules/de/ — inline it into the templates or move it there (the test harness ignores _common.yaml).

## Reminders (see docs/syntax_migration_guide.md)
- Inline list-bearing rules in templates (e.g. `<name>` -> `[de|het] {name}`).
- Flatten nested `<rule>` references.
- Add an `example:` taken from the matching test sentences.
- Delete the old `*_HassVacuumCleanArea.yaml` sentence/test files once done.
- Run `python3 -m script.intentfest validate --language de` and the tests.
