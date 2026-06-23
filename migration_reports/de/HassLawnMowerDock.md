# Migration report: de / HassLawnMowerDock

## Declared slot combinations
- `default` (no slots) — scaffolded
- `name_only` slots: {name} — scaffolded

## Scaffold files written
- /home/user/intents/sentences/de/HassLawnMowerDock/default.yaml
- /home/user/intents/sentences/de/HassLawnMowerDock/name_only.yaml
- /home/user/intents/tests/de/HassLawnMowerDock/default.yaml
- /home/user/intents/tests/de/HassLawnMowerDock/name_only.yaml

## Old files to delete when done
(this intent may span several domain files — delete ALL of them)
- /home/user/intents/sentences/de/lawn_mower_HassLawnMowerDock.yaml
- /home/user/intents/tests/de/lawn_mower_HassLawnMowerDock.yaml

## Flags needing attention (2)

### response default (2)
- `default`: old sentences had no `response`; defaulted to `default` — confirm the right response.
- `name_only`: old sentences had no `response`; defaulted to `default` — confirm the right response.

## Reminders (see docs/syntax_migration_guide.md)
- Inline list-bearing rules in templates (e.g. `<name>` -> `[de|het] {name}`).
- Flatten nested `<rule>` references.
- Add an `example:` taken from the matching test sentences.
- Delete the old `*_HassLawnMowerDock.yaml` sentence/test files once done.
- Run `python3 -m script.intentfest validate --language de` and the tests.
