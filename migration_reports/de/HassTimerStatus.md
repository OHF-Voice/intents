# Migration report: de / HassTimerStatus

## Declared slot combinations
- `default` (no slots) — scaffolded
- `name_only` slots: {name} — scaffolded
- `area_only` slots: {area} — scaffolded
- `hours_only` slots: {start_hours} — EMPTY — non-required, safe to skip
- `minutes_only` slots: {start_minutes} — EMPTY — non-required, safe to skip
- `seconds_only` slots: {start_seconds} — EMPTY — non-required, safe to skip

## Scaffold files written
- /home/user/intents/sentences/de/HassTimerStatus/name_only.yaml
- /home/user/intents/sentences/de/HassTimerStatus/default.yaml
- /home/user/intents/sentences/de/HassTimerStatus/area_only.yaml
- /home/user/intents/tests/de/HassTimerStatus/default.yaml
- /home/user/intents/tests/de/HassTimerStatus/hours_only.yaml
- /home/user/intents/tests/de/HassTimerStatus/name_only.yaml
- /home/user/intents/tests/de/HassTimerStatus/area_only.yaml

## Old files to delete when done
(this intent may span several domain files — delete ALL of them)
- /home/user/intents/sentences/de/homeassistant_HassTimerStatus.yaml
- /home/user/intents/tests/de/homeassistant_HassTimerStatus.yaml

## Flags needing attention (17)

### complex template (4)
- `wie lang[e] (hat|haben|braucht|brauchen|dauert|dauern|läuft) [(<artikel_bestimmt>|<possessivpronom_mein>|<possessivpronom_unser>) ]{timer_name:name}[[-| ]Timer][ noch]` has too many slot combinations to analyze — split it by hand from the reference language.
- `(Restzeit|Status) (des|meines|unseres) <timer_start> Timer[s]` has too many slot combinations to analyze — split it by hand from the reference language.
- `(Restzeit|Status)[ (von (dem|meinem|unserem)|vom)] <timer_start> Timer` has too many slot combinations to analyze — split it by hand from the reference language.
- `wie lang[e] (läuft|braucht|hat|dauert|geht) (der|mein|unser) <timer_start> Timer` has too many slot combinations to analyze — split it by hand from the reference language.

### fixture missing (2)
- name_only: no entitie fixture named 'Pizza' in _fixtures.yaml.
- name_only: no entitie fixture named 'Nudeln' in _fixtures.yaml.

### multi-combo template (8)
- `wann ist (der|mein|unser) timer[ für [(<artikel_bestimmt>|<possessivpronom_mein>|<possessivpronom_unser>) ]{timer_name:name}] (zu ende|fertig)` matches ['default', 'name_only'] — split into one template per combo.
- `wann läuft (der|mein|unser) timer[ für [(<artikel_bestimmt>|<possessivpronom_mein>|<possessivpronom_unser>) ]{timer_name:name}] ab` matches ['default', 'name_only'] — split into one template per combo.
- `wann endet (der|mein|unser) timer[ für [(<artikel_bestimmt>|<possessivpronom_mein>|<possessivpronom_unser>) ]{timer_name:name}]` matches ['default', 'name_only'] — split into one template per combo.
- `<timer_start> Timer (Restzeit|Status)` matches ["?['start_hours', 'start_minutes', 'start_seconds']", "?['start_hours', 'start_minutes']", "?['start_hours', 'start_seconds']", "?['start_minutes', 'start_seconds']", 'hours_only', 'minutes_only', 'seconds_only'] — split into one template per combo.
- `was macht (der|mein|unser) <timer_start> Timer` matches ["?['start_hours', 'start_minutes', 'start_seconds']", "?['start_hours', 'start_minutes']", "?['start_hours', 'start_seconds']", "?['start_minutes', 'start_seconds']", 'hours_only', 'minutes_only', 'seconds_only'] — split into one template per combo.
- `wann endet (der|mein|unser) (<timer_start>|{area}) timer` matches ["?['start_hours', 'start_minutes', 'start_seconds']", "?['start_hours', 'start_minutes']", "?['start_hours', 'start_seconds']", "?['start_minutes', 'start_seconds']", 'area_only', 'hours_only', 'minutes_only', 'seconds_only'] — split into one template per combo.
- `wann ist (der|mein|unser) (<timer_start>|{area}) timer (zu ende|fertig)` matches ["?['start_hours', 'start_minutes', 'start_seconds']", "?['start_hours', 'start_minutes']", "?['start_hours', 'start_seconds']", "?['start_minutes', 'start_seconds']", 'area_only', 'hours_only', 'minutes_only', 'seconds_only'] — split into one template per combo.
- `wann läuft (der|mein|unser) (<timer_start>|{area}) timer ab` matches ["?['start_hours', 'start_minutes', 'start_seconds']", "?['start_hours', 'start_minutes']", "?['start_hours', 'start_seconds']", "?['start_minutes', 'start_seconds']", 'area_only', 'hours_only', 'minutes_only', 'seconds_only'] — split into one template per combo.

### response default (3)
- `name_only`: old sentences had no `response`; defaulted to `default` — confirm the right response.
- `default`: old sentences had no `response`; defaulted to `default` — confirm the right response.
- `area_only`: old sentences had no `response`; defaulted to `default` — confirm the right response.

## Reminders (see docs/syntax_migration_guide.md)
- Inline list-bearing rules in templates (e.g. `<name>` -> `[de|het] {name}`).
- Flatten nested `<rule>` references.
- Add an `example:` taken from the matching test sentences.
- Delete the old `*_HassTimerStatus.yaml` sentence/test files once done.
- Run `python3 -m script.intentfest validate --language de` and the tests.
