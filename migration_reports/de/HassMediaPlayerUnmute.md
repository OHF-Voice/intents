# Migration report: de / HassMediaPlayerUnmute

## Declared slot combinations
- `default` context_area: true — EMPTY — non-required, safe to skip
- `name_only` slots: {name} — EMPTY — non-required, safe to skip

## Scaffold files written
- /home/user/intents/tests/de/HassMediaPlayerUnmute/default.yaml
- /home/user/intents/tests/de/HassMediaPlayerUnmute/name_only.yaml

## Old files to delete when done
(this intent may span several domain files — delete ALL of them)
- /home/user/intents/sentences/de/media_player_HassMediaPlayerUnmute.yaml
- /home/user/intents/tests/de/media_player_HassMediaPlayerUnmute.yaml

## Flags needing attention (2)

### complex template (2)
- `[<source_of_noise> ][<hier> ]<media_unmute>` has too many slot combinations to analyze — split it by hand from the reference language.
- `[<source_of_noise> ((auf|von)[ dem]|vom) ]<name> <media_unmute>` has too many slot combinations to analyze — split it by hand from the reference language.

## Reminders (see docs/syntax_migration_guide.md)
- Inline list-bearing rules in templates (e.g. `<name>` -> `[de|het] {name}`).
- Flatten nested `<rule>` references.
- Add an `example:` taken from the matching test sentences.
- Delete the old `*_HassMediaPlayerUnmute.yaml` sentence/test files once done.
- Run `python3 -m script.intentfest validate --language de` and the tests.
