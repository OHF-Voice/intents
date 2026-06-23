# Migration report: de / HassIncreaseTimer

## Declared slot combinations
- `hours_only` slots: {hours} — EMPTY — non-required, safe to skip
- `minutes_only` slots: {minutes} — EMPTY — non-required, safe to skip
- `seconds_only` slots: {seconds} — EMPTY — non-required, safe to skip
- `minutes_seconds` slots: {minutes}, {seconds} — EMPTY — non-required, safe to skip
- `hours_minutes` slots: {hours}, {minutes} — EMPTY — non-required, safe to skip
- `name_hours` slots: {hours}, {name} — EMPTY — non-required, safe to skip
- `name_minutes` slots: {minutes}, {name} — EMPTY — non-required, safe to skip
- `name_seconds` slots: {name}, {seconds} — EMPTY — non-required, safe to skip
- `area_hours` slots: {area}, {hours} — EMPTY — non-required, safe to skip
- `area_minutes` slots: {area}, {minutes} — EMPTY — non-required, safe to skip
- `area_seconds` slots: {area}, {seconds} — EMPTY — non-required, safe to skip
- `hours_start_hours` slots: {hours}, {start_hours} — EMPTY — non-required, safe to skip
- `hours_start_minutes` slots: {hours}, {start_minutes} — EMPTY — non-required, safe to skip
- `hours_start_seconds` slots: {hours}, {start_seconds} — EMPTY — non-required, safe to skip
- `minutes_start_hours` slots: {minutes}, {start_hours} — EMPTY — non-required, safe to skip
- `minutes_start_minutes` slots: {minutes}, {start_minutes} — EMPTY — non-required, safe to skip
- `minutes_start_seconds` slots: {minutes}, {start_seconds} — EMPTY — non-required, safe to skip
- `seconds_start_hours` slots: {seconds}, {start_hours} — EMPTY — non-required, safe to skip
- `seconds_start_minutes` slots: {seconds}, {start_minutes} — EMPTY — non-required, safe to skip
- `seconds_start_seconds` slots: {seconds}, {start_seconds} — EMPTY — non-required, safe to skip

## Scaffold files written
- /home/user/intents/tests/de/HassIncreaseTimer/minutes_only.yaml
- /home/user/intents/tests/de/HassIncreaseTimer/seconds_only.yaml
- /home/user/intents/tests/de/HassIncreaseTimer/hours_only.yaml
- /home/user/intents/tests/de/HassIncreaseTimer/hours_minutes.yaml
- /home/user/intents/tests/de/HassIncreaseTimer/minutes_start_hours.yaml
- /home/user/intents/tests/de/HassIncreaseTimer/name_minutes.yaml
- /home/user/intents/tests/de/HassIncreaseTimer/area_minutes.yaml

## Old files to delete when done
(this intent may span several domain files — delete ALL of them)
- /home/user/intents/sentences/de/homeassistant_HassIncreaseTimer.yaml
- /home/user/intents/tests/de/homeassistant_HassIncreaseTimer.yaml

## Flags needing attention (17)

### complex template (7)
- `[(<timer_start>|{area}|{timer_name:name}) Timer ]<timer_duration> (mehr|länger)` has too many slot combinations to analyze — split it by hand from the reference language.
- `verlängere[ (den|meinen|unseren)] <timer_start> Timer um <timer_duration>` has too many slot combinations to analyze — split it by hand from the reference language.
- `verlängere[ (den|meinen|unseren)] Timer für <timer_start> um <timer_duration>` has too many slot combinations to analyze — split it by hand from the reference language.
- `verlängere[ (den|meinen|unseren)] Timer <area> um <timer_duration>` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(den|meinen|unseren) ]<timer_start> Timer um <timer_duration> verlängern` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(den|meinen|unseren) ]Timer für <timer_start> um <timer_duration> verlängern` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(den|meinen|unseren) ]Timer <area> um <timer_duration> verlängern` has too many slot combinations to analyze — split it by hand from the reference language.

### fixture missing (1)
- name_minutes: no entitie fixture named 'Pizza' in _fixtures.yaml.

### multi-combo template (8)
- `verlängere[ (den|meinen|unseren)] Timer (namens|für) {timer_name:name} um <timer_duration>` matches ["?['hours', 'minutes', 'name', 'seconds']", "?['hours', 'minutes', 'name']", "?['hours', 'name', 'seconds']", "?['minutes', 'name', 'seconds']", 'name_hours', 'name_minutes', 'name_seconds'] — split into one template per combo.
- `[(den|meinen|unseren) ]Timer (namens|für) {timer_name:name} um <timer_duration> verlängern` matches ["?['hours', 'minutes', 'name', 'seconds']", "?['hours', 'minutes', 'name']", "?['hours', 'name', 'seconds']", "?['minutes', 'name', 'seconds']", 'name_hours', 'name_minutes', 'name_seconds'] — split into one template per combo.
- `verlängere[ (den|meinen|unseren)] {timer_name:name} Timer um <timer_duration>` matches ["?['hours', 'minutes', 'name', 'seconds']", "?['hours', 'minutes', 'name']", "?['hours', 'name', 'seconds']", "?['minutes', 'name', 'seconds']", 'name_hours', 'name_minutes', 'name_seconds'] — split into one template per combo.
- `[(den|meinen|unseren) ]{timer_name:name} Timer um <timer_duration> verlängern` matches ["?['hours', 'minutes', 'name', 'seconds']", "?['hours', 'minutes', 'name']", "?['hours', 'name', 'seconds']", "?['minutes', 'name', 'seconds']", 'name_hours', 'name_minutes', 'name_seconds'] — split into one template per combo.
- `verlängere[ (den|meinen|unseren)] Timer um <timer_duration>` matches ["?['hours', 'minutes', 'seconds']", "?['hours', 'seconds']", 'hours_minutes', 'hours_only', 'minutes_only', 'minutes_seconds', 'seconds_only'] — split into one template per combo.
- `verlängere[ (den|meinen|unseren)] {area} Timer um <timer_duration>` matches ["?['area', 'hours', 'minutes', 'seconds']", "?['area', 'hours', 'minutes']", "?['area', 'hours', 'seconds']", "?['area', 'minutes', 'seconds']", 'area_hours', 'area_minutes', 'area_seconds'] — split into one template per combo.
- `[(den|meinen|unseren) ]Timer um <timer_duration> verlängern` matches ["?['hours', 'minutes', 'seconds']", "?['hours', 'seconds']", 'hours_minutes', 'hours_only', 'minutes_only', 'minutes_seconds', 'seconds_only'] — split into one template per combo.
- `[(den|meinen|unseren) ]{area} Timer um <timer_duration> verlängern` matches ["?['area', 'hours', 'minutes', 'seconds']", "?['area', 'hours', 'minutes']", "?['area', 'hours', 'seconds']", "?['area', 'minutes', 'seconds']", 'area_hours', 'area_minutes', 'area_seconds'] — split into one template per combo.

### test unmapped (1)
- Test 'verlängere meinen Timer um 2 Stunden, 5 Minuten und 30 Sekunden' has slots ['hours', 'minutes', 'seconds'] matching no single combo.

## Reminders (see docs/syntax_migration_guide.md)
- Inline list-bearing rules in templates (e.g. `<name>` -> `[de|het] {name}`).
- Flatten nested `<rule>` references.
- Add an `example:` taken from the matching test sentences.
- Delete the old `*_HassIncreaseTimer.yaml` sentence/test files once done.
- Run `python3 -m script.intentfest validate --language de` and the tests.
