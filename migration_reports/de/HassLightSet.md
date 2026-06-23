# Migration report: de / HassLightSet

## Declared slot combinations
- `name_brightness` slots: {brightness}, {name} — scaffolded
- `name_color` slots: {color}, {name} — scaffolded
- `name_temperature` slots: {name}, {temperature} — scaffolded
- `brightness_only` slots: {brightness}, {domain}; context_area: true — EMPTY — non-required, safe to skip
- `area_brightness` slots: {area}, {brightness}, {domain} — EMPTY — non-required, safe to skip
- `floor_brightness` slots: {brightness}, {domain}, {floor} — EMPTY — non-required, safe to skip
- `color_only` slots: {color}, {domain}; context_area: true — EMPTY — non-required, safe to skip
- `area_color` slots: {area}, {color}, {domain} — EMPTY — non-required, safe to skip
- `floor_color` slots: {color}, {domain}, {floor} — EMPTY — non-required, safe to skip
- `temperature_only` slots: {domain}, {temperature}; context_area: true — EMPTY — non-required, safe to skip
- `area_temperature` slots: {area}, {domain}, {temperature} — EMPTY — non-required, safe to skip
- `floor_temperature` slots: {domain}, {floor}, {temperature} — EMPTY — non-required, safe to skip

## Scaffold files written
- /home/user/intents/sentences/de/HassLightSet/name_brightness.yaml
- /home/user/intents/sentences/de/HassLightSet/name_color.yaml
- /home/user/intents/sentences/de/HassLightSet/name_temperature.yaml
- /home/user/intents/tests/de/HassLightSet/name_brightness.yaml
- /home/user/intents/tests/de/HassLightSet/name_color.yaml
- /home/user/intents/tests/de/HassLightSet/name_temperature.yaml

## Old files to delete when done
(this intent may span several domain files — delete ALL of them)
- /home/user/intents/sentences/de/light_HassLightSet.yaml
- /home/user/intents/tests/de/light_HassLightSet.yaml

## Flags needing attention (90)

