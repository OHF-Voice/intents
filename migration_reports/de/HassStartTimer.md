# Migration report: de / HassStartTimer

## Declared slot combinations
- `hours_only` slots: {hours} — EMPTY — non-required, safe to skip
- `minutes_only` slots: {minutes} — EMPTY — non-required, safe to skip
- `seconds_only` slots: {seconds} — EMPTY — non-required, safe to skip
- `hours_minutes` slots: {hours}, {minutes} — EMPTY — non-required, safe to skip
- `hours_seconds` slots: {hours}, {seconds} — EMPTY — non-required, safe to skip
- `minutes_seconds` slots: {minutes}, {seconds} — EMPTY — non-required, safe to skip
- `hours_minutes_seconds` slots: {hours}, {minutes}, {seconds} — EMPTY — non-required, safe to skip
- `name_hours` slots: {hours}, {name} — EMPTY — non-required, safe to skip
- `name_minutes` slots: {minutes}, {name} — EMPTY — non-required, safe to skip
- `name_seconds` slots: {name}, {seconds} — EMPTY — non-required, safe to skip
- `name_hours_minutes` slots: {hours}, {minutes}, {name} — EMPTY — non-required, safe to skip
- `name_hours_seconds` slots: {hours}, {name}, {seconds} — EMPTY — non-required, safe to skip
- `name_minutes_seconds` slots: {minutes}, {name}, {seconds} — EMPTY — non-required, safe to skip
- `name_hours_minutes_seconds` slots: {hours}, {minutes}, {name}, {seconds} — EMPTY — non-required, safe to skip
- `command_hours` slots: {conversation_command}, {hours} — EMPTY — non-required, safe to skip
- `command_minutes` slots: {conversation_command}, {minutes} — EMPTY — non-required, safe to skip
- `command_seconds` slots: {conversation_command}, {seconds} — EMPTY — non-required, safe to skip
- `command_hours_minutes` slots: {conversation_command}, {hours}, {minutes} — EMPTY — non-required, safe to skip
- `command_hours_seconds` slots: {conversation_command}, {hours}, {seconds} — EMPTY — non-required, safe to skip
- `command_minutes_seconds` slots: {conversation_command}, {minutes}, {seconds} — EMPTY — non-required, safe to skip
- `command_hours_minutes_seconds` slots: {conversation_command}, {hours}, {minutes}, {seconds} — EMPTY — non-required, safe to skip

## Scaffold files written
- /home/user/intents/tests/de/HassStartTimer/hours_only.yaml
- /home/user/intents/tests/de/HassStartTimer/command_minutes.yaml
- /home/user/intents/tests/de/HassStartTimer/command_hours_minutes.yaml
- /home/user/intents/tests/de/HassStartTimer/command_seconds.yaml

## Old files to delete when done
(this intent may span several domain files — delete ALL of them)
- /home/user/intents/sentences/de/homeassistant_HassStartTimer.yaml
- /home/user/intents/tests/de/homeassistant_HassStartTimer.yaml

## Flags needing attention (59)

