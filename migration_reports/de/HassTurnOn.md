# Migration report: de / HassTurnOn

## Declared slot combinations
- `domain_only` slots: {domain}; context_area: true — scaffolded
- `name_only` slots: {name} — EMPTY — REQUIRED, must be filled
- `area_domain` slots: {area}, {domain} — EMPTY — REQUIRED, must be filled
- `device_class_cover` slots: {device_class}, {domain}; context_area: true — EMPTY — non-required, safe to skip
- `name_area` slots: {area}, {name} — scaffolded
- `name_floor` slots: {floor}, {name} — EMPTY — non-required, safe to skip
- `name_script` slots: {name} — EMPTY — non-required, safe to skip
- `name_scene` slots: {name} — EMPTY — non-required, safe to skip
- `area_device_class_cover` slots: {area}, {device_class}, {domain} — EMPTY — non-required, safe to skip
- `floor_device_class_cover` slots: {device_class}, {domain}, {floor} — EMPTY — non-required, safe to skip

## Scaffold files written
- /home/user/intents/sentences/de/HassTurnOn/domain_only.yaml
- /home/user/intents/sentences/de/HassTurnOn/name_area.yaml
- /home/user/intents/tests/de/HassTurnOn/area_domain.yaml
- /home/user/intents/tests/de/HassTurnOn/domain_only.yaml
- /home/user/intents/tests/de/HassTurnOn/name_area.yaml

## Old files to delete when done
(this intent may span several domain files — delete ALL of them)
- /home/user/intents/sentences/de/cover_HassTurnOn.yaml
- /home/user/intents/sentences/de/fan_HassTurnOn.yaml
- /home/user/intents/sentences/de/homeassistant_HassTurnOn.yaml
- /home/user/intents/sentences/de/light_HassTurnOn.yaml
- /home/user/intents/sentences/de/lock_HassTurnOn.yaml
- /home/user/intents/sentences/de/scene_HassTurnOn.yaml
- /home/user/intents/sentences/de/script_HassTurnOn.yaml
- /home/user/intents/sentences/de/valve_HassTurnOn.yaml
- /home/user/intents/tests/de/cover_HassTurnOn.yaml
- /home/user/intents/tests/de/fan_HassTurnOn.yaml
- /home/user/intents/tests/de/homeassistant_HassTurnOn.yaml
- /home/user/intents/tests/de/light_HassTurnOn.yaml
- /home/user/intents/tests/de/lock_HassTurnOn.yaml
- /home/user/intents/tests/de/scene_HassTurnOn.yaml
- /home/user/intents/tests/de/script_HassTurnOn.yaml
- /home/user/intents/tests/de/valve_HassTurnOn.yaml

## Flags needing attention (149)

