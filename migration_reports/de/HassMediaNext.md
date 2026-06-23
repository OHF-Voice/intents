# Migration report: de / HassMediaNext

## Declared slot combinations
- `default` context_area: true — scaffolded
- `name_only` slots: {name} — scaffolded
- `area_only` slots: {area} — scaffolded

## Scaffold files written
- /home/user/intents/sentences/de/HassMediaNext/name_only.yaml
- /home/user/intents/sentences/de/HassMediaNext/default.yaml
- /home/user/intents/sentences/de/HassMediaNext/area_only.yaml
- /home/user/intents/tests/de/HassMediaNext/name_only.yaml
- /home/user/intents/tests/de/HassMediaNext/default.yaml

## Old files to delete when done
(this intent may span several domain files — delete ALL of them)
- /home/user/intents/sentences/de/media_player_HassMediaNext.yaml
- /home/user/intents/tests/de/media_player_HassMediaNext.yaml

## Flags needing attention (26)

### complex template (22)
- `[<starte> ][(den|das|der) ]<naechster>[ <song>][ ((an|auf)[ dem]|am)] <name>` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(den|das) ]<naechster>[ <song>][ ((an|auf)[ dem]|am)] <name> <starten_end_of_sentence>` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(spring[e]|spul[e]) ]ein[en] <song> (vor[wärts]|weiter)[ ((an|auf)[ dem]|am)] <name>` has too many slot combinations to analyze — split it by hand from the reference language.
- `ein[en] <song> (vor[wärts]|weiter)[ ](springen|spulen)[ ((an|auf)[ dem]|am)] <name>` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(spring[e]|spul[e]) ]<zu_dem> <naechster> <song>[ (vor[wärts]|weiter)][ ((an|auf)[ dem]|am)] <name>` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(spring[e]|spul[e]) ][((an|auf)[ dem]|am) ]<name> <zu_dem> <naechster> <song>[ (vor[wärts]|weiter)]` has too many slot combinations to analyze — split it by hand from the reference language.
- `<zu_dem> <naechster> <song>[ (vor[wärts]|weiter)] (springen|spulen)[ ((an|auf)[ dem]|am)] <name>` has too many slot combinations to analyze — split it by hand from the reference language.
- `[((an|auf)[ dem]|am) ]<name> <zu_dem> <naechster> <song>[ (vor[wärts]|weiter)][ ](springen|spulen)` has too many slot combinations to analyze — split it by hand from the reference language.
- `überspring[e] ((das|dieses)[ eine]|ein) <song> [((an|auf)[ dem]|am) ]<name>` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(spring[e]|spul[e]) ]<zu_dem> <naechster> <song>[ (vor[wärts]|weiter)]` has too many slot combinations to analyze — split it by hand from the reference language.
- `[<starte> ][(den|das|der) ]<naechster>[ <song>] <area>` has too many slot combinations to analyze — split it by hand from the reference language.
- `[<starte> ]<area>[ (den|das|der)] <naechster>[ <song>]` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(den|das) ]<naechster>[ <song>] <area> <starten_end_of_sentence>` has too many slot combinations to analyze — split it by hand from the reference language.
- `<area> [(den|das) ]<naechster>[ <song>] <starten_end_of_sentence>` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(spring[e]|spul[e]) ]<area> ein[en] <song> (vor[wärts]|weiter)` has too many slot combinations to analyze — split it by hand from the reference language.
- `ein[en] <song> (vor[wärts]|weiter)[ ][(springen|spulen)] <area>` has too many slot combinations to analyze — split it by hand from the reference language.
- `(spring[e]|spul[e]) ein[en] <song> (vor[wärts]|weiter) <area>` has too many slot combinations to analyze — split it by hand from the reference language.
- `<area> ein[en] <song> (vor[wärts]|weiter)[ ](springen|spulen)` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(spring[e]|spul[e]) ]<zu_dem> <naechster> <song>[ (vor[wärts]|weiter)] <area>` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(spring[e]|spul[e]) ]<area> <zu_dem> <naechster> <song>[ (vor[wärts]|weiter)]` has too many slot combinations to analyze — split it by hand from the reference language.
- `<zu_dem> <naechster> <song>[ (vor[wärts]|weiter)] (springen|spulen) <area>` has too many slot combinations to analyze — split it by hand from the reference language.
- `<area> <zu_dem> <naechster> <song>[ (vor[wärts]|weiter)][ ](springen|spulen)` has too many slot combinations to analyze — split it by hand from the reference language.

### response default (3)
- `name_only`: old sentences had no `response`; defaulted to `default` — confirm the right response.
- `default`: old sentences had no `response`; defaulted to `default` — confirm the right response.
- `area_only`: old sentences had no `response`; defaulted to `default` — confirm the right response.

### test coverage (1)
- `area_only` has scaffolded sentences but no test file — add a test (old tests may have collapsed into another combo).

## Reminders (see docs/syntax_migration_guide.md)
- Inline list-bearing rules in templates (e.g. `<name>` -> `[de|het] {name}`).
- Flatten nested `<rule>` references.
- Add an `example:` taken from the matching test sentences.
- Delete the old `*_HassMediaNext.yaml` sentence/test files once done.
- Run `python3 -m script.intentfest validate --language de` and the tests.