### complex template (18)
- `[einen ]Timer[ (auf|für)] <timer_duration> [<timer_set_end_of_sentence> ]für[ (<possessivpronom_mein>|<possessivpronom_unser>|<artikel_bestimmt>)] {timer_name:name}` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(<timer_set> [einen ]|einen )]Timer (namens|für[ (<possessivpronom_mein>|<possessivpronom_unser>|<artikel_bestimmt>)]) {timer_name:name} (auf|für) <timer_duration>` has too many slot combinations to analyze — split it by hand from the reference language.
- `[einen ]Timer[ (auf|für)] <timer_duration> für[ (<possessivpronom_mein>|<possessivpronom_unser>|<artikel_bestimmt>)] {timer_name:name} <timer_set_end_of_sentence>` has too many slot combinations to analyze — split it by hand from the reference language.
- `<timer_set>[ einen] Timer (auf|für) <timer_duration> (namens|für[ (<possessivpronom_mein>|<possessivpronom_unser>|<artikel_bestimmt>)]) {timer_name:name}` has too many slot combinations to analyze — split it by hand from the reference language.
- `[einen ]Timer[ (auf|für)] <timer_duration> namens {timer_name:name}[ <timer_set_end_of_sentence>]` has too many slot combinations to analyze — split it by hand from the reference language.
- `<timer_set> einen Timer (auf|für) <timer_duration> und ([be]nenne|nenn) ihn {timer_name:name}` has too many slot combinations to analyze — split it by hand from the reference language.
- `[einen ]Timer (auf|für) <timer_duration> <timer_set_end_of_sentence> und ihn {timer_name:name} nennen` has too many slot combinations to analyze — split it by hand from the reference language.
- `[einen ]{timer_name:name} Timer[ (auf|für)] <timer_duration>[ <timer_set_end_of_sentence>]` has too many slot combinations to analyze — split it by hand from the reference language.
- `<timer_set>[ einen] <timer_duration> Timer (namens|für[ (<possessivpronom_mein>|<possessivpronom_unser>|<artikel_bestimmt>)]) {timer_name:name}` has too many slot combinations to analyze — split it by hand from the reference language.
- `[einen ]{timer_name:name} Timer <timer_set_end_of_sentence> (auf|für) <timer_duration>` has too many slot combinations to analyze — split it by hand from the reference language.
- `<timer_set>[ einen] {timer_name:name} Timer (auf|für) <timer_duration>` has too many slot combinations to analyze — split it by hand from the reference language.
- `[einen ]<timer_duration> Timer für {timer_name:name}[ <timer_set_end_of_sentence>]` has too many slot combinations to analyze — split it by hand from the reference language.
- `[einen ]<timer_duration> Timer <timer_set_end_of_sentence> für {timer_name:name}` has too many slot combinations to analyze — split it by hand from the reference language.
- `[einen ]<timer_duration> Timer[ <timer_set_end_of_sentence>]` has too many slot combinations to analyze — split it by hand from the reference language.
- `[einen ]Timer[ (auf|für)] <timer_duration>[ <timer_set_end_of_sentence>]` has too many slot combinations to analyze — split it by hand from the reference language.
- `<timer_set>[ einen] <timer_duration> Timer` has too many slot combinations to analyze — split it by hand from the reference language.
- `<timer_set>[ einen] Timer (auf|für) <timer_duration>` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(mach[e]|fahr[e]|schalt[e]) ](in|nach) <timer_duration> {timer_command:conversation_command}` has too many slot combinations to analyze — split it by hand from the reference language.

### multi-combo template (2)
- `<stelle> einen <timer_duration> Timer ein` matches ['hours_minutes', 'hours_minutes_seconds', 'hours_only', 'hours_seconds', 'minutes_only', 'minutes_seconds', 'seconds_only'] — split into one template per combo.
- `{timer_command:conversation_command} (in|nach) <timer_duration>` matches ['command_hours', 'command_hours_minutes', 'command_hours_minutes_seconds', 'command_hours_seconds', 'command_minutes', 'command_minutes_seconds', 'command_seconds'] — split into one template per combo.

