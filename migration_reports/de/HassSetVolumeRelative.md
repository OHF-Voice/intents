# Migration report: de / HassSetVolumeRelative

## Declared slot combinations
- `default` slots: {volume_step}; context_area: true — scaffolded
- `name_only` slots: {name}, {volume_step} — scaffolded
- `area_only` slots: {area}, {volume_step} — EMPTY — non-required, safe to skip
- `floor_only` slots: {floor}, {volume_step} — EMPTY — non-required, safe to skip

## Scaffold files written
- /home/user/intents/sentences/de/HassSetVolumeRelative/default.yaml
- /home/user/intents/sentences/de/HassSetVolumeRelative/name_only.yaml
- /home/user/intents/tests/de/HassSetVolumeRelative/default.yaml
- /home/user/intents/tests/de/HassSetVolumeRelative/name_only.yaml
- /home/user/intents/tests/de/HassSetVolumeRelative/floor_only.yaml

## Old files to delete when done
(this intent may span several domain files — delete ALL of them)
- /home/user/intents/sentences/de/media_player_HassSetVolumeRelative.yaml
- /home/user/intents/tests/de/media_player_HassSetVolumeRelative.yaml

## Flags needing attention (51)

### complex template (35)
- `[(mach[e]|stell[e]) ]([den ]ton|[die ]lautstärke[ der Musik]|[die ]Musik) <von_dem> <name> [(etwas|ein bisschen|ein wenig) ]leiser` has too many slot combinations to analyze — split it by hand from the reference language.
- `([den ]ton|[die ]lautstärke[ der Musik]|[die ]Musik) <von_dem> <name> [(etwas|ein bisschen|ein wenig) ]leiser (machen|[ein]stellen)` has too many slot combinations to analyze — split it by hand from the reference language.
- `[die ]lautstärke[ der Musik] <von_dem> <name> [(etwas|ein bisschen|ein wenig) ](verringern|reduzieren|[ab]senken|[he]runterdrehen)` has too many slot combinations to analyze — split it by hand from the reference language.
- `dreh[e] die lautstärke[ der Musik] <von_dem> <name> [(etwas|ein bisschen|ein wenig) ][he]runter` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(mach[e]|stell[e]) ]([den ]ton|[die ]lautstärke[ der Musik]|[die ]Musik) <von_dem> <name>[ um] <volume_step> leiser` has too many slot combinations to analyze — split it by hand from the reference language.
- `([den ]ton|[die ]lautstärke[ der Musik]|[die ]Musik) <von_dem> <name>[ um] <volume_step> leiser (machen|[ein]stellen)` has too many slot combinations to analyze — split it by hand from the reference language.
- `[die ]lautstärke[ der Musik] <von_dem> <name>[ um] <volume_step> (verringern|reduzieren|[ab]senken|[he]runterdrehen)` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(mach[e]|stell[e]) ]([den ]ton|[die ]lautstärke[ der Musik]|[die ]Musik) <von_dem> <name> [(etwas|ein bisschen|ein wenig) ]lauter` has too many slot combinations to analyze — split it by hand from the reference language.
- `([den ]ton|[die ]lautstärke[ der Musik]|[die ]Musik) <von_dem> <name> [(etwas|ein bisschen|ein wenig) ]lauter (machen|[ein]stellen)` has too many slot combinations to analyze — split it by hand from the reference language.
- `[die ]lautstärke[ der Musik] <von_dem> <name> [(etwas|ein bisschen|ein wenig) ](erhöhen|[her]aufdrehen)` has too many slot combinations to analyze — split it by hand from the reference language.
- `dreh[e] die lautstärke[ der Musik] <von_dem> <name> [(etwas|ein bisschen|ein wenig) ]([he]rauf|auf)` has too many slot combinations to analyze — split it by hand from the reference language.
- `[(mach[e]|stell[e]) ]([den ]ton|[die ]lautstärke[ der Musik]|[die ]Musik) <von_dem> <name>[ um] <volume_step> lauter` has too many slot combinations to analyze — split it by hand from the reference language.
- `([den ]ton|[die ]lautstärke[ der Musik]|[die ]Musik) <von_dem> <name>[ um] <volume_step> lauter (machen|[ein]stellen)` has too many slot combinations to analyze — split it by hand from the reference language.
- `(({area}|{floor}) [(etwas|ein bisschen|ein wenig) ]leiser|[[die ]Musik ][(etwas|ein bisschen|ein wenig) ]leiser <area_floor>)` has too many slot combinations to analyze — split it by hand from the reference language.
- `([mach[e] den ]ton|[stell[e] die ]lautstärke[ der Musik]|[[mach[e] ]die ]Musik) <area_floor> [(etwas|ein bisschen|ein wenig) ]leiser` has too many slot combinations to analyze — split it by hand from the reference language.
- `([den ]ton|[die ]lautstärke[ der Musik]|[die ]Musik) <area_floor> [(etwas|ein bisschen|ein wenig) ]leiser (machen|[ein]stellen)` has too many slot combinations to analyze — split it by hand from the reference language.
- `(verringere|reduziere) die lautstärke[ der Musik] <area_floor>[ (etwas|ein bisschen|ein wenig)]` has too many slot combinations to analyze — split it by hand from the reference language.
- `senke die lautstärke[ der Musik] <area_floor>[ (etwas|ein bisschen|ein wenig)][ ab]` has too many slot combinations to analyze — split it by hand from the reference language.
- `[die ]lautstärke[ der Musik] <area_floor> [(etwas|ein bisschen|ein wenig) ](verringern|reduzieren|[ab]senken|[he]runterdrehen)` has too many slot combinations to analyze — split it by hand from the reference language.
- `dreh[e] die lautstärke[ der Musik] <area_floor> [(etwas|ein bisschen|ein wenig) ][he]runter` has too many slot combinations to analyze — split it by hand from the reference language.
- `([mach[e] den ]ton|[stell[e] die ]lautstärke[ der Musik]|[[mach[e] ]die ]Musik) <area_floor>[ um] <volume_step> leiser` has too many slot combinations to analyze — split it by hand from the reference language.
- `([den ]ton|[die ]lautstärke[ der Musik]|[die ]Musik) <area_floor>[ um] <volume_step> leiser (machen|[ein]stellen)` has too many slot combinations to analyze — split it by hand from the reference language.
- `senke die lautstärke[ der Musik] <area_floor>[ um] <volume_step>[ ab]` has too many slot combinations to analyze — split it by hand from the reference language.
- `senke die lautstärke[ der Musik][ um] <volume_step> <area_floor>[ ab]` has too many slot combinations to analyze — split it by hand from the reference language.
- `[die ]lautstärke[ der Musik] <area_floor>[ um] <volume_step> (verringern|reduzieren|[ab]senken|[he]runterdrehen)` has too many slot combinations to analyze — split it by hand from the reference language.
- `dreh[e] die lautstärke[ der Musik] <area_floor>[ um] <volume_step> [he]runter` has too many slot combinations to analyze — split it by hand from the reference language.
- `(({area}|{floor}) [(etwas|ein bisschen|ein wenig) ]lauter|[[die ]Musik ][(etwas|ein bisschen|ein wenig) ]lauter <area_floor>)` has too many slot combinations to analyze — split it by hand from the reference language.
- `([mach[e] den ]ton|[stell[e] die ]lautstärke[ der Musik]|[[mach[e] ]die ]Musik) <area_floor> [(etwas|ein bisschen|ein wenig) ]lauter` has too many slot combinations to analyze — split it by hand from the reference language.
- `([den ]ton|[die ]lautstärke[ der Musik]|[die ]Musik) <area_floor> [(etwas|ein bisschen|ein wenig) ]lauter (machen|[ein]stellen)` has too many slot combinations to analyze — split it by hand from the reference language.
- `[die ]lautstärke[ der Musik] <area_floor> [(etwas|ein bisschen|ein wenig) ](erhöhen|[her]aufdrehen)` has too many slot combinations to analyze — split it by hand from the reference language.
- `dreh[e] die lautstärke[ der Musik] <area_floor> [(etwas|ein bisschen|ein wenig) ]([he]rauf|auf)` has too many slot combinations to analyze — split it by hand from the reference language.
- `([mach[e] den ]ton|[stell[e] die ]lautstärke[ der Musik]|[[mach[e] ]die ]Musik) <area_floor>[ um] <volume_step> lauter` has too many slot combinations to analyze — split it by hand from the reference language.
- `([den ]ton|[die ]lautstärke[ der Musik]|[die ]Musik) <area_floor>[ um] <volume_step> lauter (machen|[ein]stellen)` has too many slot combinations to analyze — split it by hand from the reference language.
- `[die ]lautstärke[ der Musik] <area_floor>[ um] <volume_step> (erhöhen|[her]aufdrehen)` has too many slot combinations to analyze — split it by hand from the reference language.
- `dreh[e] die lautstärke[ der Musik] <area_floor>[ um] <volume_step> ([he]rauf|auf)` has too many slot combinations to analyze — split it by hand from the reference language.

