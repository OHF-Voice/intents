# Migration report: de / HassCancelAllTimers

## Declared slot combinations
- `default` (no slots) — scaffolded
- `area_only` slots: {area} — scaffolded

## Scaffold files written
- /home/user/intents/sentences/de/HassCancelAllTimers/default.yaml
- /home/user/intents/sentences/de/HassCancelAllTimers/area_only.yaml
- /home/user/intents/tests/de/HassCancelAllTimers/default.yaml
- /home/user/intents/tests/de/HassCancelAllTimers/area_only.yaml

## Old files to delete when done
(this intent may span several domain files — delete ALL of them)
- /home/user/intents/sentences/de/homeassistant_HassCancelAllTimers.yaml
- /home/user/intents/tests/de/homeassistant_HassCancelAllTimers.yaml

## Flags needing attention (5)

### response default (1)
- `default`: old sentences had no `response`; defaulted to `default` — confirm the right response.

### test unmapped (1)
- Test 'beende alle Timer hier' has slots ['__context_area__'] matching no single combo.

### unmapped signature (3)
- `<timer_cancel> (alle[ (meine|unsere)]|sämtliche[ (meiner|unserer)]) Timer <hier>` has slots ['__context_area__'] which match no single declared combo — check intents.yaml / domain.
- `<timer_cancel> <hier> (alle[ (meine|unsere)]|sämtliche[ (meiner|unserer)]) Timer` has slots ['__context_area__'] which match no single declared combo — check intents.yaml / domain.
- `(alle[ (meine|unsere)]|sämtliche[ (meiner|unserer)]) Timer <hier> <timer_cancel_end_of_sentence>` has slots ['__context_area__'] which match no single declared combo — check intents.yaml / domain.

## Reminders (see docs/syntax_migration_guide.md)
- Inline list-bearing rules in templates (e.g. `<name>` -> `[de|het] {name}`).
- Flatten nested `<rule>` references.
- Add an `example:` taken from the matching test sentences.
- Delete the old `*_HassCancelAllTimers.yaml` sentence/test files once done.
- Run `python3 -m script.intentfest validate --language de` and the tests.
