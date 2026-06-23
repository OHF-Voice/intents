# Migration report: de / HassFanSetSpeed

## Declared slot combinations
- `default` slots: {percentage}; context_area: true — scaffolded
- `name_only` slots: {name}, {percentage} — scaffolded
- `area_only` slots: {area}, {percentage} — EMPTY — non-required, safe to skip
- `floor_only` slots: {floor}, {percentage} — EMPTY — non-required, safe to skip

## Scaffold files written
- /home/user/intents/sentences/de/HassFanSetSpeed/default.yaml
- /home/user/intents/sentences/de/HassFanSetSpeed/name_only.yaml
- /home/user/intents/tests/de/HassFanSetSpeed/default.yaml
- /home/user/intents/tests/de/HassFanSetSpeed/name_only.yaml
- /home/user/intents/tests/de/HassFanSetSpeed/area_only.yaml
- /home/user/intents/tests/de/HassFanSetSpeed/floor_only.yaml

## Old files to delete when done
(this intent may span several domain files — delete ALL of them)
- /home/user/intents/sentences/de/fan_HassFanSetSpeed.yaml
- /home/user/intents/tests/de/fan_HassFanSetSpeed.yaml

## Flags needing attention (8)

### complex template (5)
- `[<setzen> [die ]]Geschwindigkeit (<luefter>|<luefter_genitiv>)[ <hier>] (auf|zu) <fan_speed>` has too many slot combinations to analyze — split it by hand from the reference language.
- `[Geschwindigkeit ](<luefter>|<luefter_genitiv>)[ <hier>][ auf] <fan_speed>[ <setzen_end_of_sentence>]` has too many slot combinations to analyze — split it by hand from the reference language.
- `[<setzen> [die ]]Geschwindigkeit (<luefter>|<luefter_genitiv>) <area_floor> (auf|zu) <fan_speed>` has too many slot combinations to analyze — split it by hand from the reference language.
- `<stelle> [die ]Geschwindigkeit (<luefter>|<luefter_genitiv>) <area_floor> auf <fan_speed> ein` has too many slot combinations to analyze — split it by hand from the reference language.
- `[Geschwindigkeit ](<luefter>|<luefter_genitiv>) <area_floor>[ auf] <fan_speed>[ <setzen_end_of_sentence>]` has too many slot combinations to analyze — split it by hand from the reference language.

### response default (2)
- `default`: old sentences had no `response`; defaulted to `default` — confirm the right response.
- `name_only`: old sentences had no `response`; defaulted to `default` — confirm the right response.

### unresolved rule (1)
- `<fan_speed>` is not in rules/de/ — inline it into the templates or move it there (the test harness ignores _common.yaml).

## Reminders (see docs/syntax_migration_guide.md)
- Inline list-bearing rules in templates (e.g. `<name>` -> `[de|het] {name}`).
- Flatten nested `<rule>` references.
- Add an `example:` taken from the matching test sentences.
- Delete the old `*_HassFanSetSpeed.yaml` sentence/test files once done.
- Run `python3 -m script.intentfest validate --language de` and the tests.
