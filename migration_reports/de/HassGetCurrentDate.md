# Migration report: de / HassGetCurrentDate

## Declared slot combinations
- `default` (no slots) — scaffolded

## Scaffold files written
- /home/user/intents/sentences/de/HassGetCurrentDate/default.yaml
- /home/user/intents/tests/de/HassGetCurrentDate/default.yaml

## Old files to delete when done
(this intent may span several domain files — delete ALL of them)
- /home/user/intents/sentences/de/homeassistant_HassGetCurrentDate.yaml
- /home/user/intents/tests/de/homeassistant_HassGetCurrentDate.yaml

## Flags needing attention (1)

### response default (1)
- `default`: old sentences had no `response`; defaulted to `default` — confirm the right response.

## Reminders (see docs/syntax_migration_guide.md)
- Inline list-bearing rules in templates (e.g. `<name>` -> `[de|het] {name}`).
- Flatten nested `<rule>` references.
- Add an `example:` taken from the matching test sentences.
- Delete the old `*_HassGetCurrentDate.yaml` sentence/test files once done.
- Run `python3 -m script.intentfest validate --language de` and the tests.
