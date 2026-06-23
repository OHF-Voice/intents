# Migration report: de / HassUnpauseTimer

## Declared slot combinations
- `default` (no slots) — scaffolded
- `name_only` slots: {name} — scaffolded
- `area_only` slots: {area} — scaffolded
- `hours_only` slots: {start_hours} — EMPTY — non-required, safe to skip
- `minutes_only` slots: {start_minutes} — EMPTY — non-required, safe to skip
- `seconds_only` slots: {start_seconds} — EMPTY — non-required, safe to skip

## Scaffold files written
- /home/user/intents/sentences/de/HassUnpauseTimer/name_only.yaml
- /home/user/intents/sentences/de/HassUnpauseTimer/default.yaml
- /home/user/intents/sentences/de/HassUnpauseTimer/area_only.yaml
- /home/user/intents/tests/de/HassUnpauseTimer/default.yaml
- /home/user/intents/tests/de/HassUnpauseTimer/hours_only.yaml
- /home/user/intents/tests/de/HassUnpauseTimer/name_only.yaml
- /home/user/intents/tests/de/HassUnpauseTimer/area_only.yaml

## Old files to delete when done
(this intent may span several domain files — delete ALL of them)
- /home/user/intents/sentences/de/homeassistant_HassUnpauseTimer.yaml
- /home/user/intents/tests/de/homeassistant_HassUnpauseTimer.yaml

## Flags needing attention (10)

### complex template (6)
- `(setz[e]|<stt_fix_setze>)[ (den|meinen)] <timer_start> Timer fort` has too many slot combinations to analyze — split it by hand from the reference language.
- `(setz[e]|<stt_fix_setze>)[ (den|meinen)] Timer für <timer_start> fort` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(den|meinen) ]<timer_start> Timer (fortsetzen|weiter[ ]laufen lassen)` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(den|meinen) ]Timer für <timer_start> (fortsetzen|weiter[ ]laufen lassen)` has too many slot combinations to analyze — split it by hand from the reference language.
- `lass[e] (den|meinen) <timer_start> Timer weiter[ ]laufen` has too many slot combinations to analyze — split it by hand from the reference language.
- `lass[e][ (den|meinen)] Timer für <timer_start> weiter[ ]laufen` has too many slot combinations to analyze — split it by hand from the reference language.

### fixture missing (1)
- name_only: no entitie fixture named 'Pizza' in _fixtures.yaml.

### response default (3)
- `name_only`: old sentences had no `response`; defaulted to `default` — confirm the right response.
- `default`: old sentences had no `response`; defaulted to `default` — confirm the right response.
- `area_only`: old sentences had no `response`; defaulted to `default` — confirm the right response.

## Reminders (see docs/syntax_migration_guide.md)
- Inline list-bearing rules in templates (e.g. `<name>` -> `[de|het] {name}`).
- Flatten nested `<rule>` references.
- Add an `example:` taken from the matching test sentences.
- Delete the old `*_HassUnpauseTimer.yaml` sentence/test files once done.
- Run `python3 -m script.intentfest validate --language de` and the tests.
