# Migration report: de / HassListRemoveItem

## Declared slot combinations
- `name_item` slots: {item}, {name} — scaffolded

## Scaffold files written
- /home/user/intents/sentences/de/HassListRemoveItem/name_item.yaml
- /home/user/intents/tests/de/HassListRemoveItem/name_item.yaml

## Old files to delete when done
(this intent may span several domain files — delete ALL of them)
- /home/user/intents/sentences/de/todo_HassListRemoveItem.yaml
- /home/user/intents/tests/de/todo_HassListRemoveItem.yaml

## Flags needing attention (1)

### unresolved rule (1)
- `<item>` is not in rules/de/ — inline it into the templates or move it there (the test harness ignores _common.yaml).

## Reminders (see docs/syntax_migration_guide.md)
- Inline list-bearing rules in templates (e.g. `<name>` -> `[de|het] {name}`).
- Flatten nested `<rule>` references.
- Add an `example:` taken from the matching test sentences.
- Delete the old `*_HassListRemoveItem.yaml` sentence/test files once done.
- Run `python3 -m script.intentfest validate --language de` and the tests.
