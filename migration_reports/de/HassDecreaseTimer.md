# Migration report: de / HassDecreaseTimer

## Declared slot combinations
- `hours_only` slots: {hours} — EMPTY — non-required, safe to skip
- `minutes_only` slots: {minutes} — EMPTY — non-required, safe to skip
- `seconds_only` slots: {seconds} — EMPTY — non-required, safe to skip
- `hours_minutes` slots: {hours}, {minutes} — EMPTY — non-required, safe to skip
- `hours_seconds` slots: {hours}, {seconds} — EMPTY — non-required, safe to skip
- `minutes_seconds` slots: {minutes}, {seconds} — EMPTY — non-required, safe to skip
- `name_hours` slots: {hours}, {name} — EMPTY — non-required, safe to skip
- `name_minutes` slots: {minutes}, {name} — EMPTY — non-required, safe to skip
- `name_seconds` slots: {name}, {seconds} — EMPTY — non-required, safe to skip
- `name_hours_minutes` slots: {hours}, {minutes}, {name} — EMPTY — non-required, safe to skip
- `name_hours_seconds` slots: {hours}, {name}, {seconds} — EMPTY — non-required, safe to skip
- `area_hours` slots: {area}, {hours} — EMPTY — non-required, safe to skip
- `area_minutes` slots: {area}, {minutes} — EMPTY — non-required, safe to skip
- `area_seconds` slots: {area}, {seconds} — EMPTY — non-required, safe to skip
- `area_minutes_seconds` slots: {area}, {minutes}, {seconds} — EMPTY — non-required, safe to skip
- `area_hours_minutes` slots: {area}, {hours}, {minutes} — EMPTY — non-required, safe to skip
- `area_hours_seconds` slots: {area}, {hours}, {seconds} — EMPTY — non-required, safe to skip
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
- /home/user/intents/tests/de/HassDecreaseTimer/minutes_only.yaml
- /home/user/intents/tests/de/HassDecreaseTimer/seconds_only.yaml
- /home/user/intents/tests/de/HassDecreaseTimer/hours_only.yaml
- /home/user/intents/tests/de/HassDecreaseTimer/hours_minutes.yaml
- /home/user/intents/tests/de/HassDecreaseTimer/minutes_start_hours.yaml
- /home/user/intents/tests/de/HassDecreaseTimer/name_minutes.yaml
- /home/user/intents/tests/de/HassDecreaseTimer/area_minutes.yaml

## Old files to delete when done
(this intent may span several domain files — delete ALL of them)
- /home/user/intents/sentences/de/homeassistant_HassDecreaseTimer.yaml
- /home/user/intents/tests/de/homeassistant_HassDecreaseTimer.yaml

## Flags needing attention (17)

### complex template (15)
- `[(den|meinen|unseren) ]Timer (namens|für) {timer_name:name} um <timer_duration> <timer_decrease_end_of_sentence>` has too many slot combinations to analyze — split it by hand from the reference language.
- `<timer_decrease>[ (den|meinen|unseren)] Timer (namens|für) {timer_name:name} um <timer_duration>` has too many slot combinations to analyze — split it by hand from the reference language.
- `<timer_decrease>[ (den|meinen|unseren)] {timer_name:name} Timer um <timer_duration>` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(den|meinen|unseren) ]{timer_name:name} Timer um <timer_duration> <timer_decrease_end_of_sentence>` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(<timer_start>|{area}|{timer_name:name}) Timer ]<timer_duration> (weniger|kürzer)` has too many slot combinations to analyze — split it by hand from the reference language.
- `<timer_decrease>[ (den|meinen|unseren)] Timer um <timer_duration>` has too many slot combinations to analyze — split it by hand from the reference language.
- `<timer_decrease>[ (den|meinen|unseren)] <timer_start> Timer um <timer_duration>` has too many slot combinations to analyze — split it by hand from the reference language.
- `<timer_decrease>[ (den|meinen|unseren)] Timer für <timer_start> um <timer_duration>` has too many slot combinations to analyze — split it by hand from the reference language.
- `<timer_decrease>[ (den|meinen|unseren)] {area} Timer um <timer_duration>` has too many slot combinations to analyze — split it by hand from the reference language.
- `<timer_decrease>[ (den|meinen|unseren)] Timer <area> um <timer_duration>` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(den|meinen|unseren) ]Timer um <timer_duration> <timer_decrease_end_of_sentence>` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(den|meinen|unseren) ]<timer_start> Timer um <timer_duration> <timer_decrease_end_of_sentence>` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(den|meinen|unseren) ]Timer für <timer_start> um <timer_duration> <timer_decrease_end_of_sentence>` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(den|meinen|unseren) ]{area} Timer um <timer_duration> <timer_decrease_end_of_sentence>` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(den|meinen|unseren) ]Timer <area> um <timer_duration> <timer_decrease_end_of_sentence>` has too many slot combinations to analyze — split it by hand from the reference language.

### fixture missing (1)
- name_minutes: no entitie fixture named 'Pizza' in _fixtures.yaml.

### test unmapped (1)
- Test 'verkürze meinen Timer um 2 Stunden, 5 Minuten und 30 Sekunden' has slots ['hours', 'minutes', 'seconds'] matching no single combo.

## Reminders (see docs/syntax_migration_guide.md)
- Inline list-bearing rules in templates (e.g. `<name>` -> `[de|het] {name}`).
- Flatten nested `<rule>` references.
- Add an `example:` taken from the matching test sentences.
- Delete the old `*_HassDecreaseTimer.yaml` sentence/test files once done.
- Run `python3 -m script.intentfest validate --language de` and the tests.