### multi-combo template (7)
- `(({area}|{floor})[ um] <volume_step> leiser|[[die ]Musik ]<volume_step> leiser <area_floor>)` matches ['area_only', 'floor_only'] — split into one template per combo.
- `(verringere|reduziere) die lautstärke[ der Musik] <area_floor>[ um] <volume_step>` matches ['area_only', 'floor_only'] — split into one template per combo.
- `(verringere|reduziere) die lautstärke[ der Musik][ um] <volume_step> <area_floor>` matches ['area_only', 'floor_only'] — split into one template per combo.
- `erhöhe die lautstärke[ der Musik] <area_floor>[ (etwas|ein bisschen|ein wenig)]` matches ['area_only', 'floor_only'] — split into one template per combo.
- `(({area}|{floor})[ um] <volume_step> lauter|[[die ]Musik ]<volume_step> lauter <area_floor>)` matches ['area_only', 'floor_only'] — split into one template per combo.
- `erhöhe die lautstärke[ der Musik] <area_floor>[ um] <volume_step>` matches ['area_only', 'floor_only'] — split into one template per combo.
- `erhöhe die lautstärke[ der Musik][ um] <volume_step> <area_floor>` matches ['area_only', 'floor_only'] — split into one template per combo.

### response default (8)
- `default`: old sentences had no `response`; defaulted to `default` — confirm the right response.
- `default`: old sentences had no `response`; defaulted to `default` — confirm the right response.
- `default`: old sentences had no `response`; defaulted to `default` — confirm the right response.
- `default`: old sentences had no `response`; defaulted to `default` — confirm the right response.
- `name_only`: old sentences had no `response`; defaulted to `default` — confirm the right response.
- `name_only`: old sentences had no `response`; defaulted to `default` — confirm the right response.
- `name_only`: old sentences had no `response`; defaulted to `default` — confirm the right response.
- `name_only`: old sentences had no `response`; defaulted to `default` — confirm the right response.

### unresolved rule (1)
- `<volume_step>` is not in rules/de/ — inline it into the templates or move it there (the test harness ignores _common.yaml).

## Reminders (see docs/syntax_migration_guide.md)
- Inline list-bearing rules in templates (e.g. `<name>` -> `[de|het] {name}`).
- Flatten nested `<rule>` references.
- Add an `example:` taken from the matching test sentences.
- Delete the old `*_HassSetVolumeRelative.yaml` sentence/test files once done.
- Run `python3 -m script.intentfest validate --language de` and the tests.
