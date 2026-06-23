# Migration report: de / HassCancelTimer

## Declared slot combinations
- `default` (no slots) — scaffolded
- `name_only` slots: {name} — scaffolded
- `area_only` slots: {area} — scaffolded
- `hours_only` slots: {start_hours} — EMPTY — non-required, safe to skip
- `minutes_only` slots: {start_minutes} — EMPTY — non-required, safe to skip
- `seconds_only` slots: {start_seconds} — EMPTY — non-required, safe to skip

## Scaffold files written
- /home/user/intents/sentences/de/HassCancelTimer/name_only.yaml
- /home/user/intents/sentences/de/HassCancelTimer/default.yaml
- /home/user/intents/sentences/de/HassCancelTimer/area_only.yaml
- /home/user/intents/tests/de/HassCancelTimer/default.yaml
- /home/user/intents/tests/de/HassCancelTimer/minutes_only.yaml
- /home/user/intents/tests/de/HassCancelTimer/name_only.yaml
- /home/user/intents/tests/de/HassCancelTimer/area_only.yaml

## Old files to delete when done
(this intent may span several domain files — delete ALL of them)
- /home/user/intents/sentences/de/homeassistant_HassCancelTimer.yaml
- /home/user/intents/tests/de/homeassistant_HassCancelTimer.yaml

## Flags needing attention (10)

### complex template (3)
- `[(den|meinen|unseren) ][(<timer_start>|{timer_name:name}|{area}) ]Timer <timer_cancel_end_of_sentence>` has too many slot combinations to analyze — split it by hand from the reference language.
- `<timer_cancel>[ (den|meinen|unseren)] <timer_start> Timer` has too many slot combinations to analyze — split it by hand from the reference language.
- `<timer_cancel>[ (den|meinen|unseren)] Timer für <timer_start>` has too many slot combinations to analyze — split it by hand from the reference language.

### fixture missing (1)
- name_only: no entitie fixture named 'Pizza' in _fixtures.yaml.

### multi-combo template (3)
- `[(den|meinen|unseren) ]Timer (für [<artikel_bestimmt> ]{timer_name:name}|<area>) <timer_cancel_end_of_sentence>` matches ['area_only', 'name_only'] — split into one template per combo.
- `brech[e] (den|meinen|unseren) <timer_start> Timer ab` matches ["?['start_hours', 'start_minutes', 'start_seconds']", "?['start_hours', 'start_minutes']", "?['start_hours', 'start_seconds']", "?['start_minutes', 'start_seconds']", 'hours_only', 'minutes_only', 'seconds_only'] — split into one template per combo.
- `brech[e] (den|meinen|unseren) Timer für <timer_start> ab` matches ["?['start_hours', 'start_minutes', 'start_seconds']", "?['start_hours', 'start_minutes']", "?['start_hours', 'start_seconds']", "?['start_minutes', 'start_seconds']", 'hours_only', 'minutes_only', 'seconds_only'] — split into one template per combo.

### response default (3)
- `name_only`: old sentences had no `response`; defaulted to `default` — confirm the right response.
- `default`: old sentences had no `response`; defaulted to `default` — confirm the right response.
- `area_only`: old sentences had no `response`; defaulted to `default` — confirm the right response.

## Reminders (see docs/syntax_migration_guide.md)
- Inline list-bearing rules in templates (e.g. `<name>` -> `[de|het] {name}`).
- Flatten nested `<rule>` references.
- Add an `example:` taken from the matching test sentences.
- Delete the old `*_HassCancelTimer.yaml` sentence/test files once done.
- Run `python3 -m script.intentfest validate --language de` and the tests.
