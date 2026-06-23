# Migration report: de / HassSetPosition

## Declared slot combinations
- `name_only` slots: {name}, {position} — scaffolded
- `device_class` slots: {device_class}, {domain}, {position}; context_area: true — EMPTY — non-required, safe to skip
- `area_device_class` slots: {area}, {device_class}, {domain}, {position} — EMPTY — non-required, safe to skip

## Scaffold files written
- /home/user/intents/sentences/de/HassSetPosition/name_only.yaml
- /home/user/intents/tests/de/HassSetPosition/name_only.yaml

## Old files to delete when done
(this intent may span several domain files — delete ALL of them)
- /home/user/intents/sentences/de/cover_HassSetPosition.yaml
- /home/user/intents/sentences/de/homeassistant_HassSetPosition.yaml
- /home/user/intents/tests/de/cover_HassSetPosition.yaml
- /home/user/intents/tests/de/homeassistant_HassSetPosition.yaml

## Flags needing attention (35)

### complex template (24)
- `<schliessen> <area_floor> <abdeckung> auf <position>` has too many slot combinations to analyze — split it by hand from the reference language.
- `<schliessen> <abdeckung> <area_floor> auf <position>` has too many slot combinations to analyze — split it by hand from the reference language.
- `<abdeckung> <area_floor> auf <position> <schliessen_end_of_sentence>` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<machen>|<fahren>|<setzen>) <area_floor> <abdeckung> auf <position>` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<machen>|<fahren>|<setzen>) <abdeckung> <area_floor> auf <position>` has too many slot combinations to analyze — split it by hand from the reference language.
- `<abdeckung> <area_floor> auf <position>[ (machen|fahren|<setzen_end_of_sentence>)]` has too many slot combinations to analyze — split it by hand from the reference language.
- `<schliessen> <area_floor> <alle_abdeckungen> auf <position>` has too many slot combinations to analyze — split it by hand from the reference language.
- `<schliessen> <alle_abdeckungen> <area_floor> auf <position>` has too many slot combinations to analyze — split it by hand from the reference language.
- `<alle_abdeckungen> <area_floor> auf <position> <schliessen_end_of_sentence>` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<machen>|<fahren>|<setzen>) <area_floor> <alle_abdeckungen> auf <position>` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<machen>|<fahren>|<setzen>) <alle_abdeckungen> <area_floor> auf <position>` has too many slot combinations to analyze — split it by hand from the reference language.
- `<alle_abdeckungen> <area_floor> auf <position>[ (machen|fahren|<setzen_end_of_sentence>)]` has too many slot combinations to analyze — split it by hand from the reference language.
- `<schliessen>[ <hier>] <abdeckung> auf <position>` has too many slot combinations to analyze — split it by hand from the reference language.
- `<schliessen> <abdeckung> [ <hier>]auf <position>` has too many slot combinations to analyze — split it by hand from the reference language.
- `<abdeckung> [ <hier>] auf <position> <schliessen_end_of_sentence>` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<machen>|<fahren>|<setzen>) [ <hier>] <abdeckung> auf <position>` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<machen>|<fahren>|<setzen>) <abdeckung> [ <hier>] auf <position>` has too many slot combinations to analyze — split it by hand from the reference language.
- `<abdeckung> [ <hier>] auf <position>[ (machen|fahren|<setzen_end_of_sentence>)]` has too many slot combinations to analyze — split it by hand from the reference language.
- `<setze> [die ]Position[ von] <name>[ auf] <position>` has too many slot combinations to analyze — split it by hand from the reference language.
- `<stelle> [die ]Position[ von] <name>[ auf] <position>[ ein]` has too many slot combinations to analyze — split it by hand from the reference language.
- `[die ]Position[ von] <name>[ auf] <position>[ <setzen_end_of_sentence>]` has too many slot combinations to analyze — split it by hand from the reference language.
- `<setze> [die ]Position[ <von_dem>] <name> auf [(die|das) ]{position_level:position}[ Stufe]` has too many slot combinations to analyze — split it by hand from the reference language.
- `<stelle> [die ]Position[ <von_dem>] <name> auf [(die|das) ]{position_level:position}[ Stufe][ ein]` has too many slot combinations to analyze — split it by hand from the reference language.
- `[die ]Position[ <von_dem>] <name> auf [(die|das) ]{position_level:position}[ Stufe] <setzen_end_of_sentence>` has too many slot combinations to analyze — split it by hand from the reference language.

### response default (2)
- `name_only`: old sentences had no `response`; defaulted to `default` — confirm the right response.
- `name_only`: old sentences had no `response`; defaulted to `default` — confirm the right response.

### test unmapped (6)
- Test 'fahre das Rollo rechts auf 10%' has slots ['domain', 'name', 'position'] matching no single combo.
- Test 'mache im Schlafzimmer den Vorhang auf 20%' has slots ['area', 'domain', 'position'] matching no single combo.
- Test 'mache im Erdgeschoss den Vorhang auf 20%' has slots ['domain', 'floor', 'position'] matching no single combo.
- Test 'mache im Schlafzimmer alle Rollläden auf 20%' has slots ['area', 'domain', 'position'] matching no single combo.
- Test 'mache im Erdgeschoss alle Rollläden auf 20%' has slots ['domain', 'floor', 'position'] matching no single combo.
- Test 'mache den Vorhang auf 20%' has slots ['__context_area__', 'domain', 'position'] matching no single combo.

### unmapped signature (3)
- `(öffne|<schliessen>|<machen>|<fahren>|<setzen>) <name> auf <position>` has slots ['domain', 'name', 'position'] which match no single declared combo — check intents.yaml / domain.
- `<name> auf <position> (öffnen|<schliessen>|machen|fahren|setzen|stellen)` has slots ['domain', 'name', 'position'] which match no single declared combo — check intents.yaml / domain.
- `position von <name> auf <position>[ <setzen_end_of_sentence>]` has slots ['domain', 'name', 'position'] which match no single declared combo — check intents.yaml / domain.

## Reminders (see docs/syntax_migration_guide.md)
- Inline list-bearing rules in templates (e.g. `<name>` -> `[de|het] {name}`).
- Flatten nested `<rule>` references.
- Add an `example:` taken from the matching test sentences.
- Delete the old `*_HassSetPosition.yaml` sentence/test files once done.
- Run `python3 -m script.intentfest validate --language de` and the tests.
