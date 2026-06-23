# Migration report: de / HassClimateSetTemperature

## Declared slot combinations
- `temperature_only` slots: {temperature}; context_area: true — scaffolded
- `name_temperature` slots: {name}, {temperature} — scaffolded
- `area_temperature` slots: {area}, {temperature} — scaffolded
- `floor_temperature` slots: {floor}, {temperature} — EMPTY — non-required, safe to skip

## Scaffold files written
- /home/user/intents/sentences/de/HassClimateSetTemperature/name_temperature.yaml
- /home/user/intents/sentences/de/HassClimateSetTemperature/area_temperature.yaml
- /home/user/intents/sentences/de/HassClimateSetTemperature/temperature_only.yaml
- /home/user/intents/tests/de/HassClimateSetTemperature/area_temperature.yaml
- /home/user/intents/tests/de/HassClimateSetTemperature/floor_temperature.yaml
- /home/user/intents/tests/de/HassClimateSetTemperature/temperature_only.yaml
- /home/user/intents/tests/de/HassClimateSetTemperature/name_temperature.yaml

## Old files to delete when done
(this intent may span several domain files — delete ALL of them)
- /home/user/intents/sentences/de/climate_HassClimateSetTemperature.yaml
- /home/user/intents/tests/de/climate_HassClimateSetTemperature.yaml

## Flags needing attention (33)

### complex template (25)
- `<setzen> <heizung> <von_dem> <name> auf <temperature>` has too many slot combinations to analyze — split it by hand from the reference language.
- `<setzen> <heizung> <name>[s] auf <temperature>` has too many slot combinations to analyze — split it by hand from the reference language.
- `<heizung> [<von_dem> ]<name> auf <temperature>[ <setzen_end_of_sentence>]` has too many slot combinations to analyze — split it by hand from the reference language.
- `<heizung> <area_floor> auf <temperature>[ <setzen_end_of_sentence>]` has too many slot combinations to analyze — split it by hand from the reference language.
- `<floor> auf <temperature> <heat_cool>` has too many slot combinations to analyze — split it by hand from the reference language.
- `<setzen> <area_floor> <heizung> auf <temperature>` has too many slot combinations to analyze — split it by hand from the reference language.
- `<stelle> <area_floor> <heizung> auf <temperature> ein` has too many slot combinations to analyze — split it by hand from the reference language.
- `<setzen> <heizung> <area_floor> auf <temperature>` has too many slot combinations to analyze — split it by hand from the reference language.
- `<stelle> <heizung> <area_floor> auf <temperature> ein` has too many slot combinations to analyze — split it by hand from the reference language.
- `<area_floor> <temperature>` has too many slot combinations to analyze — split it by hand from the reference language.
- `heiz[e] <area> auf <temperature>[ auf]` has too many slot combinations to analyze — split it by hand from the reference language.
- `heiz[e] <floor> auf <temperature>[ auf]` has too many slot combinations to analyze — split it by hand from the reference language.
- `kühl[e] <area> auf <temperature>[ (ab|[he]runter)]` has too many slot combinations to analyze — split it by hand from the reference language.
- `kühl[e] <floor> auf <temperature>[ (ab|[he]runter)]` has too many slot combinations to analyze — split it by hand from the reference language.
- `[<hier> ]<heizung> auf <temperature>[ <setzen_end_of_sentence>]` has too many slot combinations to analyze — split it by hand from the reference language.
- `<heizung> <hier> auf <temperature>[ <setzen_end_of_sentence>]` has too many slot combinations to analyze — split it by hand from the reference language.
- `<heizung> auf <temperature> <hier>[ <setzen_end_of_sentence>]` has too many slot combinations to analyze — split it by hand from the reference language.
- `<setzen>[ <hier>] <heizung> auf <temperature>` has too many slot combinations to analyze — split it by hand from the reference language.
- `<setzen> <heizung> <hier> auf <temperature>` has too many slot combinations to analyze — split it by hand from the reference language.
- `<setzen> <heizung> auf <temperature> <hier>` has too many slot combinations to analyze — split it by hand from the reference language.
- `heiz[e][ <hier>] auf <temperature>[ auf]` has too many slot combinations to analyze — split it by hand from the reference language.
- `heiz[e] auf <temperature> <hier>[ auf]` has too many slot combinations to analyze — split it by hand from the reference language.
- `kühl[e][ <hier>] auf <temperature>[ (ab|[he]runter)]` has too many slot combinations to analyze — split it by hand from the reference language.
- `kühl[e] auf <temperature> <hier>[ (ab|[he]runter)]` has too many slot combinations to analyze — split it by hand from the reference language.
- `kühl[e] auf <temperature> (ab|[he]runter) <hier>` has too many slot combinations to analyze — split it by hand from the reference language.

### multi-combo template (3)
- `<setzen> (<area_heizung>|<floor_heizung>) auf <temperature>` matches ['area_temperature', 'floor_temperature'] — split into one template per combo.
- `<stelle> (<area_heizung>|<floor_heizung>) auf <temperature> ein` matches ['area_temperature', 'floor_temperature'] — split into one template per combo.
- `(<area_heizung>|<floor_heizung>) auf <temperature>[ <setzen_end_of_sentence>]` matches ['area_temperature', 'floor_temperature'] — split into one template per combo.

### response default (3)
- `name_temperature`: old sentences had no `response`; defaulted to `default` — confirm the right response.
- `area_temperature`: old sentences had no `response`; defaulted to `default` — confirm the right response.
- `temperature_only`: old sentences had no `response`; defaulted to `default` — confirm the right response.

### unresolved rule (2)
- `<heat_cool>` is not in rules/de/ — inline it into the templates or move it there (the test harness ignores _common.yaml).
- `<heizung>` is not in rules/de/ — inline it into the templates or move it there (the test harness ignores _common.yaml).

## Reminders (see docs/syntax_migration_guide.md)
- Inline list-bearing rules in templates (e.g. `<name>` -> `[de|het] {name}`).
- Flatten nested `<rule>` references.
- Add an `example:` taken from the matching test sentences.
- Delete the old `*_HassClimateSetTemperature.yaml` sentence/test files once done.
- Run `python3 -m script.intentfest validate --language de` and the tests.
