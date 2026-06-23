# Migration report: de / HassShoppingListCompleteItem

## Declared slot combinations
- `item_only` slots: {item} — scaffolded

## Scaffold files written
- /home/user/intents/sentences/de/HassShoppingListCompleteItem/item_only.yaml
- /home/user/intents/tests/de/HassShoppingListCompleteItem/item_only.yaml

## Old files to delete when done
(this intent may span several domain files — delete ALL of them)
- /home/user/intents/sentences/de/shopping_list_HassShoppingListCompleteItem.yaml
- /home/user/intents/tests/de/shopping_list_HassShoppingListCompleteItem.yaml

## Flags needing attention (3)

### unresolved rule (3)
- `<item>` is not in rules/de/ — inline it into the templates or move it there (the test harness ignores _common.yaml).
- `<mein_einkauf_dativ>` is not in rules/de/ — inline it into the templates or move it there (the test harness ignores _common.yaml).
- `<meine_einkaufsliste_dativ>` is not in rules/de/ — inline it into the templates or move it there (the test harness ignores _common.yaml).

## Reminders (see docs/syntax_migration_guide.md)
- Inline list-bearing rules in templates (e.g. `<name>` -> `[de|het] {name}`).
- Flatten nested `<rule>` references.
- Add an `example:` taken from the matching test sentences.
- Delete the old `*_HassShoppingListCompleteItem.yaml` sentence/test files once done.
- Run `python3 -m script.intentfest validate --language de` and the tests.
