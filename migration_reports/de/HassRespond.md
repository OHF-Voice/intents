# Migration report: de / HassRespond

## Declared slot combinations
- `default` (no slots) — scaffolded

## Scaffold files written
- /home/user/intents/sentences/de/HassRespond/default.yaml
- /home/user/intents/tests/de/HassRespond/default.yaml

## Old files to delete when done
(this intent may span several domain files — delete ALL of them)
- /home/user/intents/sentences/de/homeassistant_HassRespond.yaml
- /home/user/intents/tests/de/homeassistant_HassRespond.yaml

## Flags needing attention (0)
- none — review the scaffold and run `validate` + tests.

## Reminders (see docs/syntax_migration_guide.md)
- Inline list-bearing rules in templates (e.g. `<name>` -> `[de|het] {name}`).
- Flatten nested `<rule>` references.
- Add an `example:` taken from the matching test sentences.
- Delete the old `*_HassRespond.yaml` sentence/test files once done.
- Run `python3 -m script.intentfest validate --language de` and the tests.
