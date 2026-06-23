# Migration report: de / HassPauseTimer

## Declared slot combinations
- `default` (no slots) — scaffolded
- `name_only` slots: {name} — scaffolded
- `area_only` slots: {area} — scaffolded
- `hours_only` slots: {start_hours} — EMPTY — non-required, safe to skip
- `minutes_only` slots: {start_minutes} — EMPTY — non-required, safe to skip
- `seconds_only` slots: {start_seconds} — EMPTY — non-required, safe to skip

## Scaffold files written
- /home/user/intents/sentences/de/HassPauseTimer/name_only.yaml
- /home/user/intents/sentences/de/HassPauseTimer/default.yaml
- /home/user/intents/sentences/de/HassPauseTimer/area_only.yaml
- /home/user/intents/tests/de/HassPauseTimer/default.yaml
- /home/user/intents/tests/de/HassPauseTimer/hours_only.yaml
- /home/user/intents/tests/de/HassPauseTimer/name_only.yaml
- /home/user/intents/tests/de/HassPauseTimer/area_only.yaml

## Old files to delete when done
(this intent may span several domain files — delete ALL of them)
- /home/user/intents/sentences/de/homeassistant_HassPauseTimer.yaml
- /home/user/intents/tests/de/homeassistant_HassPauseTimer.yaml

## Flags needing attention (9)

### fixture missing (1)
- name_only: no entitie fixture named 'Pizza' in _fixtures.yaml.

### multi-combo template (5)
- `pausiere[ (den|meinen|unseren)] <timer_start> Timer` matches ["?['start_hours', 'start_minutes', 'start_seconds']", "?['start_hours', 'start_minutes']", "?['start_hours', 'start_seconds']", "?['start_minutes', 'start_seconds']", 'hours_only', 'minutes_only', 'seconds_only'] — split into one template per combo.
- `pausiere[ (den|meinen|unseren)] Timer für <timer_start>` matches ["?['start_hours', 'start_minutes', 'start_seconds']", "?['start_hours', 'start_minutes']", "?['start_hours', 'start_seconds']", "?['start_minutes', 'start_seconds']", 'hours_only', 'minutes_only', 'seconds_only'] — split into one template per combo.
- `[(den|meinen|unseren) ]<timer_start> Timer (pausieren|anhalten)` matches ["?['start_hours', 'start_minutes', 'start_seconds']", "?['start_hours', 'start_minutes']", "?['start_hours', 'start_seconds']", "?['start_minutes', 'start_seconds']", 'hours_only', 'minutes_only', 'seconds_only'] — split into one template per combo.
- `halt[e] (den|meinen|unseren) <timer_start> Timer an` matches ["?['start_hours', 'start_minutes', 'start_seconds']", "?['start_hours', 'start_minutes']", "?['start_hours', 'start_seconds']", "?['start_minutes', 'start_seconds']", 'hours_only', 'minutes_only', 'seconds_only'] — split into one template per combo.
- `halt[e] (den|meinen|unseren) Timer für <timer_start> an` matches ["?['start_hours', 'start_minutes', 'start_seconds']", "?['start_hours', 'start_minutes']", "?['start_hours', 'start_seconds']", "?['start_minutes', 'start_seconds']", 'hours_only', 'minutes_only', 'seconds_only'] — split into one template per combo.

### response default (3)
- `name_only`: old sentences had no `response`; defaulted to `default` — confirm the right response.
- `default`: old sentences had no `response`; defaulted to `default` — confirm the right response.
- `area_only`: old sentences had no `response`; defaulted to `default` — confirm the right response.

## Reminders (see docs/syntax_migration_guide.md)
- Inline list-bearing rules in templates (e.g. `<name>` -> `[de|het] {name}`).
- Flatten nested `<rule>` references.
- Add an `example:` taken from the matching test sentences.
- Delete the old `*_HassPauseTimer.yaml` sentence/test files once done.
- Run `python3 -m script.intentfest validate --language de` and the tests.
