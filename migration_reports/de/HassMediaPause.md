# Migration report: de / HassMediaPause

## Declared slot combinations
- `default` context_area: true — scaffolded
- `name_only` slots: {name} — scaffolded
- `area_only` slots: {area} — scaffolded

## Scaffold files written
- /home/user/intents/sentences/de/HassMediaPause/name_only.yaml
- /home/user/intents/sentences/de/HassMediaPause/default.yaml
- /home/user/intents/sentences/de/HassMediaPause/area_only.yaml
- /home/user/intents/tests/de/HassMediaPause/name_only.yaml
- /home/user/intents/tests/de/HassMediaPause/default.yaml

## Old files to delete when done
(this intent may span several domain files — delete ALL of them)
- /home/user/intents/sentences/de/media_player_HassMediaPause.yaml
- /home/user/intents/tests/de/media_player_HassMediaPause.yaml

## Flags needing attention (11)

### complex template (6)
- `(stopp[e]|halt[e])[ (die|das|mein|meine)] <media_type>[ <hier>][ an]` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(die|das|mein|meine) ]<media_type> [<hier> ](pausieren|pause|anhalten|stop[p]|stoppen|aus[schalten])` has too many slot combinations to analyze — split it by hand from the reference language.
- `(stopp[e]|halt[e])[ (die|das|mein|meine)] <media_type> <area>[ an]` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(die|das|mein|meine) ]<media_type> <area> (pausieren|pause|anhalten|stop[p]|stoppen|aus[schalten])` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(die|das|mein|meine) ]<media_type> (pausieren|pause|anhalten|stop[p][en]|aus[schalten]|<stt_fix_aus_im>) <area>` has too many slot combinations to analyze — split it by hand from the reference language.
- `<area> [(die|das|mein|meine) ]<media_type> (pausieren|pause|anhalten|stop[p]|stoppen|aus[schalten])` has too many slot combinations to analyze — split it by hand from the reference language.

### response default (4)
- `name_only`: old sentences had no `response`; defaulted to `default` — confirm the right response.
- `default`: old sentences had no `response`; defaulted to `default` — confirm the right response.
- `area_only`: old sentences had no `response`; defaulted to `default` — confirm the right response.
- `area_only`: old sentences had no `response`; defaulted to `default` — confirm the right response.

### test coverage (1)
- `area_only` has scaffolded sentences but no test file — add a test (old tests may have collapsed into another combo).

## Reminders (see docs/syntax_migration_guide.md)
- Inline list-bearing rules in templates (e.g. `<name>` -> `[de|het] {name}`).
- Flatten nested `<rule>` references.
- Add an `example:` taken from the matching test sentences.
- Delete the old `*_HassMediaPause.yaml` sentence/test files once done.
- Run `python3 -m script.intentfest validate --language de` and the tests.
