# Migration report: de / HassBroadcast

## Declared slot combinations
- `message_only` slots: {message} — scaffolded

## Scaffold files written
- /home/user/intents/sentences/de/HassBroadcast/message_only.yaml
- /home/user/intents/tests/de/HassBroadcast/message_only.yaml

## Old files to delete when done
(this intent may span several domain files — delete ALL of them)
- /home/user/intents/sentences/de/assist_satellite_HassBroadcast.yaml
- /home/user/intents/tests/de/assist_satellite_HassBroadcast.yaml

## Flags needing attention (1)

### response default (1)
- `message_only`: old sentences had no `response`; defaulted to `default` — confirm the right response.

## Reminders (see docs/syntax_migration_guide.md)
- Inline list-bearing rules in templates (e.g. `<name>` -> `[de|het] {name}`).
- Flatten nested `<rule>` references.
- Add an `example:` taken from the matching test sentences.
- Delete the old `*_HassBroadcast.yaml` sentence/test files once done.
- Run `python3 -m script.intentfest validate --language de` and the tests.