### complex template (85)
- `<name>[ <area_floor>] <öffnen_end_of_sentence>` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<machen>|<fahren>) <name>[ <area_floor>] <auf>` has too many slot combinations to analyze — split it by hand from the reference language.
- `<name>[ <area_floor>] <auf>[[ ](machen|fahren)]` has too many slot combinations to analyze — split it by hand from the reference language.
- `öffne <area_floor> (<abdeckung>|<tor>|<garage>|<fenster>)` has too many slot combinations to analyze — split it by hand from the reference language.
- `öffne (<abdeckung>|<tor>|<garage>|<fenster>) <area_floor>` has too many slot combinations to analyze — split it by hand from the reference language.
- `<area_floor> (<abdeckung>|<tor>|<garage>|<fenster>) <öffnen_end_of_sentence>` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<abdeckung>|<tor>|<garage>|<fenster>) <area_floor> <öffnen_end_of_sentence>` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<machen>|<fahren>) <area_floor> (<abdeckung>|<tor>|<garage>|<fenster>) <auf>` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<machen>|<fahren>) (<abdeckung>|<tor>|<garage>|<fenster>) <area_floor> <auf>` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<abdeckung>|<tor>|<garage>|<fenster>) <area_floor> <auf>[[ ](machen|fahren)]` has too many slot combinations to analyze — split it by hand from the reference language.
- `<area_floor> (<abdeckung>|<tor>|<garage>|<fenster>) <auf>[[ ](machen|fahren)]` has too many slot combinations to analyze — split it by hand from the reference language.
- `öffne <area_floor> (<alle_abdeckungen>|<alle_tore>|<alle_garagen>|<alle_fenster>)` has too many slot combinations to analyze — split it by hand from the reference language.
- `<area_floor> (<alle_abdeckungen>|<alle_tore>|<alle_garagen>|<alle_fenster>) <öffnen_end_of_sentence>` has too many slot combinations to analyze — split it by hand from the reference language.
- `<area_floor> (<alle_abdeckungen>|<alle_tore>|<alle_garagen>|<alle_fenster>) <auf>[[ ](machen|fahren)]` has too many slot combinations to analyze — split it by hand from the reference language.
- `öffne (<alle_abdeckungen>|<alle_tore>|<alle_garagen>|<alle_fenster>)[ <area_floor>]` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<machen>|<fahren>)[ <area_floor>] (<alle_abdeckungen>|<alle_tore>|<alle_garagen>|<alle_fenster>) <auf>` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<machen>|<fahren>) (<alle_abdeckungen>|<alle_tore>|<alle_garagen>|<alle_fenster>) <area_floor> <auf>` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<alle_abdeckungen>|<alle_tore>|<alle_garagen>|<alle_fenster>) (<auf>[[ ](machen|fahren)]|<öffnen_end_of_sentence>)` has too many slot combinations to analyze — split it by hand from the reference language.
- `[<hier> ](<abdeckung>|<tor>|<garage>|<fenster>) <öffnen_end_of_sentence>` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<abdeckung>|<tor>|<garage>|<fenster>) <hier> <öffnen_end_of_sentence>` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<abdeckung>|<tor>|<garage>|<fenster>) <öffnen_end_of_sentence> <hier>` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<machen>|<fahren>)[ <hier>] (<abdeckung>|<tor>|<garage>|<fenster>) <auf>` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<machen>|<fahren>) (<abdeckung>|<tor>|<garage>|<fenster>) <hier> <auf>` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<abdeckung>|<tor>|<garage>|<fenster>)[ <hier>] <auf>[[ ](machen|fahren)]` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<abdeckung>|<tor>|<garage>|<fenster>) <auf>[[ ](machen|fahren)] <hier>` has too many slot combinations to analyze — split it by hand from the reference language.
- `<hier> (<abdeckung>|<tor>|<garage>|<fenster>) <auf>[[ ](machen|fahren)]` has too many slot combinations to analyze — split it by hand from the reference language.
- `öffne <hier> (<alle_abdeckungen>|<alle_tore>|<alle_garagen>|<alle_fenster>)` has too many slot combinations to analyze — split it by hand from the reference language.
- `<hier> (<alle_abdeckungen>|<alle_tore>|<alle_garagen>|<alle_fenster>) <öffnen_end_of_sentence>` has too many slot combinations to analyze — split it by hand from the reference language.
- `<hier> (<alle_abdeckungen>|<alle_tore>|<alle_garagen>|<alle_fenster>) <auf>[[ ](machen|fahren)]` has too many slot combinations to analyze — split it by hand from the reference language.
- `öffne (<alle_abdeckungen>|<alle_tore>|<alle_garagen>|<alle_fenster>) <hier>` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<machen>|<fahren>) <hier> (<alle_abdeckungen>|<alle_tore>|<alle_garagen>|<alle_fenster>) <auf>` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<machen>|<fahren>) (<alle_abdeckungen>|<alle_tore>|<alle_garagen>|<alle_fenster>) <hier> <auf>` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<alle_abdeckungen>|<alle_tore>|<alle_garagen>|<alle_fenster>) <hier> (<auf>[[ ](machen|fahren)]|<öffnen_end_of_sentence>)` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<alle_abdeckungen>|<alle_tore>|<alle_garagen>|<alle_fenster>) (<auf>[[ ](machen|fahren)]|<öffnen_end_of_sentence>) <hier>` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<schalten>|<machen>) <name>[ <area>] <an>` has too many slot combinations to analyze — split it by hand from the reference language.
- `[<szene> ]<name> <area>[ (<aktivieren>|<ausfuehren>|<an>)]` has too many slot combinations to analyze — split it by hand from the reference language.
- `<name> <szene> <area> (<aktivieren>|<ausfuehren>|<an>)` has too many slot combinations to analyze — split it by hand from the reference language.
- `<aktivieren>[ <szene>] <name> <area>` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<schalten>|<machen>) <name>[ <area_floor>] (an|ein)` has too many slot combinations to analyze — split it by hand from the reference language.
- `dreh[e] <name>[ <area_floor>] auf` has too many slot combinations to analyze — split it by hand from the reference language.
- `<name>[ <area_floor>] ((an|ein)[schalten]|anmachen|aufdrehen)` has too many slot combinations to analyze — split it by hand from the reference language.
- `<aktivieren> <name>[ <area_floor>]` has too many slot combinations to analyze — split it by hand from the reference language.
- `<name>[ <area_floor>] <aktivieren>` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<schalten>|<machen>) (<licht>|<lichter>|<alle_lichter>) <area_floor> an` has too many slot combinations to analyze — split it by hand from the reference language.
- `<schalten> (<licht>|<lichter>|<alle_lichter>) <area_floor> ein` has too many slot combinations to analyze — split it by hand from the reference language.
- `dreh[e] (<licht>|<lichter>|<alle_lichter>) <area_floor> auf` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<schalten>|<machen>) <area_floor> ((<licht>|<lichter>|<alle_lichter>) an|[das ]<stt_fix_licht_an>)` has too many slot combinations to analyze — split it by hand from the reference language.
- `<schalten> <area_floor> (<licht>|<lichter>|<alle_lichter>) ein` has too many slot combinations to analyze — split it by hand from the reference language.
- `dreh[e] <area_floor> (<licht>|<lichter>|<alle_lichter>) auf` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<licht>|<lichter>|<alle_lichter>) <area_floor> ((an|ein)[schalten]|anmachen|aufdrehen)` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<licht>|<lichter>|<alle_lichter>) ((an|ein)[schalten]|anmachen|aufdrehen) <area_floor>` has too many slot combinations to analyze — split it by hand from the reference language.
- `<area_floor> (<licht>|<lichter>|<alle_lichter>) ((an|ein)[schalten]|anmachen|aufdrehen)` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<schalten>|<machen>) ((<licht>|<lichter>)[ <hier>] an|[das ]<stt_fix_licht_an>)` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<schalten>|<machen>) <hier> ((<licht>|<lichter>) an|[das ]<stt_fix_licht_an>)` has too many slot combinations to analyze — split it by hand from the reference language.
- `(<licht>|<lichter>)[ <hier>] ((an|ein)[schalten]|anmachen|aufdrehen)` has too many slot combinations to analyze — split it by hand from the reference language.
- `<hier> (<licht>|<lichter>) ((an|ein)[schalten]|anmachen|aufdrehen)` has too many slot combinations to analyze — split it by hand from the reference language.
- `<schalten> <luefter> <area_floor> (an|ein)` has too many slot combinations to analyze — split it by hand from the reference language.
- `<schalten> <area_floor> <luefter> (an|ein)` has too many slot combinations to analyze — split it by hand from the reference language.
- `<machen> <luefter> <area_floor> an` has too many slot combinations to analyze — split it by hand from the reference language.
- `<machen> <area_floor> <luefter> an` has too many slot combinations to analyze — split it by hand from the reference language.
- `<luefter> <area_floor> (an|(ein|an)schalten|anmachen)` has too many slot combinations to analyze — split it by hand from the reference language.
- `<area_floor> <luefter> (an|(ein|an)schalten|anmachen)` has too many slot combinations to analyze — split it by hand from the reference language.
- `starte <alle_luefter>[ <area_floor>]` has too many slot combinations to analyze — split it by hand from the reference language.
- `starte <area_floor> <alle_luefter>` has too many slot combinations to analyze — split it by hand from the reference language.
- `<schalten> <alle_luefter>[ <area_floor>] (an|ein)` has too many slot combinations to analyze — split it by hand from the reference language.
- `<schalten> <area_floor> <alle_luefter> (an|ein)` has too many slot combinations to analyze — split it by hand from the reference language.
- `<machen> <alle_luefter>[ <area_floor>] an` has too many slot combinations to analyze — split it by hand from the reference language.
- `<machen> <area_floor> <alle_luefter> an` has too many slot combinations to analyze — split it by hand from the reference language.
- `<alle_luefter>[ <area_floor>] (an|(ein|an)schalten|anmachen)` has too many slot combinations to analyze — split it by hand from the reference language.
- `<area_floor> <alle_luefter> (an|(ein|an)schalten|anmachen)` has too many slot combinations to analyze — split it by hand from the reference language.
- `<schalten> <hier> <alle_luefter> (an|ein)` has too many slot combinations to analyze — split it by hand from the reference language.
- `<schalten> <alle_luefter> <hier> (an|ein)` has too many slot combinations to analyze — split it by hand from the reference language.
- `<schalten> <alle_luefter> (an|ein) <hier>` has too many slot combinations to analyze — split it by hand from the reference language.
- `<name>[ <area_floor>] <öffnen_end_of_sentence>` has too many slot combinations to analyze — split it by hand from the reference language.
- `<name>[ <area_floor>] auf[ ]drehen` has too many slot combinations to analyze — split it by hand from the reference language.
- `<sperren> <name>[ <area>][ (zu|ab)]` has too many slot combinations to analyze — split it by hand from the reference language.
- `<sperren> <area> <name>[ (zu|ab)]` has too many slot combinations to analyze — split it by hand from the reference language.
- `<sperren>[ <alle>] (<tuer>|<schloss>) <area>[ (zu|ab)]` has too many slot combinations to analyze — split it by hand from the reference language.
- `<machen>[ <alle>] (<tuer>|<schloss>) <area> zu` has too many slot combinations to analyze — split it by hand from the reference language.
- `<sperren> <area>[ <alle>] (<tuer>|<schloss>)[ (zu|ab)]` has too many slot combinations to analyze — split it by hand from the reference language.
- `<machen> <area>[ <alle>] (<tuer>|<schloss>) zu` has too many slot combinations to analyze — split it by hand from the reference language.
- `[<alle> ](<tuer>|<schloss>) <area> (zu[machen]|<absperren>)` has too many slot combinations to analyze — split it by hand from the reference language.
- `<area>[ <alle>] (<tuer>|<schloss>) (zu[machen]|<absperren>)` has too many slot combinations to analyze — split it by hand from the reference language.
- `<absperren>[ <alle>] (<tuer>|<schloss>) <area>` has too many slot combinations to analyze — split it by hand from the reference language.
- `<absperren> <area>[ <alle>] (<tuer>|<schloss>)` has too many slot combinations to analyze — split it by hand from the reference language.

