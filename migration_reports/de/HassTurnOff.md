# Migration report: de / HassTurnOff

## Declared slot combinations
- `domain_only` slots: {domain}; context_area: true — scaffolded
- `name_only` slots: {name} — EMPTY — REQUIRED, must be filled
- `area_domain` slots: {area}, {domain} — EMPTY — REQUIRED, must be filled
- `device_class_cover` slots: {device_class}, {domain}; context_area: true — EMPTY — non-required, safe to skip
- `name_area` slots: {area}, {name} — scaffolded
- `name_floor` slots: {floor}, {name} — EMPTY — non-required, safe to skip
- `area_device_class_cover` slots: {area}, {device_class}, {domain} — EMPTY — non-required, safe to skip
- `floor_device_class_cover` slots: {device_class}, {domain}, {floor} — EMPTY — non-required, safe to skip
- `domain_all` slots: {domain} — scaffolded

## Scaffold files written
- /home/user/intents/sentences/de/HassTurnOff/name_area.yaml
- /home/user/intents/sentences/de/HassTurnOff/domain_all.yaml
- /home/user/intents/sentences/de/HassTurnOff/domain_only.yaml
- /home/user/intents/tests/de/HassTurnOff/area_domain.yaml
- /home/user/intents/tests/de/HassTurnOff/domain_all.yaml
- /home/user/intents/tests/de/HassTurnOff/domain_only.yaml
- /home/user/intents/tests/de/HassTurnOff/name_only.yaml
- /home/user/intents/tests/de/HassTurnOff/name_area.yaml

## Old files to delete when done
(this intent may span several domain files — delete ALL of them)
- /home/user/intents/sentences/de/cover_HassTurnOff.yaml
- /home/user/intents/sentences/de/fan_HassTurnOff.yaml
- /home/user/intents/sentences/de/homeassistant_HassTurnOff.yaml
- /home/user/intents/sentences/de/light_HassTurnOff.yaml
- /home/user/intents/sentences/de/lock_HassTurnOff.yaml
- /home/user/intents/sentences/de/valve_HassTurnOff.yaml
- /home/user/intents/tests/de/cover_HassTurnOff.yaml
- /home/user/intents/tests/de/fan_HassTurnOff.yaml
- /home/user/intents/tests/de/homeassistant_HassTurnOff.yaml
- /home/user/intents/tests/de/light_HassTurnOff.yaml
- /home/user/intents/tests/de/lock_HassTurnOff.yaml
- /home/user/intents/tests/de/valve_HassTurnOff.yaml

## Flags needing attention (113)

