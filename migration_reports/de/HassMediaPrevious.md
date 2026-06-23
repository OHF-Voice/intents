# Migration report: de / HassMediaPrevious

## Declared slot combinations
- `default` context_area: true — scaffolded
- `name_only` slots: {name} — EMPTY — non-required, safe to skip
- `area_only` slots: {area} — scaffolded

## Scaffold files written
- /home/user/intents/sentences/de/HassMediaPrevious/default.yaml
- /home/user/intents/sentences/de/HassMediaPrevious/area_only.yaml
- /home/user/intents/tests/de/HassMediaPrevious/name_only.yaml
- /home/user/intents/tests/de/HassMediaPrevious/default.yaml

## Old files to delete when done
(this intent may span several domain files — delete ALL of them)
- /home/user/intents/sentences/de/media_player_HassMediaPrevious.yaml
- /home/user/intents/tests/de/media_player_HassMediaPrevious.yaml

## Flags needing attention (33)

### complex template (30)
- `[(<starte>[ (den|das)]|<wiederhole>) ]<vorheriger_letzter>[ <song>][ ((an|auf)[ dem]|am)] <name>` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(den|das) ]<vorheriger_letzter>[ <song>][ ((an|auf)[ dem]|am)] <name> [nochmal ](<starten_end_of_sentence>|wiederholen)` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(<starte>[ (den|das)]|<wiederhole>) ]<song>[ ((an|auf)[ dem]|am)] <name> nochmal[ ab]` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(spring[e]|spul[e]) ]ein[en] <song> (zurück|rückwärts)[ ((an|auf)[ dem]|am)] <name>` has too many slot combinations to analyze — split it by hand from the reference language.
- `ein[en] <song> (zurück|rückwärts)[ ](springen|spulen)[ ((an|auf)[ dem]|am)] <name>` has too many slot combinations to analyze — split it by hand from the reference language.
- `<wiederhole> [(den|das) ]<song>[ ((an|auf)[ dem]|am)] <name>[ nochmal]` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(den|das) ]<song>[ ((an|auf)[ dem]|am)] <name> (nochmal <starten_end_of_sentence>|[nochmal ]wiederholen)` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(spring[e]|spul[e]) ]ein[en] <song> (zurück|rückwärts)[ ((an|auf)[ dem]|am)] <name>` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(spring[e]|spul[e]) ]<zu_dem> <vorheriger_letzter> <song>[ (zurück|rückwärts)][ ((an|auf)[ dem]|am)] <name>` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(spring[e]|spul[e]) ][((an|auf)[ dem]|am) ]<name> <zu_dem> <vorheriger_letzter> <song>[ (zurück|rückwärts)]` has too many slot combinations to analyze — split it by hand from the reference language.
- `<zu_dem> <vorheriger_letzter> <song>[ (zurück|rückwärts)] (springen|spulen)[ ((an|auf)[ dem]|am)] <name>` has too many slot combinations to analyze — split it by hand from the reference language.
- `[((an|auf)[ dem]|am) ]<name> <zu_dem> <vorheriger_letzter> <song>[ (zurück|rückwärts)][ ](springen|spulen)` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(den|das) ]<vorheriger_letzter>[ <song>][ nochmal] (<starten_end_of_sentence>|wiederholen)` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(<starte>[ (den|das)]|<wiederhole>) ][<vorheriger_letzter> ]<song> nochmal[ ab]` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(spring[e]|spul[e]) ]<zu_dem> <vorheriger_letzter> <song>[ (zurück|rückwärts)]` has too many slot combinations to analyze — split it by hand from the reference language.
- `<zu_dem> <vorheriger_letzter> <song>[ (zurück|rückwärts)][ ](springen|spulen)` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(<starte>[ (den|das)]|<wiederhole>) ]<vorheriger_letzter>[ <song>] <area>` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(<starte>|<wiederhole>) ]<area>[ (den|das)] <vorheriger_letzter>[ <song>]` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(den|das|der) ]<vorheriger_letzter>[ <song>] <area>[ nochmal][ (<starten_end_of_sentence>|wiederholen)]` has too many slot combinations to analyze — split it by hand from the reference language.
- `<area> [(den|das) ]<vorheriger_letzter>[ <song>][ nochmal] (<starten_end_of_sentence>|wiederholen)` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(den|das) ]<song> <area> (nochmal <starten_end_of_sentence>|[nochmal ]wiederholen)` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(den|das) ]<song> (nochmal <starten_end_of_sentence>|[nochmal ]wiederholen) <area>` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(spring[e]|spul[e]) ]<area> ein[en] <song> (zurück|rückwärts)` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(spring[e]|spul[e]) ]ein[en] <song> (zurück|rückwärts) <area>` has too many slot combinations to analyze — split it by hand from the reference language.
- `ein[en] <song> (zurück|rückwärts)[ ](springen|spulen) <area>` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(spring[e]|spul[e]) ]<zu_dem> <vorheriger_letzter> <song>[ (zurück|rückwärts)] <area>` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(spring[e]|spul[e]) ]<area> <zu_dem> <vorheriger_letzter> <song>[ (zurück|rückwärts)]` has too many slot combinations to analyze — split it by hand from the reference language.
- `<zu_dem> <vorheriger_letzter> <song>[ (zurück|rückwärts)][ ](springen|spulen) <area>` has too many slot combinations to analyze — split it by hand from the reference language.
- `<area> <zu_dem> <vorheriger_letzter> <song>[ (zurück|rückwärts)][ ](springen|spulen)` has too many slot combinations to analyze — split it by hand from the reference language.
- `<wiederhole> <song> <area>[ nochmal]` has too many slot combinations to analyze — split it by hand from the reference language.

### response default (2)
- `default`: old sentences had no `response`; defaulted to `default` — confirm the right response.
- `area_only`: old sentences had no `response`; defaulted to `default` — confirm the right response.

### test coverage (1)
- `area_only` has scaffolded sentences but no test file — add a test (old tests may have collapsed into another combo).

## Reminders (see docs/syntax_migration_guide.md)
- Inline list-bearing rules in templates (e.g. `<name>` -> `[de|het] {name}`).
- Flatten nested `<rule>` references.
- Add an `example:` taken from the matching test sentences.
- Delete the old `*_HassMediaPrevious.yaml` sentence/test files once done.
- Run `python3 -m script.intentfest validate --language de` and the tests.