### missing required coverage (2)
- combo `name_only` declares required name_domains ['light', 'switch', 'fan', 'media_player', 'input_boolean', 'cover'] but no sentences were placed there.
- combo `area_domain` declares required inferred_domains ['light'] but no sentences were placed there.

### multi-combo template (13)
- `öffne <name>[ <area_floor>]` matches ["?['area', 'domain', 'name']", "?['domain', 'floor', 'name']", "?['domain', 'name']"] — split into one template per combo.
- `starte <name>[ <area>]` matches ["?['name']", 'name_area'] — split into one template per combo.
- `<aktivieren> <name>[ <area>]` matches ["?['name']", 'name_area'] — split into one template per combo.
- `<name>[ <area>] <aktivieren>` matches ["?['name']", 'name_area'] — split into one template per combo.
- `<name>[ <area>] <an>[schalten|machen]` matches ["?['name']", 'name_area'] — split into one template per combo.
- `[das ]<stt_fix_licht_an> <area_floor>` matches ["?['domain', 'floor']", 'area_domain'] — split into one template per combo.
- `<area_floor> [das ]<stt_fix_licht_an>` matches ["?['domain', 'floor']", 'area_domain'] — split into one template per combo.
- `starte <luefter> <area_floor>` matches ["?['domain', 'floor']", 'area_domain'] — split into one template per combo.
- `starte <area_floor> <luefter>` matches ["?['domain', 'floor']", 'area_domain'] — split into one template per combo.
- `öffne <name>[ <area_floor>]` matches ["?['area', 'domain', 'name']", "?['domain', 'floor', 'name']", "?['domain', 'name']"] — split into one template per combo.
- `<machen> <name>[ <area>] zu` matches ['name_area', 'name_only'] — split into one template per combo.
- `<name>[ <area>] (zu[machen]|<absperren>)` matches ['name_area', 'name_only'] — split into one template per combo.
- `<absperren> <name>[ <area>]` matches ['name_area', 'name_only'] — split into one template per combo.

