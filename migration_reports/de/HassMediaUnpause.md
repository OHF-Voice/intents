# Migration report: de / HassMediaUnpause

## Declared slot combinations
- `default` context_area: true — scaffolded
- `name_only` slots: {name} — scaffolded
- `area_only` slots: {area} — scaffolded

## Scaffold files written
- /home/user/intents/sentences/de/HassMediaUnpause/name_only.yaml
- /home/user/intents/sentences/de/HassMediaUnpause/default.yaml
- /home/user/intents/sentences/de/HassMediaUnpause/area_only.yaml
- /home/user/intents/tests/de/HassMediaUnpause/name_only.yaml
- /home/user/intents/tests/de/HassMediaUnpause/default.yaml

## Old files to delete when done
(this intent may span several domain files — delete ALL of them)
- /home/user/intents/sentences/de/media_player_HassMediaUnpause.yaml
- /home/user/intents/tests/de/media_player_HassMediaUnpause.yaml

## Flags needing attention (16)

### complex template (10)
- `[[(die|das|mein|meine) ]<media_type> ][<hier> ](fortsetzen|weiter[ (machen|<local_play>)]|wieder <local_play>)` has too many slot combinations to analyze — split it by hand from the reference language.
- `[[(die|das|mein|meine) ]<media_type> ][<hier> ]weiter(machen|schauen|hören|spielen|laufen lassen)` has too many slot combinations to analyze — split it by hand from the reference language.
- `lass [(die|das|mein|meine) ]<media_type> [<hier> ]wieder (starten|[ab]spielen|laufen)` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(die|das|mein|meine) ]<media_type> <area> (fortsetzen|weiter[ (machen|<local_play>)])` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(die|das|mein|meine) ]<media_type> <area> weiter(machen|schauen|hören|spielen|laufen lassen)` has too many slot combinations to analyze — split it by hand from the reference language.
- `spiel[e] [(die|das|mein|meine) ]<media_type> <area> (wieder ab|weiter[ ab])` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(die|das|mein|meine) ]<media_type> <area> wieder (starten|[ab]spielen|laufen lassen)` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(die|das|mein|meine) ]<media_type> <area> weiter[ ]([ab]spielen|laufen lassen)` has too many slot combinations to analyze — split it by hand from the reference language.
- `lass [(die|das|mein|meine) ]<media_type> <area> wieder (starten|[ab]spielen|laufen)` has too many slot combinations to analyze — split it by hand from the reference language.
- `lass [(die|das|mein|meine) ]<media_type> <area> weiter ([ab]spielen|laufen)` has too many slot combinations to analyze — split it by hand from the reference language.

### response default (4)
- `name_only`: old sentences had no `response`; defaulted to `default` — confirm the right response.
- `default`: old sentences had no `response`; defaulted to `default` — confirm the right response.
- `area_only`: old sentences had no `response`; defaulted to `default` — confirm the right response.
- `area_only`: old sentences had no `response`; defaulted to `default` — confirm the right response.

### test coverage (1)
- `area_only` has scaffolded sentences but no test file — add a test (old tests may have collapsed into another combo).

### unresolved rule (1)
- `<local_play>` is not in rules/de/ — inline it into the templates or move it there (the test harness ignores _common.yaml).

## Reminders (see docs/syntax_migration_guide.md)
- Inline list-bearing rules in templates (e.g. `<name>` -> `[de|het] {name}`).
- Flatten nested `<rule>` references.
- Add an `example:` taken from the matching test sentences.
- Delete the old `*_HassMediaUnpause.yaml` sentence/test files once done.
- Run `python3 -m script.intentfest validate --language de` and the tests.