### complex template (85)
- `<schliessen> <name>[ <area_floor>]` has too many slot combinations to analyze — split it by hand from the reference language.
- `<name>[ <area_floor>] <schliessen_end_of_sentence>` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<machen>|<fahren>) <name>[ <area_floor>] <zu>` has too many slot combinations to analyze — split it by hand from the reference language.
- `<name>[ <area_floor>] <zu>[[ ](machen|fahren)]` has too many slot combinations to analyze — split it by hand from the reference language.
- `<schliessen> <area_floor> (<abdeckung>|<tor>|<garage>|<fenster>)` has too many slot combinations to analyze — split it by hand from the reference language.
- `<schliessen> (<abdeckung>|<tor>|<garage>|<fenster>) <area_floor>` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<abdeckung>|<tor>|<garage>|<fenster>) <area_floor> <schliessen_end_of_sentence>` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<machen>|<fahren>) <area_floor> (<abdeckung>|<tor>|<garage>|<fenster>) <zu>` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<machen>|<fahren>) (<abdeckung>|<tor>|<garage>|<fenster>) <area_floor> <zu>` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<abdeckung>|<tor>|<garage>|<fenster>) <area_floor> <zu>[[ ](machen|fahren)]` has too many slot combinations to analyze — split it by hand from the reference language.
- `<area_floor> (<abdeckung>|<tor>|<garage>|<fenster>) <schliessen_end_of_sentence>` has too many slot combinations to analyze — split it by hand from the reference language.
- `<area_floor> (<abdeckung>|<tor>|<garage>|<fenster>) <zu>[[ ](machen|fahren)]` has too many slot combinations to analyze — split it by hand from the reference language.
- `<schliessen>[ <area_floor>] (<alle_abdeckungen>|<alle_tore>|<alle_garagen>|<alle_fenster>)` has too many slot combinations to analyze — split it by hand from the reference language.
- `<schliessen> (<alle_abdeckungen>|<alle_tore>|<alle_garagen>|<alle_fenster>) <area_floor>` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<machen>|<fahren>)[ <area_floor>] (<alle_abdeckungen>|<alle_tore>|<alle_garagen>|<alle_fenster>) <zu>` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<machen>|<fahren>) (<alle_abdeckungen>|<alle_tore>|<alle_garagen>|<alle_fenster>) <area_floor> <zu>` has too many slot combinations to analyze — split it by hand from the reference language.
- `<area_floor> (<alle_abdeckungen>|<alle_tore>|<alle_garagen>|<alle_fenster>) <zu>[[ ](machen|fahren)]` has too many slot combinations to analyze — split it by hand from the reference language.
- `<area_floor> (<alle_abdeckungen>|<alle_tore>|<alle_garagen>|<alle_fenster>) <schliessen_end_of_sentence>` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<alle_abdeckungen>|<alle_tore>|<alle_garagen>|<alle_fenster>)[ <area_floor>] <zu>[[ ](machen|fahren)]` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<alle_abdeckungen>|<alle_tore>|<alle_garagen>|<alle_fenster>)[ <area_floor>] <schliessen_end_of_sentence>` has too many slot combinations to analyze — split it by hand from the reference language.
- `<schliessen>[ <hier>] (<abdeckung>|<tor>|<garage>|<fenster>)` has too many slot combinations to analyze — split it by hand from the reference language.
- `<schliessen> (<abdeckung>|<tor>|<garage>|<fenster>) <hier>` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<abdeckung>|<tor>|<garage>|<fenster>)[ <hier>] <schliessen_end_of_sentence>` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<abdeckung>|<tor>|<garage>|<fenster>) <schliessen_end_of_sentence> <hier>` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<machen>|<fahren>)[ <hier>] (<abdeckung>|<tor>|<garage>|<fenster>) <zu>` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<machen>|<fahren>) (<abdeckung>|<tor>|<garage>|<fenster>) <hier> <zu>` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<machen>|<fahren>) (<abdeckung>|<tor>|<garage>|<fenster>) <zu> <hier>` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<abdeckung>|<tor>|<garage>|<fenster>)[ <hier>] <zu>[[ ](machen|fahren)]` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<abdeckung>|<tor>|<garage>|<fenster>) <zu>[[ ](machen|fahren)] <hier>` has too many slot combinations to analyze — split it by hand from the reference language.
- `[<hier> ](<abdeckung>|<tor>|<garage>|<fenster>) <schliessen_end_of_sentence>` has too many slot combinations to analyze — split it by hand from the reference language.
- `<hier> (<abdeckung>|<tor>|<garage>|<fenster>) <zu>[[ ](machen|fahren)]` has too many slot combinations to analyze — split it by hand from the reference language.
- `<schliessen> <hier> (<alle_abdeckungen>|<alle_tore>|<alle_garagen>|<alle_fenster>)` has too many slot combinations to analyze — split it by hand from the reference language.
- `<schliessen> (<alle_abdeckungen>|<alle_tore>|<alle_garagen>|<alle_fenster>) <hier>` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<machen>|<fahren>) <hier> (<alle_abdeckungen>|<alle_tore>|<alle_garagen>|<alle_fenster>) <zu>` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<machen>|<fahren>) (<alle_abdeckungen>|<alle_tore>|<alle_garagen>|<alle_fenster>) <hier> <zu>` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<machen>|<fahren>) (<alle_abdeckungen>|<alle_tore>|<alle_garagen>|<alle_fenster>) <zu> <hier>` has too many slot combinations to analyze — split it by hand from the reference language.
- `<hier> (<alle_abdeckungen>|<alle_tore>|<alle_garagen>|<alle_fenster>) <zu>[[ ](machen|fahren)]` has too many slot combinations to analyze — split it by hand from the reference language.
- `<hier> (<alle_abdeckungen>|<alle_tore>|<alle_garagen>|<alle_fenster>) <schliessen_end_of_sentence>` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<alle_abdeckungen>|<alle_tore>|<alle_garagen>|<alle_fenster>) <hier> <zu>[[ ](machen|fahren)]` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<alle_abdeckungen>|<alle_tore>|<alle_garagen>|<alle_fenster>) <hier> <schliessen_end_of_sentence>` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<alle_abdeckungen>|<alle_tore>|<alle_garagen>|<alle_fenster>) <zu>[[ ](machen|fahren)] <hier>` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<alle_abdeckungen>|<alle_tore>|<alle_garagen>|<alle_fenster>) <schliessen_end_of_sentence> <hier>` has too many slot combinations to analyze — split it by hand from the reference language.
- `<entsperren>[ <alle>] (<tuer>|<schloss>) <area>` has too many slot combinations to analyze — split it by hand from the reference language.
- `<entsperren> <area>[ <alle>] (<tuer>|<schloss>)` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<sperren>|<machen>)[ <alle>] (<tuer>|<schloss>) <area> auf` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<sperren>|<machen>) <area>[ <alle>] (<tuer>|<schloss>) auf` has too many slot combinations to analyze — split it by hand from the reference language.
- `[<alle> ](<tuer>|<schloss>) <area> (auf[machen]|<entsperren>)` has too many slot combinations to analyze — split it by hand from the reference language.
- `<area>[ <alle>] (<tuer>|<schloss>) (auf[machen]|<entsperren>)` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<schalten>|<machen>) <name>[ <area>] <aus>` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<schalten>|<machen>) <name>[ <area_floor>] (aus|ab)` has too many slot combinations to analyze — split it by hand from the reference language.
- `dreh[e] <name>[ <area_floor>] ab` has too many slot combinations to analyze — split it by hand from the reference language.
- `<name>[ <area_floor>] (aus[schalten]|abschalten|ausmachen|abdrehen)` has too many slot combinations to analyze — split it by hand from the reference language.
- `<deaktivieren> <name>[ <area_floor>]` has too many slot combinations to analyze — split it by hand from the reference language.
- `<name>[ <area_floor>] <deaktivieren>` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<schalten>|<machen>) (<licht>|<lichter>|<alle_lichter>) <area_floor> aus` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<schalten>|dreh[e]) (<licht>|<lichter>|<alle_lichter>) <area_floor> ab` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<schalten>|<machen>) <area_floor> (<licht>|<lichter>|<alle_lichter>) aus` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<schalten>|dreh[e]) <area_floor> (<licht>|<lichter>|<alle_lichter>) ab` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<licht>|<lichter>|<alle_lichter>) <area_floor> (aus[schalten]|abschalten|ausmachen|abdrehen)` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<licht>|<lichter>|<alle_lichter>) (aus[schalten]|abschalten|ausmachen|abdrehen|<stt_fix_aus_im>) <area_floor>` has too many slot combinations to analyze — split it by hand from the reference language.
- `<area_floor> (<licht>|<lichter>|<alle_lichter>) (aus[schalten]|abschalten|ausmachen|abdrehen)` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<schalten>|<machen>) (<licht>|<lichter>)[ <hier>] aus` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<schalten>|dreh[e]) (<licht>|<lichter>)[ <hier>] ab` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<schalten>|<machen>) <hier> (<licht>|<lichter>) aus` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<schalten>|dreh[e]) <hier> (<licht>|<lichter>) ab` has too many slot combinations to analyze — split it by hand from the reference language.
- `<schalten> <luefter> <area_floor> (aus|ab)` has too many slot combinations to analyze — split it by hand from the reference language.
- `<schalten> <area_floor> <luefter> (aus|ab)` has too many slot combinations to analyze — split it by hand from the reference language.
- `<machen> <luefter> <area_floor> aus` has too many slot combinations to analyze — split it by hand from the reference language.
- `<machen> <area_floor> <luefter> aus` has too many slot combinations to analyze — split it by hand from the reference language.
- `<luefter> <area_floor> (aus|aus(schalten|machen)|abschalten)` has too many slot combinations to analyze — split it by hand from the reference language.
- `<area_floor> <luefter> (aus|aus(schalten|machen)|abschalten)` has too many slot combinations to analyze — split it by hand from the reference language.
- `<schalten> <alle_luefter>[ <area_floor>] (aus|ab)` has too many slot combinations to analyze — split it by hand from the reference language.
- `<schalten> <area_floor> <alle_luefter> (aus|ab)` has too many slot combinations to analyze — split it by hand from the reference language.
- `stoppe <alle_luefter>[ <area_floor>]` has too many slot combinations to analyze — split it by hand from the reference language.
- `stoppe <area_floor> <alle_luefter>` has too many slot combinations to analyze — split it by hand from the reference language.
- `<machen> <alle_luefter>[ <area_floor>] aus` has too many slot combinations to analyze — split it by hand from the reference language.
- `<machen> <area_floor> <alle_luefter> aus` has too many slot combinations to analyze — split it by hand from the reference language.
- `<alle_luefter>[ <area_floor>] (aus|aus(schalten|machen)|abschalten)` has too many slot combinations to analyze — split it by hand from the reference language.
- `<area_floor> <alle_luefter> (aus|aus(schalten|machen)|abschalten)` has too many slot combinations to analyze — split it by hand from the reference language.
- `<schalten> <hier> <alle_luefter> (aus|ab)` has too many slot combinations to analyze — split it by hand from the reference language.
- `<schalten> <alle_luefter> <hier> (aus|ab)` has too many slot combinations to analyze — split it by hand from the reference language.
- `<schalten> <alle_luefter> (aus|ab) <hier>` has too many slot combinations to analyze — split it by hand from the reference language.
- `<schliessen> <name>[ <area_floor>]` has too many slot combinations to analyze — split it by hand from the reference language.
- `<name>[ <area_floor>] <schliessen_end_of_sentence>` has too many slot combinations to analyze — split it by hand from the reference language.
- `<name>[ <area_floor>] (zu|ab)[ ]drehen` has too many slot combinations to analyze — split it by hand from the reference language.

### missing required coverage (2)
- combo `name_only` declares required name_domains ['light', 'switch', 'fan', 'media_player', 'input_boolean', 'cover'] but no sentences were placed there.
- combo `area_domain` declares required inferred_domains ['light'] but no sentences were placed there.

### multi-combo template (9)
- `<entsperren> <name>[ <area>]` matches ['name_area', 'name_only'] — split into one template per combo.
- `(<sperren>|<machen>) <name>[ <area>] auf` matches ['name_area', 'name_only'] — split into one template per combo.
- `<name>[ <area>] (auf[machen]|<entsperren>)` matches ['name_area', 'name_only'] — split into one template per combo.
- `stoppe <name>[ <area>]` matches ['name_area', 'name_only'] — split into one template per combo.
- `<deaktivieren> <name>[ <area>]` matches ['name_area', 'name_only'] — split into one template per combo.
- `<name>[ <area>] <deaktivieren>` matches ['name_area', 'name_only'] — split into one template per combo.
- `<name>[ <area>] <aus>[schalten|machen]` matches ['name_area', 'name_only'] — split into one template per combo.
- `stoppe <luefter> <area_floor>` matches ["?['domain', 'floor']", 'area_domain'] — split into one template per combo.
- `stoppe <area_floor> <luefter>` matches ["?['domain', 'floor']", 'area_domain'] — split into one template per combo.

### test unmapped (17)
- Test 'schließ das Rollo links' has slots ['domain', 'name'] matching no single combo.
- Test 'schließ den Vorhang links' has slots ['domain', 'name'] matching no single combo.
- Test 'schließe den Vorhang rechts im Wohnzimmer' has slots ['area', 'domain', 'name'] matching no single combo.
- Test 'schließe den Vorhang links im Obergeschoss' has slots ['domain', 'floor', 'name'] matching no single combo.
- Test 'schließe im Erdgeschoss das Tor' has slots ['domain', 'floor'] matching no single combo.
- Test 'schließe im Erdgeschoss alle Tore' has slots ['domain', 'floor'] matching no single combo.
- Test 'öffne die Haustür' has slots ['domain', 'name'] matching no single combo.
- Test 'Haustür im Flur öffnen' has slots ['area', 'domain', 'name'] matching no single combo.
- Test 'schalte die Schlafzimmerlampe aus' has slots ['domain', 'name'] matching no single combo.
- Test 'schalte die Stehlampe im Schlafzimmer aus' has slots ['area', 'domain', 'name'] matching no single combo.
- Test 'schalte die Stehlampe im Obergeschoss aus' has slots ['domain', 'floor', 'name'] matching no single combo.
- Test 'Schalte das Licht im Erdgeschoss aus' has slots ['domain', 'floor'] matching no single combo.
- Test 'mach den Ventilator im Erdgeschoss aus' has slots ['domain', 'floor'] matching no single combo.
- Test 'mach alle Ventilatoren im Erdgeschoss aus' has slots ['domain', 'floor'] matching no single combo.
- Test 'Schließe das Hauptventil' has slots ['domain', 'name'] matching no single combo.
- Test 'Schließe das Hauptventil in der Küche' has slots ['area', 'domain', 'name'] matching no single combo.
- Test 'Schließe das Hauptventil im Erdgeschoss' has slots ['domain', 'floor', 'name'] matching no single combo.

## Reminders (see docs/syntax_migration_guide.md)
- Inline list-bearing rules in templates (e.g. `<name>` -> `[de|het] {name}`).
- Flatten nested `<rule>` references.
- Add an `example:` taken from the matching test sentences.
- Delete the old `*_HassTurnOff.yaml` sentence/test files once done.
- Run `python3 -m script.intentfest validate --language de` and the tests.