### complex template (71)
- `<setze> [die ]Helligkeit[ (von|vom)] <name>[ auf] <brightness>` has too many slot combinations to analyze — split it by hand from the reference language.
- `<stelle> [die ]Helligkeit[ (von|vom)] <name>[ auf] <brightness>[ ein]` has too many slot combinations to analyze — split it by hand from the reference language.
- `[die ]Helligkeit[ (von|vom)] <name>[ auf] <brightness>[ (<setzen_end_of_sentence>|dimmen)]` has too many slot combinations to analyze — split it by hand from the reference language.
- `<setze> [die ]Helligkeit[ (von|vom)] <name> auf [(die|das) ]{brightness_level:brightness}[ Stufe]` has too many slot combinations to analyze — split it by hand from the reference language.
- `<stelle> [die ]Helligkeit[ (von|vom)] <name> auf [(die|das) ]{brightness_level:brightness}[ Stufe][ ein]` has too many slot combinations to analyze — split it by hand from the reference language.
- `[die ]Helligkeit[ (von|vom)] <name>[ auf[ (die|das)]] {brightness_level:brightness}[ Stufe][ (<setzen_end_of_sentence>|dimmen)]` has too many slot combinations to analyze — split it by hand from the reference language.
- `<setze> [die ]Helligkeit[ (<licht_ohne_artikel>|<lichtes_mit_artikel>|<lichter>|<alle_lichter>)] <area_floor> auf <brightness>` has too many slot combinations to analyze — split it by hand from the reference language.
- `[die ]Helligkeit[ (<licht_ohne_artikel>|<lichtes_mit_artikel>|<lichter>|<alle_lichter>)] <area_floor>[ auf] <brightness>` has too many slot combinations to analyze — split it by hand from the reference language.
- `<area_floor>[ die] Helligkeit[ (<licht_ohne_artikel>|<lichtes_mit_artikel>|<lichter>|<alle_lichter>)][ auf] <brightness>` has too many slot combinations to analyze — split it by hand from the reference language.
- `<area_floor>[ die] Helligkeit[ (<licht_ohne_artikel>|<lichtes_mit_artikel>|<lichter>|<alle_lichter>)] auf <brightness> (<setzen_end_of_sentence>|dimmen)` has too many slot combinations to analyze — split it by hand from the reference language.
- `<stelle> [die ]Helligkeit[ (<licht_ohne_artikel>|<lichtes_mit_artikel>|<lichter>|<alle_lichter>)] <area_floor> auf <brightness>[ ein]` has too many slot combinations to analyze — split it by hand from the reference language.
- `[die ]Helligkeit[ (<licht_ohne_artikel>|<lichtes_mit_artikel>|<lichter>|<alle_lichter>)] <area_floor> auf <brightness> (<setzen_end_of_sentence>|dimmen)` has too many slot combinations to analyze — split it by hand from the reference language.
- `dimme[ (<licht>|<lichter>|<alle_lichter>)] <area_floor>[ (auf|zu)] <brightness>` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(<licht>|<lichter>|<alle_lichter>) ]<area_floor>[ (auf|zu)] <brightness> dimmen` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<licht>|<lichter>|<alle_lichter>) <area_floor> (auf <brightness> Helligkeit[ [ein]stellen]|<brightness>[ (Helligkeit|[Helligkeit ]einstellen)]|auf <brightness>[ [ein]stellen])` has too many slot combinations to analyze — split it by hand from the reference language.
- `<area_floor> [auf ]<brightness> Helligkeit[ [ein]stellen]` has too many slot combinations to analyze — split it by hand from the reference language.
- `[<setze> ]<area_floor> auf [(die|das) ]{brightness_level:brightness}[ (Helligkeit[sstufe]|Stufe)]` has too many slot combinations to analyze — split it by hand from the reference language.
- `<stelle> <area_floor> auf [(die|das) ]{brightness_level:brightness}[ (Helligkeit[sstufe]|Stufe)][ ein]` has too many slot combinations to analyze — split it by hand from the reference language.
- `<area_floor> auf [(die|das) ]{brightness_level:brightness}[ (Helligkeit[sstufe]|Stufe)] (<setzen_end_of_sentence>|dimmen)` has too many slot combinations to analyze — split it by hand from the reference language.
- `<setze> [die ]Helligkeit <area_floor> auf [(die|das) ]{brightness_level:brightness}[ Stufe]` has too many slot combinations to analyze — split it by hand from the reference language.
- `<stelle> [die ]Helligkeit <area_floor> auf [(die|das) ]{brightness_level:brightness}[ Stufe][ ein]` has too many slot combinations to analyze — split it by hand from the reference language.
- `[die ]Helligkeit <area_floor>[ auf[ (die|das)]] {brightness_level:brightness}[ Stufe][ (<setzen_end_of_sentence>|dimmen)]` has too many slot combinations to analyze — split it by hand from the reference language.
- `[<setze> die ]Helligkeit[ (<licht_ohne_artikel>|<lichtes_mit_artikel>|<lichter>|<alle_lichter>)][ <hier>][ auf] <brightness>` has too many slot combinations to analyze — split it by hand from the reference language.
- `<stelle> [die ]Helligkeit[ (<licht_ohne_artikel>|<lichtes_mit_artikel>|<lichter>|<alle_lichter>)][ <hier>] auf <brightness>[ ein]` has too many slot combinations to analyze — split it by hand from the reference language.
- `[die ]Helligkeit[ (<licht_ohne_artikel>|<lichtes_mit_artikel>|<lichter>|<alle_lichter>)][ <hier>] auf <brightness> (<setzen_end_of_sentence>|dimmen)` has too many slot combinations to analyze — split it by hand from the reference language.
- `dimme[ (<licht>|<lichter>|<alle_lichter>)][ <hier>] (auf|zu) <brightness>` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(<licht>|<lichter>|<alle_lichter>) ][<hier> ](auf|zu) <brightness> dimmen` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<licht>|<lichter>|<alle_lichter>) [<hier> ][ auf] <brightness>[ [ein]stellen]` has too many slot combinations to analyze — split it by hand from the reference language.
- `<setze> [(<licht>|[die ]Farbe [(<lichtes_mit_artikel>|<lichter>|<alle_lichter>)]|<lichter>|<alle_lichter>) ]<area_floor> auf {color}` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(<licht>|[die ]Farbe [(<lichtes_mit_artikel>|<lichter>|<alle_lichter>)]|<lichter>|<alle_lichter>) ]<area_floor>[ auf] {color}` has too many slot combinations to analyze — split it by hand from the reference language.
- `<stelle> [(<licht>|[die ]Farbe [(<lichtes_mit_artikel>|<lichter>|<alle_lichter>)]|<lichter>|<alle_lichter>) ]<area_floor>[ auf] {color}[ ein]` has too many slot combinations to analyze — split it by hand from the reference language.
- `(änder[e]|veränder[e]) (<licht>|[die ]Farbe [(<lichtes_mit_artikel>|<lichter>|<alle_lichter>)]|<lichter>|<alle_lichter>) <area_floor> zu {color}` has too many slot combinations to analyze — split it by hand from the reference language.
- `[die ]Farbe[ (<licht_ohne_artikel>|<lichtes_mit_artikel>|<lichter>|<alle_lichter>)] <area_floor>[ auf] {color} <setzen_end_of_sentence>` has too many slot combinations to analyze — split it by hand from the reference language.
- `[die ]Farbe[ (<licht_ohne_artikel>|<lichtes_mit_artikel>|<lichter>|<alle_lichter>)] <area_floor> zu {color} [ver]ändern` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(<licht>|<lichter>|<alle_lichter>|<beim_licht>|<bei_allen_lichtern>) ]<area_floor> [die ]Farbe[ auf] {color}[ <setzen_end_of_sentence>]` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(<licht>|<lichter>|<alle_lichter>|<beim_licht>|<bei_allen_lichtern>) ]<area_floor> [die ]Farbe zu {color} [ver]ändern` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(<licht>|<lichter>|<alle_lichter>) ]<area_floor> [in [Farbe ]]{color} <leuchten_lassen>` has too many slot combinations to analyze — split it by hand from the reference language.
- `Färbe[ (<licht>|<lichter>|<alle_lichter>)] <area_floor> {color}[ ein]` has too many slot combinations to analyze — split it by hand from the reference language.
- `[<setze> ][(<licht>|[die ]Farbe [(<lichtes_mit_artikel>|<lichter>|<alle_lichter>)]|<lichter>|<alle_lichter>) ][<hier> ][auf ]{color}` has too many slot combinations to analyze — split it by hand from the reference language.
- `<stelle> [(<licht>|[die ]Farbe [(<lichtes_mit_artikel>|<lichter>|<alle_lichter>)]|<lichter>|<alle_lichter>) ][<hier> ][auf ]{color}[ ein]` has too many slot combinations to analyze — split it by hand from the reference language.
- `(änder[e]|veränder[e]) (<licht>|[die ]Farbe [(<lichtes_mit_artikel>|<lichter>|<alle_lichter>)]|<lichter>|<alle_lichter>)[ <hier>] zu {color}` has too many slot combinations to analyze — split it by hand from the reference language.
- `[die ]Farbe[ (<licht_ohne_artikel>|<lichtes_mit_artikel>|<lichter>|<alle_lichter>)][ <hier>][ auf] {color} <setzen_end_of_sentence>` has too many slot combinations to analyze — split it by hand from the reference language.
- `[die ]Farbe[ (<licht_ohne_artikel>|<lichtes_mit_artikel>|<lichter>|<alle_lichter>)][ <hier>] zu {color} <setzen_end_of_sentence>` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(<licht>|<lichtes_mit_artikel>|<lichter>|<alle_lichter>|<beim_licht>|<bei_allen_lichtern>) ][<hier> ][die ]Farbe[ auf] {color}[ <setzen_end_of_sentence>]` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(<licht>|<lichtes_mit_artikel>|<lichter>|<alle_lichter>|<beim_licht>|<bei_allen_lichtern>) ][<hier> ][die ]Farbe zu {color} [ver]ändern` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(<licht>|<lichtes_mit_artikel>|<lichter>|<alle_lichter>) ][<hier> ][in [Farbe ]]{color} <leuchten_lassen>` has too many slot combinations to analyze — split it by hand from the reference language.
- `Färbe ((<licht>|<lichter>|<alle_lichter>)[ <hier>]|(den|diesen) Raum|(das|dieses) Zimmer) {color}[ ein]` has too many slot combinations to analyze — split it by hand from the reference language.
- `[<setze> ][[die ]Farbtemperatur[ (von|vom)] ]<name>[ auf] <color_temp>` has too many slot combinations to analyze — split it by hand from the reference language.
- `<stelle> [[die ]Farbtemperatur[ (von|vom)] ]<name>[ auf] <color_temp>[ ein]` has too many slot combinations to analyze — split it by hand from the reference language.
- `(änder[e]|veränder[e]) [[die ]Farbtemperatur[ (von|vom)] ]<name> zu <color_temp>` has too many slot combinations to analyze — split it by hand from the reference language.
- `[die ]Farbtemperatur[ (von|vom)] <name>[ (auf|zu)] <color_temp> <setzen_end_of_sentence>` has too many slot combinations to analyze — split it by hand from the reference language.
- `<name>[ Farbtemperatur][ (auf|zu)] <color_temp>[ <setzen_end_of_sentence>]` has too many slot combinations to analyze — split it by hand from the reference language.
- `<setze> [(<licht>|[die ]Farbtemperatur [(<lichtes_mit_artikel>|<lichter>|<alle_lichter>)]|<lichter>|<alle_lichter>) ]<area_floor> auf <color_temp>` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(<licht>|[die ]Farbtemperatur [(<lichtes_mit_artikel>|<lichter>|<alle_lichter>)]|<lichter>|<alle_lichter>) ]<area_floor>[ auf] <color_temp>` has too many slot combinations to analyze — split it by hand from the reference language.
- `<stelle> [(<licht>|[die ]Farbtemperatur [(<lichtes_mit_artikel>|<lichter>|<alle_lichter>)]|<lichter>|<alle_lichter>) ]<area_floor>[ auf] <color_temp>[ ein]` has too many slot combinations to analyze — split it by hand from the reference language.
- `(änder[e]|veränder[e]) (<licht>|[die ]Farbtemperatur [(<lichtes_mit_artikel>|<lichter>|<alle_lichter>)]|<lichter>|<alle_lichter>) <area_floor> zu <color_temp>` has too many slot combinations to analyze — split it by hand from the reference language.
- `[die ]Farbtemperatur[ (<licht_ohne_artikel>|<lichtes_mit_artikel>|<lichter>|<alle_lichter>)] <area_floor>[ auf] <color_temp> <setzen_end_of_sentence>` has too many slot combinations to analyze — split it by hand from the reference language.
- `[die ]Farbtemperatur[ (<licht_ohne_artikel>|<lichtes_mit_artikel>|<lichter>|<alle_lichter>)] <area_floor> zu <color_temp> [ver]ändern` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(<licht>|<lichter>|<alle_lichter>|<beim_licht>|<bei_allen_lichtern>) ]<area_floor> [die ]Farbtemperatur[ auf] <color_temp>[ <setzen_end_of_sentence>]` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(<licht>|<lichter>|<alle_lichter>|<beim_licht>|<bei_allen_lichtern>) ]<area_floor> [die ]Farbtemperatur zu <color_temp> [ver]ändern` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(<licht>|<lichter>|<alle_lichter>) ]<area_floor> [in [Farbtemperatur ]]<color_temp> <leuchten_lassen>` has too many slot combinations to analyze — split it by hand from the reference language.
- `Färbe[ (<licht>|<lichter>|<alle_lichter>)] <area_floor> <color_temp>[ ein]` has too many slot combinations to analyze — split it by hand from the reference language.
- `[<setze> ][(<licht>|[die ]Farbtemperatur [(<lichtes_mit_artikel>|<lichter>|<alle_lichter>)]|<lichter>|<alle_lichter>) ][<hier> ][auf ]<color_temp>` has too many slot combinations to analyze — split it by hand from the reference language.
- `<stelle> [(<licht>|[die ]Farbtemperatur [(<lichtes_mit_artikel>|<lichter>|<alle_lichter>)]|<lichter>|<alle_lichter>) ][<hier> ][auf ]<color_temp>[ ein]` has too many slot combinations to analyze — split it by hand from the reference language.
- `(änder[e]|veränder[e]) (<licht>|[die ]Farbtemperatur [(<lichtes_mit_artikel>|<lichter>|<alle_lichter>)]|<lichter>|<alle_lichter>)[ <hier>] zu <color_temp>` has too many slot combinations to analyze — split it by hand from the reference language.
- `[die ]Farbtemperatur[ (<licht_ohne_artikel>|<lichtes_mit_artikel>|<lichter>|<alle_lichter>)][ <hier>][ auf] <color_temp> <setzen_end_of_sentence>` has too many slot combinations to analyze — split it by hand from the reference language.
- `[die ]Farbtemperatur[ (<licht_ohne_artikel>|<lichtes_mit_artikel>|<lichter>|<alle_lichter>)][ <hier>] zu <color_temp> <setzen_end_of_sentence>` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(<licht>|<lichtes_mit_artikel>|<lichter>|<alle_lichter>|<beim_licht>|<bei_allen_lichtern>) ][<hier> ][die ]Farbtemperatur[ auf] <color_temp>[ <setzen_end_of_sentence>]` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(<licht>|<lichtes_mit_artikel>|<lichter>|<alle_lichter>|<beim_licht>|<bei_allen_lichtern>) ][<hier> ][die ]Farbtemperatur zu <color_temp> [ver]ändern` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(<licht>|<lichtes_mit_artikel>|<lichter>|<alle_lichter>) ][<hier> ][in [Farbtemperatur ]]<color_temp> <leuchten_lassen>` has too many slot combinations to analyze — split it by hand from the reference language.
- `Färbe ((<licht>|<lichter>|<alle_lichter>)[ <hier>]|(den|diesen) Raum|(das|dieses) Zimmer) <color_temp>[ ein]` has too many slot combinations to analyze — split it by hand from the reference language.