### test unmapped (39)
- Test 'Starte einen 1 Stunde Timer' has slots ['__context_area__', 'hours'] matching no single combo.
- Test 'Starte einen 1 Stunde und 15 Minuten Timer' has slots ['__context_area__', 'hours', 'minutes'] matching no single combo.
- Test 'Starte einen 1 Stunde und 30 Sekunden Timer' has slots ['__context_area__', 'hours', 'seconds'] matching no single combo.
- Test 'Starte einen 1 Stunde 15 Minuten und 30 Sekunden timer' has slots ['__context_area__', 'hours', 'minutes', 'seconds'] matching no single combo.
- Test 'Starte einen 5 Minuten Timer' has slots ['__context_area__', 'minutes'] matching no single combo.
- Test 'einen 5 Minuten Timer für Pizza' has slots ['__context_area__', 'minutes', 'name'] matching no single combo.
- Test 'Timer für 5 Minuten für den Auflauf' has slots ['__context_area__', 'minutes', 'name'] matching no single combo.
- Test 'Starte einen 5 Minuten und 10 Sekunden Timer' has slots ['__context_area__', 'minutes', 'seconds'] matching no single combo.
- Test 'Starte einen 45 Sekunden Timer' has slots ['__context_area__', 'seconds'] matching no single combo.
- Test 'Stelle einen Pizza Timer für 5 Minuten' has slots ['__context_area__', 'minutes', 'name'] matching no single combo.
- Test 'Timer für eine viertel Stunde' has slots ['__context_area__', 'minutes'] matching no single combo.
- Test 'Timer für eine halbe Stunde' has slots ['__context_area__', 'minutes'] matching no single combo.
- Test 'Timer für eine drei viertel Stunde' has slots ['__context_area__', 'minutes'] matching no single combo.
- Test 'stelle einen Timer für den Kuchen auf eine dreiviertel Stunde' has slots ['__context_area__', 'minutes', 'name'] matching no single combo.
- Test 'Timer für ein einviertel Stunden' has slots ['__context_area__', 'minutes'] matching no single combo.
- Test 'Timer für eineinviertel Stunden' has slots ['__context_area__', 'minutes'] matching no single combo.
- Test 'Timer für ein einhalb Stunden' has slots ['__context_area__', 'minutes'] matching no single combo.
- Test 'Timer für anderthalb Stunden' has slots ['__context_area__', 'minutes'] matching no single combo.
- Test 'Timer für ein dreiviertel Stunden' has slots ['__context_area__', 'minutes'] matching no single combo.
- Test 'Timer für ein drei viertel Stunden' has slots ['__context_area__', 'minutes'] matching no single combo.
- Test 'Timer für zwei einhalb Stunden' has slots ['__context_area__', 'minutes'] matching no single combo.
- Test 'Timer für zweieinhalb Stunden' has slots ['__context_area__', 'minutes'] matching no single combo.
- Test 'Timer für drei einhalb Stunden' has slots ['__context_area__', 'minutes'] matching no single combo.
- Test 'Timer für dreieinhalb Stunden' has slots ['__context_area__', 'minutes'] matching no single combo.
- Test 'Timer für vier einhalb Stunden' has slots ['__context_area__', 'minutes'] matching no single combo.
- Test 'Timer für viereinhalb Stunden' has slots ['__context_area__', 'minutes'] matching no single combo.
- Test 'Timer für eine halbe Minute' has slots ['__context_area__', 'seconds'] matching no single combo.
- Test 'Timer für eine halbe minute' has slots ['__context_area__', 'seconds'] matching no single combo.
- Test 'Timer für eineinhalb Minuten' has slots ['__context_area__', 'seconds'] matching no single combo.
- Test 'Timer für anderthalb Minuten' has slots ['__context_area__', 'seconds'] matching no single combo.
- Test 'Timer für zweieinhalb Minuten' has slots ['__context_area__', 'seconds'] matching no single combo.
- Test 'Timer für dreieinhalb Minuten' has slots ['__context_area__', 'seconds'] matching no single combo.
- Test 'Timer für vier einhalb Minuten' has slots ['__context_area__', 'seconds'] matching no single combo.
- Test 'Timer für fünfeinhalb Minuten' has slots ['__context_area__', 'seconds'] matching no single combo.
- Test 'Timer für sechs ein halb Minuten' has slots ['__context_area__', 'seconds'] matching no single combo.
- Test 'Timer für siebeneinhalb Minuten' has slots ['__context_area__', 'seconds'] matching no single combo.
- Test 'Timer für achteinhalb Minuten' has slots ['__context_area__', 'seconds'] matching no single combo.
- Test 'Timer für neuneinhalb Minuten' has slots ['__context_area__', 'seconds'] matching no single combo.
- Test 'Timer für neuneinhalb minuten' has slots ['__context_area__', 'seconds'] matching no single combo.

## Reminders (see docs/syntax_migration_guide.md)
- Inline list-bearing rules in templates (e.g. `<name>` -> `[de|het] {name}`).
- Flatten nested `<rule>` references.
- Add an `example:` taken from the matching test sentences.
- Delete the old `*_HassStartTimer.yaml` sentence/test files once done.
- Run `python3 -m script.intentfest validate --language de` and the tests.