### test unmapped (24)
- Test 'öffne das Rollo rechts' has slots ['domain', 'name'] matching no single combo.
- Test 'öffne den Vorhang rechts' has slots ['domain', 'name'] matching no single combo.
- Test 'öffne den Vorhang rechts im Wohnzimmer' has slots ['area', 'domain', 'name'] matching no single combo.
- Test 'öffne den Vorhang links im Obergeschoss' has slots ['domain', 'floor', 'name'] matching no single combo.
- Test 'öffne im Erdgeschoss das Tor' has slots ['domain', 'floor'] matching no single combo.
- Test 'öffne im Erdgeschoss alle Tore' has slots ['domain', 'floor'] matching no single combo.
- Test 'öffne alle Jalousien' has slots ['domain'] matching no single combo.
- Test 'schalte den Deckenventilator ein' has slots ['name'] matching no single combo.
- Test 'Partymodus an' has slots ['domain', 'name'] matching no single combo.
- Test 'Partymodus im Schlafzimmer an' has slots ['area', 'domain', 'name'] matching no single combo.
- Test 'schalte die Schlafzimmerlampe an' has slots ['domain', 'name'] matching no single combo.
- Test 'schalte die Stehlampe im Schlafzimmer an' has slots ['area', 'domain', 'name'] matching no single combo.
- Test 'schalte die Stehlampe im Obergeschoss an' has slots ['domain', 'floor', 'name'] matching no single combo.
- Test 'Schalte alle Lichter an' has slots ['domain'] matching no single combo.
- Test 'Schalte das Licht im Erdgeschoss an' has slots ['domain', 'floor'] matching no single combo.
- Test 'schalte alle Ventilatoren ein' has slots ['domain'] matching no single combo.
- Test 'schalte die Ventilatoren im Erdgeschoss ein' has slots ['domain', 'floor'] matching no single combo.
- Test 'starte alle ventilatoren im Erdgeschoss' has slots ['domain', 'floor'] matching no single combo.
- Test 'Öffne das Hauptventil' has slots ['domain', 'name'] matching no single combo.
- Test 'Öffne das Hauptventil in der Küche' has slots ['area', 'domain', 'name'] matching no single combo.
- Test 'Öffne das Hauptventil im Erdgeschoss' has slots ['domain', 'floor', 'name'] matching no single combo.
- Test 'Batteriewarnung ausführen' has slots ['domain', 'name'] matching no single combo.
- Test 'schließe die Haustür zu' has slots ['domain', 'name'] matching no single combo.
- Test 'schließe die Haustür im Flur zu' has slots ['area', 'domain', 'name'] matching no single combo.