### multi-combo template (3)
- `<brightness> Helligkeit <area_floor>[ einstellen]` matches ["?['area', 'brightness']", "?['brightness', 'floor']"] — split into one template per combo.
- `<area_floor> [auf ]{brightness_level:brightness}[ (Helligkeit[sstufe]|Stufe)]` matches ["?['area', 'brightness']", "?['brightness', 'floor']"] — split into one template per combo.
- `<area_floor> Helligkeit {brightness_level:brightness}[ Stufe]` matches ["?['area', 'brightness']", "?['brightness', 'floor']"] — split into one template per combo.

### test unmapped (14)
- Test 'Schlafzimmer hell' has slots ['area', 'brightness'] matching no single combo.
- Test 'ändere das Schlafzimmer auf die maximale Helligkeitsstufe' has slots ['area', 'brightness'] matching no single combo.
- Test 'ändere das Schlafzimmer auf die minimale Helligkeitsstufe' has slots ['area', 'brightness'] matching no single combo.
- Test 'Stelle die Helligkeit im Schlafzimmer auf 11' has slots ['area', 'brightness'] matching no single combo.
- Test 'ändere das Erdgeschoss auf die maximale Helligkeitsstufe' has slots ['brightness', 'floor'] matching no single combo.
- Test 'ändere das Erdgeschoss auf die minimale Helligkeitsstufe' has slots ['brightness', 'floor'] matching no single combo.
- Test 'setze die Helligkeit der Lampe im Erdgeschoss auf 15%' has slots ['brightness', 'floor'] matching no single combo.
- Test 'Helligkeit hier auf 10' has slots ['__context_area__', 'brightness'] matching no single combo.
- Test 'Stelle die Farbe im Schlafzimmer auf blau' has slots ['area', 'color'] matching no single combo.
- Test 'Stelle die Farbe im Erdgeschoss auf blau' has slots ['color', 'floor'] matching no single combo.
- Test 'Stelle die Farbe auf blau' has slots ['__context_area__', 'color'] matching no single combo.
- Test 'Stelle die Farbtemperatur im Schlafzimmer auf kaltweiss' has slots ['area', 'temperature'] matching no single combo.
- Test 'Stelle die Farbtemperatur im Erdgeschoss auf kaltweiss' has slots ['floor', 'temperature'] matching no single combo.
- Test 'Stelle die Farbtemperatur auf warmweiss' has slots ['__context_area__', 'temperature'] matching no single combo.

### unmapped signature (2)
- `[<hier> ]<brightness> helligkeit[ einstellen]` has slots ['__context_area__', 'brightness'] which match no single declared combo — check intents.yaml / domain.
- `<brightness> helligkeit <hier>[ einstellen]` has slots ['__context_area__', 'brightness'] which match no single declared combo — check intents.yaml / domain.

## Reminders (see docs/syntax_migration_guide.md)
- Inline list-bearing rules in templates (e.g. `<name>` -> `[de|het] {name}`).
- Flatten nested `<rule>` references.
- Add an `example:` taken from the matching test sentences.
- Delete the old `*_HassLightSet.yaml` sentence/test files once done.
- Run `python3 -m script.intentfest validate --language de` and the tests.
