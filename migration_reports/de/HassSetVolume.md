# Migration report: de / HassSetVolume

## Declared slot combinations
- `default` slots: {volume_level}; context_area: true — scaffolded
- `name_only` slots: {name}, {volume_level} — scaffolded
- `area_only` slots: {area}, {volume_level} — EMPTY — non-required, safe to skip

## Scaffold files written
- /home/user/intents/sentences/de/HassSetVolume/name_only.yaml
- /home/user/intents/sentences/de/HassSetVolume/default.yaml
- /home/user/intents/tests/de/HassSetVolume/name_only.yaml
- /home/user/intents/tests/de/HassSetVolume/default.yaml

## Old files to delete when done
(this intent may span several domain files — delete ALL of them)
- /home/user/intents/sentences/de/media_player_HassSetVolume.yaml
- /home/user/intents/tests/de/media_player_HassSetVolume.yaml

## Flags needing attention (13)

### complex template (10)
- `<setzen> [die ]Lautstärke[ von] <name>[ auf] <volume>` has too many slot combinations to analyze — split it by hand from the reference language.
- `[die ]Lautstärke[ von] <name>[ auf] <volume>[ <setzen_end_of_sentence>]` has too many slot combinations to analyze — split it by hand from the reference language.
- `<setzen> [die ]Lautstärke[ <von_dem>] <name> auf [(die|das) ]{volume_mapping:volume_level}[ Stufe]` has too many slot combinations to analyze — split it by hand from the reference language.
- `<stelle> [die ]Lautstärke[ <von_dem>] <name> auf [(die|das) ]{volume_mapping:volume_level}[ Stufe] ein` has too many slot combinations to analyze — split it by hand from the reference language.
- `[die ]Lautstärke[ <von_dem>] <name> auf [(die|das) ]{volume_mapping:volume_level}[ Stufe] <setzen_end_of_sentence>` has too many slot combinations to analyze — split it by hand from the reference language.
- `[die ]Lautstärke[ <hier>][ (auf|zu)] <volume>[ <setzen_end_of_sentence>]` has too many slot combinations to analyze — split it by hand from the reference language.
- `[die ]Lautstärke[ <hier>][ auf] [(die|das) ]{volume_mapping:volume_level}[ Stufe][ <setzen_end_of_sentence>]` has too many slot combinations to analyze — split it by hand from the reference language.
- `<setzen> [die ]Lautstärke[ (in|im)] <area>[ auf] <volume>` has too many slot combinations to analyze — split it by hand from the reference language.
- `<stelle> [die ]Lautstärke[ (in|im)] <area>[ auf] <volume> ein` has too many slot combinations to analyze — split it by hand from the reference language.
- `[die ]Lautstärke[ (in|im)] <area>[ (auf|zu)] <volume>[ <setzen_end_of_sentence>]` has too many slot combinations to analyze — split it by hand from the reference language.

### response default (3)
- `name_only`: old sentences had no `response`; defaulted to `default` — confirm the right response.
- `name_only`: old sentences had no `response`; defaulted to `default` — confirm the right response.
- `default`: old sentences had no `response`; defaulted to `default` — confirm the right response.

## Reminders (see docs/syntax_migration_guide.md)
- Inline list-bearing rules in templates (e.g. `<name>` -> `[de|het] {name}`).
- Flatten nested `<rule>` references.
- Add an `example:` taken from the matching test sentences.
- Delete the old `*_HassSetVolume.yaml` sentence/test files once done.
- Run `python3 -m script.intentfest validate --language de` and the tests.