### unmapped signature (25)
- `[<szene> ]<name>[(<aktivieren>|<ausfuehren>|<an>)]` has slots ['domain', 'name'] which match no single declared combo — check intents.yaml / domain.
- `<name> <szene> (<aktivieren>|<ausfuehren>|<an>)` has slots ['domain', 'name'] which match no single declared combo — check intents.yaml / domain.
- `führe[ <szene>] <name> aus` has slots ['domain', 'name'] which match no single declared combo — check intents.yaml / domain.
- `führe <name> <szene> aus` has slots ['domain', 'name'] which match no single declared combo — check intents.yaml / domain.
- `<aktivieren>[ <szene>] <name>` has slots ['domain', 'name'] which match no single declared combo — check intents.yaml / domain.
- `<aktivieren> <name> <szene>` has slots ['domain', 'name'] which match no single declared combo — check intents.yaml / domain.
- `führe[ <szene>] <name> <area> aus` has slots ['area', 'domain', 'name'] which match no single declared combo — check intents.yaml / domain.
- `führe <name> <szene> <area> aus` has slots ['area', 'domain', 'name'] which match no single declared combo — check intents.yaml / domain.
- `<aktivieren> <name> <szene> <area>` has slots ['area', 'domain', 'name'] which match no single declared combo — check intents.yaml / domain.
- `(<schalten>|<machen>) <alle_lichter_ueberall> an` has slots ['domain'] which match no single declared combo — check intents.yaml / domain.
- `(<schalten>|<machen>) überall [das ]<stt_fix_licht_an>` has slots ['domain'] which match no single declared combo — check intents.yaml / domain.
- `<schalten> <alle_lichter_ueberall> ein` has slots ['domain'] which match no single declared combo — check intents.yaml / domain.
- `dreh[e] <alle_lichter_ueberall> auf` has slots ['domain'] which match no single declared combo — check intents.yaml / domain.
- `<alle_lichter_ueberall> ((an|ein)[schalten]|anmachen|aufdrehen)` has slots ['domain'] which match no single declared combo — check intents.yaml / domain.
- `überall [das ]<stt_fix_licht_an>` has slots ['domain'] which match no single declared combo — check intents.yaml / domain.
- `starte <luefter_ueberall>` has slots ['domain'] which match no single declared combo — check intents.yaml / domain.
- `<schalten> <luefter_ueberall> (an|ein)` has slots ['domain'] which match no single declared combo — check intents.yaml / domain.
- `<machen> <luefter_ueberall> an` has slots ['domain'] which match no single declared combo — check intents.yaml / domain.
- `<luefter_ueberall> (an|(ein|an)schalten|anmachen)` has slots ['domain'] which match no single declared combo — check intents.yaml / domain.
- `[<skript> ]<name> (<ausfuehren>|<aktivieren>)` has slots ['domain', 'name'] which match no single declared combo — check intents.yaml / domain.
- `<name> <skript> (<ausfuehren>|<aktivieren>)` has slots ['domain', 'name'] which match no single declared combo — check intents.yaml / domain.
- `führe[ <skript>] <name> aus` has slots ['domain', 'name'] which match no single declared combo — check intents.yaml / domain.
- `führe <name> <skript> aus` has slots ['domain', 'name'] which match no single declared combo — check intents.yaml / domain.
- `<aktivieren>[ <skript>] <name>` has slots ['domain', 'name'] which match no single declared combo — check intents.yaml / domain.
- `<aktivieren> <name> <skript>` has slots ['domain', 'name'] which match no single declared combo — check intents.yaml / domain.

## Reminders (see docs/syntax_migration_guide.md)
- Inline list-bearing rules in templates (e.g. `<name>` -> `[de|het] {name}`).
- Flatten nested `<rule>` references.
- Add an `example:` taken from the matching test sentences.
- Delete the old `*_HassTurnOn.yaml` sentence/test files once done.
- Run `python3 -m script.intentfest validate --language de` and the tests.
