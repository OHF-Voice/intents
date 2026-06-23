# Migration report: de / HassMediaSearchAndPlay

## Declared slot combinations
- `default` slots: {search_query}; context_area: true — scaffolded
- `name_only` slots: {name}, {search_query} — EMPTY — non-required, safe to skip
- `area_only` slots: {area}, {search_query} — scaffolded
- `name_area` slots: {area}, {name}, {search_query} — EMPTY — non-required, safe to skip
- `media_class_only` slots: {media_class}, {search_query}; context_area: true — scaffolded
- `name_media_class` slots: {media_class}, {name}, {search_query} — EMPTY — non-required, safe to skip
- `area_media_class` slots: {area}, {media_class}, {search_query} — scaffolded
- `name_area_media_class` slots: {area}, {media_class}, {name}, {search_query} — EMPTY — non-required, safe to skip

## Scaffold files written
- /home/user/intents/sentences/de/HassMediaSearchAndPlay/media_class_only.yaml
- /home/user/intents/sentences/de/HassMediaSearchAndPlay/default.yaml
- /home/user/intents/sentences/de/HassMediaSearchAndPlay/area_media_class.yaml
- /home/user/intents/sentences/de/HassMediaSearchAndPlay/area_only.yaml
- /home/user/intents/tests/de/HassMediaSearchAndPlay/default.yaml
- /home/user/intents/tests/de/HassMediaSearchAndPlay/media_class_only.yaml
- /home/user/intents/tests/de/HassMediaSearchAndPlay/name_only.yaml
- /home/user/intents/tests/de/HassMediaSearchAndPlay/name_media_class.yaml
- /home/user/intents/tests/de/HassMediaSearchAndPlay/area_only.yaml
- /home/user/intents/tests/de/HassMediaSearchAndPlay/name_area.yaml
- /home/user/intents/tests/de/HassMediaSearchAndPlay/name_area_media_class.yaml
- /home/user/intents/tests/de/HassMediaSearchAndPlay/area_media_class.yaml

## Old files to delete when done
(this intent may span several domain files — delete ALL of them)
- /home/user/intents/sentences/de/media_player_HassMediaSearchAndPlay.yaml
- /home/user/intents/tests/de/media_player_HassMediaSearchAndPlay.yaml

## Flags needing attention (13)

### complex template (8)
- `spiel[e] {media_class} {search_query}[ (<an>|am)] <name>[ <area>][ ab]` has too many slot combinations to analyze — split it by hand from the reference language.
- `spiel[e] {search_query}[ (<an>|am)] <name>[ <area>][ ab]` has too many slot combinations to analyze — split it by hand from the reference language.
- `{media_class} {search_query}[ (<an>|am)] <name>[ <area>] <starten_end_of_sentence>` has too many slot combinations to analyze — split it by hand from the reference language.
- `{search_query}[ (<an>|am)] <name>[ <area>] <starten_end_of_sentence>` has too many slot combinations to analyze — split it by hand from the reference language.
- `spiel[e] <my_query_class>[ (<an>|am)] <name>[ <area>][ ab]` has too many slot combinations to analyze — split it by hand from the reference language.
- `spiel[e][ (<an>|am)] <name>[ <area>] <my_query_class>[ ab]` has too many slot combinations to analyze — split it by hand from the reference language.
- `<my_query_class>[ (<an>|am)] <name>[ <area>] <starten_end_of_sentence>` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(<an>|am) ]<name>[ <area>] <my_query_class> <starten_end_of_sentence>` has too many slot combinations to analyze — split it by hand from the reference language.

### response default (4)
- `media_class_only`: old sentences had no `response`; defaulted to `default` — confirm the right response.
- `default`: old sentences had no `response`; defaulted to `default` — confirm the right response.
- `area_media_class`: old sentences had no `response`; defaulted to `default` — confirm the right response.
- `area_only`: old sentences had no `response`; defaulted to `default` — confirm the right response.

### unresolved rule (1)
- `<my_query_class>` is not in rules/de/ — inline it into the templates or move it there (the test harness ignores _common.yaml).

## Reminders (see docs/syntax_migration_guide.md)
- Inline list-bearing rules in templates (e.g. `<name>` -> `[de|het] {name}`).
- Flatten nested `<rule>` references.
- Add an `example:` taken from the matching test sentences.
- Delete the old `*_HassMediaSearchAndPlay.yaml` sentence/test files once done.
- Run `python3 -m script.intentfest validate --language de` and the tests.
