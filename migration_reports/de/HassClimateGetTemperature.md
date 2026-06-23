# Migration report: de / HassClimateGetTemperature

## Declared slot combinations
- `default` context_area: true — scaffolded
- `name_only` slots: {name} — scaffolded
- `area_only` slots: {area} — EMPTY — non-required, safe to skip
- `floor_only` slots: {floor} — EMPTY — non-required, safe to skip

## Scaffold files written
- /home/user/intents/sentences/de/HassClimateGetTemperature/default.yaml
- /home/user/intents/sentences/de/HassClimateGetTemperature/name_only.yaml
- /home/user/intents/tests/de/HassClimateGetTemperature/area_only.yaml
- /home/user/intents/tests/de/HassClimateGetTemperature/floor_only.yaml
- /home/user/intents/tests/de/HassClimateGetTemperature/default.yaml
- /home/user/intents/tests/de/HassClimateGetTemperature/name_only.yaml

## Old files to delete when done
(this intent may span several domain files — delete ALL of them)
- /home/user/intents/sentences/de/climate_HassClimateGetTemperature.yaml
- /home/user/intents/tests/de/climate_HassClimateGetTemperature.yaml

## Flags needing attention (14)

### complex template (5)
- `(Auf (<wieviel> Grad|welche [Ziel|Soll]Temperatur)|wie (warm|kalt)) ist (die Heizung|(der|das) Thermostat|die Klima[anlage])[ <hier>] [ein]gestellt` has too many slot combinations to analyze — split it by hand from the reference language.
- `(Auf (<wieviel> Grad|welche [Ziel|Soll]Temperatur)|wie (warm|kalt)) ist <hier> (die Heizung|(der|das) Thermostat|die Klima[anlage]) [ein]gestellt` has too many slot combinations to analyze — split it by hand from the reference language.
- `<wieviel> Grad (hat|sind) [es ]<area_floor>` has too many slot combinations to analyze — split it by hand from the reference language.
- `(Auf (<wieviel> Grad|welche [Ziel|Soll]Temperatur)|wie (warm|kalt)) ist[ (die Heizung|(der|das) Thermostat|die Klima[anlage])] <area_floor> [ein]gestellt` has too many slot combinations to analyze — split it by hand from the reference language.
- `(Auf (<wieviel> Grad|welche [Ziel|Soll]Temperatur)|wie (warm|kalt)) ist <area_floor> (Heizung|Thermostat|Klima[anlage]) [ein]gestellt` has too many slot combinations to analyze — split it by hand from the reference language.

### multi-combo template (9)
- `Wie[ (hoch|niedrig)] ist die Temperatur <area_floor>` matches ['area_only', 'floor_only'] — split into one template per combo.
- `Wie[ (hoch|niedrig)] ist <area_floor> die Temperatur` matches ['area_only', 'floor_only'] — split into one template per combo.
- `Wie[ (hoch|niedrig)] ist die Temperatur <von_dem> Thermostat <area_floor>` matches ['area_only', 'floor_only'] — split into one template per combo.
- `Wie[ (hoch|niedrig)] ist die Temperatur des Thermostat[s] <area_floor>` matches ['area_only', 'floor_only'] — split into one template per combo.
- `Wie (warm|kalt) ist [es ]<area_floor>` matches ['area_only', 'floor_only'] — split into one template per combo.
- `Temperatur <area_floor>` matches ['area_only', 'floor_only'] — split into one template per combo.
- `<area_floor> Temperatur` matches ['area_only', 'floor_only'] — split into one template per combo.
- `(Ziel|Soll)temperatur <area_floor>` matches ['area_only', 'floor_only'] — split into one template per combo.
- `<area_floor> (Ziel|Soll)temperatur` matches ['area_only', 'floor_only'] — split into one template per combo.

## Reminders (see docs/syntax_migration_guide.md)
- Inline list-bearing rules in templates (e.g. `<name>` -> `[de|het] {name}`).
- Flatten nested `<rule>` references.
- Add an `example:` taken from the matching test sentences.
- Delete the old `*_HassClimateGetTemperature.yaml` sentence/test files once done.
- Run `python3 -m script.intentfest validate --language de` and the tests.
