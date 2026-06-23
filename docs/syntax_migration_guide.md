# Migration Guide: Old Template Syntax → Slot Combinations

This guide explains how to migrate sentences written in the original
[HassIL template format](templates.md) (as documented in
[`hassil`](../../hassil/docs/template_syntax.md)) to the new
**slot combination** format described in [`slot_combinations.md`](slot_combinations.md).

The _template syntax itself_ (alternatives `(a|b)`, optionals `[x]`, lists
`{list}`, rules `<rule>`, permutations `(a;b)`) is **unchanged**. What changes
is **how files are organized**, **where lists and rules live**, **how target
domains are declared**, and a few **new restrictions** on what a template may
contain.

- [At a glance](#at-a-glance)
- [1. Sentence files: group by slot combination](#1-sentence-files-group-by-slot-combination)
- [2. Declaring target domains (`requires_context` is gone)](#2-declaring-target-domains-requires_context-is-gone)
- [3. Lists move out of `_common.yaml`](#3-lists-move-out-of-_commonyaml)
- [4. Rules move out of `_common.yaml`](#4-rules-move-out-of-_commonyaml)
- [5. New template restrictions](#5-new-template-restrictions)
- [6. Tests](#6-tests)
- [7. Tooling: scaffold one intent at a time](#7-tooling-scaffold-one-intent-at-a-time)
- [8. Lessons from practice (gotchas)](#8-lessons-from-practice-gotchas)
- [Migration checklist](#migration-checklist)
- [Adversarial review (final step)](#adversarial-review-final-step)

## At a glance

| Concern        | Old format                                                | New format                                                       |
| -------------- | --------------------------------------------------------- | ---------------------------------------------------------------- |
| Sentence files | `sentences/<lang>/<domain>_<intent>.yaml`                 | `sentences/<lang>/<intent>/<slot_combination>.yaml`              |
| File root      | `intents: <Intent>: data:`                                | `data:` (intent & slot combination come from the path)           |
| Grouping       | By intent (and ad‑hoc by domain in the filename)          | By **slot combination**, declared in `intents.yaml`              |
| Target domain  | `requires_context: { domain: ... }` / `slots: { domain }` | `name_domains:` / `inferred_domain:` in each sentence group      |
| Lists          | `sentences/<lang>/_common.yaml` → `lists:`                | `lists/<lang>/<group>.yaml` (or shared `lists/<group>.yaml`)     |
| Rules          | `sentences/<lang>/_common.yaml` → `expansion_rules:`      | `rules/<lang>/<group>.yaml`                                      |
| Tests          | `tests/<lang>/<domain>_<intent>.yaml`                     | `tests/<lang>/<intent>/<slot_combination>.yaml` (self‑contained) |

## 1. Sentence files: group by slot combination

In the old format, all of an intent's sentences lived in one file per
domain/intent pair, under a top-level `intents:` block:

```yaml
# OLD: sentences/en/light_HassTurnOn.yaml
language: "en"
intents:
  HassTurnOn:
    data:
      # Turn on a specific light
      - sentences:
          - "<turn> on <name> <light>"
        requires_context:
          domain: "light"

      # Turn on all lights in an area
      - sentences:
          - "<turn> on [<the>] <light> <in> <area>"
        slots:
          domain: "light"
        response: "lights_area"
```

In the new format, sentences are split into **one file per slot combination**.
The slot combinations are declared once in the root `intents.yaml`, and each
gets its own file at `sentences/<lang>/<intent>/<slot_combination>.yaml`. The
`intents:`/`<Intent>:` nesting is gone — the file starts directly at `data:`,
because the intent and slot combination are implied by the path.

```yaml
# NEW: sentences/en/HassTurnOn/name_only.yaml
language: "en"
data:
  - sentences:
      - "<turn> on [<the>] {name}"
    name_domains:
      - "light"
    example: "turn on the overhead light" # use names from tests
    response: "default"
```

```yaml
# NEW: sentences/en/HassTurnOn/domain_only.yaml
language: "en"
data:
  - sentences:
      - "<turn> on [<the>] <light> <here>"
    inferred_domain: "light"
    example: "turn on the lights in here"
    response: "lights_area"
```

To know which files an intent needs, look at its `slot_combinations` in
`intents.yaml`. A slot combination whose `importance` is `required` (or that has
any `required` entries under `name_domains` / `inferred_domains`) **must** have a
matching sentence file; `usable` combinations produce a warning when missing.

> All templates in a slot combination file must match **exactly** the slots
> listed for that combination in `intents.yaml`. Don't mix sentences that match
> different slots into the same file.

## 2. Declaring target domains (`requires_context` is gone)

Previously, template authors hand-wrote the matching context so the intent would
only fire for the right entity domain:

```yaml
# OLD
- sentences:
    - "<turn> on [<the>] {name}"
  requires_context:
    domain: "light"
```

In the new format you **no longer write `requires_context`**. The information
needed to generate it lives in `intents.yaml`, under `name_domains` (when the
`{name}` slot is used) or `inferred_domains` (when the domain is inferred from
the words, e.g. "turn on the lights"):

```yaml
# intents.yaml
HassTurnOn:
  slot_combinations:
    name_only:
      slots: ["name"]
      name_domains:
        required: ["light", "cover"]
        complete: ["valve"]
```

In the sentence file you then just list which of those domains each group of
sentences covers, using `name_domains:` (a list) or `inferred_domain:` (a single
value — no "s", since only one domain can be inferred):

```yaml
# NEW: sentences/en/HassTurnOn/name_only.yaml
language: "en"
data:
  # lights and switches
  - sentences:
      - "<turn> on [<the>] {name}"
    name_domains:
      - "light"
    response: "default"

  # covers
  - sentences:
      - "<open> [<the>] {name}"
    name_domains:
      - "cover"
    response: "cover"
```

Every domain marked `required` in `intents.yaml` must be covered somewhere in the
file, but not necessarily by the same group of sentences — split them in whatever
way reads best for your language. Non-required levels (`usable`, `complete`,
`optional`) only affect the language's coverage score.

## 3. Lists move out of `_common.yaml`

Lists used to live in `sentences/<lang>/_common.yaml` under a `lists:` key:

```yaml
# OLD: sentences/en/_common.yaml
lists:
  color:
    values:
      - "red"
      - "green"
      - "blue"
  brightness:
    range:
      type: "percentage"
      from: 0
      to: 100
```

They now live in dedicated files under `lists/<lang>/`, grouped however makes
sense for the language (e.g. `lists/en/lights.yaml` for colors and brightness):

```yaml
# NEW: lists/en/lights.yaml
language: "en"
lists:
  color:
    values:
      - in: "red"
        out: "red"
      - in: "green"
        out: "green"
      - in: "blue"
        out: "blue"
```

Two things to note:

- **Shared lists.** Range lists and wildcards can now be shared across all
  languages by placing them at the top level (`lists/<group>.yaml`, no language
  subdirectory). Value lists still can't be shared, since their values must be
  translated per language.

  ```yaml
  # NEW: lists/lights.yaml  (shared across languages)
  lists:
    brightness:
      range:
        type: "percentage"
        from: 0
        to: 100
    search_query:
      wildcard: true
  ```

- The `range` (`from`/`to`/`step`/`type`) and `wildcard: true` forms are
  unchanged; only the file location changes.

## 4. Rules move out of `_common.yaml`

Expansion rules used to share the `_common.yaml` file under `expansion_rules:`:

```yaml
# OLD: sentences/en/_common.yaml
expansion_rules:
  the: "(the|my|our)"
  light: "(light|lights|lighting|lamp|lamps)"
  name: "[<the>] {name}"
```

They now live under `rules/<lang>/`, grouped into files such as `verbs.yaml`,
`light.yaml`, or `common.yaml`:

```yaml
# NEW: rules/en/common.yaml
language: "en"
expansion_rules:
  the: "(the|my|our)"

# NEW: rules/en/light.yaml
language: "en"
expansion_rules:
  light: "(light|lights|lighting|lamp|lamps)"
```

While migrating, apply these **recommended** restrictions (they make templates
readable and keep the matched slots predictable):

- **Rules should not contain lists.** A rule should not reference `{list_name}`.
  In particular, drop the common `<name>` rule (`"[<the>] {name}"`) and write the
  list directly in the template, e.g. `[<the>] {name}`. Otherwise it's impossible
  to tell which slots a template matches just by reading it, and you get
  duplicated optionals like `[the] [the] {name}`.
- **Rules should not reference other rules.** A rule should not contain
  `<other_rule>`. Nesting forces readers to chase a chain of definitions and can
  make the set of possible sentences explode.

## 5. New template restrictions

The template syntax is otherwise unchanged, but **list references are no longer
allowed inside alternatives or optionals**:

```text
(text|{list_name})   ❌ no longer allowed
[{list_name}]        ❌ no longer allowed
```

This guarantees that a sentence template always matches the same set of slots. If
you have a sentence where a list is optional, split it into two templates (one
with the list, one without) so each has a well-defined slot signature.

## 6. Tests

Tests follow the same per‑slot‑combination reorganization as sentences. Old tests
lived at `tests/<lang>/<domain>_<intent>.yaml`; new tests live at
`tests/<lang>/<intent>/<slot_combination>.yaml` and are **self-contained** —
each file declares all of its own fixtures (entities, areas, floors, timers):

```yaml
# NEW: tests/en/HassTurnOn/name_only.yaml
language: "en"

entities:
  - name: "Overhead Light"
    domain: "light"

areas:
  - name: "Kitchen"

tests:
  - sentences:
      - "turn on the overhead light"
    slots:
      name: "Overhead Light"
    response: "Turned on the light" # rendered response text, not the key
```

> Note the two meanings of `response:` — in a **sentence** file it's the response
> **key** (e.g. `default`); in a **test** file it's the expected rendered **text**
> (e.g. `Turned on the light`). See §8.

## 7. Tooling

### Step 0 — copy lists/rules out of `_common.yaml` (once per language)

```bash
python3 -m script.intentfest migrate_common --language <lang>
```

This **copies** the `expansion_rules:` and `lists:` blocks from
`sentences/<lang>/_common.yaml` into `rules/<lang>/` and `lists/<lang>/`, grouped
to mirror `rules/en/` / `lists/en/`. It is a **copy, not a move** — `_common.yaml`
is left untouched so the not-yet-migrated old-format files keep resolving their
rules/lists. (You only delete the `_common.yaml` blocks at the very end; see the
checklist's cleanup step.) The helper:

- skips range/wildcard lists that already exist as shared top-level `lists/*.yaml`
  (they're language-independent — reuse the shared one);
- skips and **flags** items the new format rejects: fully-optional rules (e.g.
  `<in>` = `[in|op|van|bij]`, which must be inlined) and value lists whose values
  contain `<rule>`/`{list}` references (which must be inlined first);
- flags list-bearing rules (`<name>`) and nested-rule references as §4 cleanups;
- flags **dangling references** — a copied rule that references a rule the tool
  skipped (e.g. a rule using `<in>`, which was dropped as fully-optional). These
  are latent: they resolve in `_common.yaml` but break the moment a new sentence
  reaches them, and `validate` won't catch an unreferenced rule body.

Grouping is purely organizational (the test harness merges every file in
`rules/<lang>/`), so re-group the output by hand if you like. **Once the language
is fully migrated, prune `rules/<lang>/` _and_ `lists/<lang>/` down to what your
combos actually reference** (like `rules/en/`) — `migrate_common` copies
everything, so the inlined slot rules (`name`/`area`/`floor`), unused value lists,
and any composite/dangling rules are left behind as dead weight to delete. Prune
**orphaned response keys** too (see the final-cleanup step). Build the reference
graph carefully: a rule/list is live only if a sentence — or another _live_ rule —
references it (a rule used only by another dead rule is itself dead).

### Per intent — scaffold the sentences and tests

Most of the mechanical work — bucketing sentences by slot combination, rewriting
`requires_context`/`slots` into `name_domains`/`inferred_domain`, and splitting
and reshaping tests — can be scaffolded automatically. Migrate **one intent at a
time** with:

```bash
python3 -m script.intentfest migrate_language --language <lang> --intent <Intent>
```

The tool reuses the same slot-resolution logic as `check_slot_combinations`
(parsing each template and resolving its rules/lists to a slot signature) to:

- write `sentences/<lang>/<Intent>/<slot_combination>.yaml` for every sentence it
  can map **unambiguously** to a single combo, with the right
  `name_domains`/`inferred_domain` filled in;
- split and reshape the old tests into
  `tests/<lang>/<Intent>/<slot_combination>.yaml`, pulling the fixtures each file
  needs out of `tests/<lang>/_fixtures.yaml` and converting them to the new shape
  (entity/area/floor fixtures by name; `timers:`/`media:` are carried verbatim for
  `*Timer*`/`*Media*` intents — trim them to what each file needs);
- write a **flag report** to `migration_reports/<lang>/<Intent>.md` listing
  everything it could _not_ safely do.

The tool is deliberately conservative: it never edits or deletes the old
`*_<Intent>.yaml` files and never touches `_common.yaml`, so a run is always safe
to inspect and redo (use `--force` to overwrite scaffold files). It does **not**
finish the job — a human or AI agent then resolves every item in the flag report,
deletes the old files, and runs `validate` + the tests. The report categories map
directly onto the gotchas below.

> `migration_reports/` holds throwaway scaffolding output — it's gitignored, so
> don't commit it (a blanket `git add -A` will otherwise sweep the reports in).

This per-intent split is intended to be done by a focused agent with limited
context: feed it this guide, run the tool for its one intent, and have it clear
the flag report.

## 8. Lessons from practice (gotchas)

These are the things the scaffolder **flags for you** because they need judgement:

- **A slot signature does not uniquely identify a combo.** Several combos can
  share the same slots — e.g. `name_only`, `name_scene`, and `name_script` are all
  just `{name}`. They are told apart by their **domain** (`media_player` vs `scene`
  vs `script`), so you must carry the old `requires_context.domain` / `slots.domain`
  through to pick the right file.

- **Old templates pack several combos into one line.** Compact templates such as
  `open (<name>;[<in>] (<area>|<floor>))` match `name_area` _and_ `name_floor`
  (and the `(area|floor)` alternative alone yields two signatures). The new format
  requires each file to match exactly one signature, so these must be **split into
  one template per combo**. This is the largest manual chunk — in NL's `HassTurnOn`,
  ~40% of templates needed splitting.

- **`domain`/`device_class` come from `slots:`/`requires_context:`, not the words.**
  A `requires_context: { domain: X }` on a `{name}` template becomes
  `name_domains: [X]`; a `slots: { domain: X }` (inferred from the words, e.g.
  "turn on the lights") becomes `inferred_domain: X` (singular).

- **The slot-combination test harness reads only `skip_words:` from `_common.yaml`.**
  New-format sentences resolve expansion rules **only** from `rules/<lang>/` and
  lists only from `lists/` and `lists/<lang>/` (see `tests/test_slot_combinations.py`);
  the lone block still pulled from `_common.yaml` is `skip_words:` (see the
  skip_words note below). A
  migrated template that references a `<rule>` or `{list}` which isn't there yet
  compiles fine for `validate` but fails the tests with
  `ValueError: RuleReference(...)`. So, **before** an intent's templates can be
  tested, every rule/list they reference must already live in `rules/<lang>/` /
  `lists/<lang>/`, or be inlined. Two ways to satisfy this:
  - **Preferred — move the rules/lists first.** Move the `<rule>`s and `{list}`s
    the intent needs out of `_common.yaml` into `rules/<lang>/<group>.yaml` /
    `lists/<lang>/<group>.yaml` and keep the `<rule>` references in the templates.
    This keeps templates readable.
  - **Fallback — inline.** Inline the rule bodies into the templates. This always
    works but bloats templates badly (e.g. a long `<media_item>` alternation
    repeated on every line), so reserve it for small, one-off rules.
    You must always inline **list-bearing** rules regardless (`<name>` →
    `[<the>] {name}`), per §4. The scaffolder flags every rule/list reference that
    isn't resolvable from `rules/<lang>/` / `lists/<lang>/` as `unresolved rule` /
    `unresolved list`.

- **Every sentence template must be exercised by a test.** The slot-combination
  harness fails if a template in a combo file is never matched by any test
  sentence. After you split or inline templates you often need to **add test
  sentences** so each template is hit (the scaffolder can't know this — it only
  carries over the old tests).

- **`skip_words` ARE applied by the slot-combination harness.** Unlike rules and
  lists, `skip_words` from `_common.yaml` _are_ loaded and applied when matching
  test sentences (the harness reads them into the compiled `Intents` — see
  `tests/test_slot_combinations.py`). So a test sentence that leans on a skip word
  (e.g. German "_kannst du_ ..." / "_bitte_ ...") still matches, and you do **not**
  need to strip skip words from carried-over tests. (This changed when `skip_words`
  loading was added to the harness; migrations that pre-date it may contain
  unnecessary rewrites.)

- **EMPTY combos are only a problem if required.** The scaffolder lists each
  declared combo as scaffolded or EMPTY. An EMPTY combo that is **non-required**
  (importance `usable`/`complete`/`optional`, and no `required` domains) is safe
  to leave unscaffolded — the old language may simply not cover it. Only EMPTY
  **required** combos must be filled (those are also flagged as "missing required
  coverage").

- **Test fixtures change shape.** New-format test entities use `domain:` (taken
  from the old fixture `id` prefix, e.g. `media_player.tv` → `media_player`) and
  drop `id:`; areas and floors keep only `name:` (plus an optional floor **name**).
  The scaffolder converts these, but flags any entity whose `id` has no domain.

- **`response:` means two different things.** In a **sentence** file `response:` is
  the response **key** (e.g. `default`). In a **test** file `response:` is the
  expected rendered **text** (e.g. `Gepauzeerd`). Old sentence groups with no
  `response:` default to the `default` key.

- **`context.area` can collapse `area_only` into `default`.** Old area tests often
  set `context: { area: ... }`, which looks like the `default` (context-area)
  combo. The scaffolder flags any combo that got sentences but no test so you can
  add one.

### Writing the new sentence templates

- **Compact templates pack several combos; split them.** The biggest manual job.
  Old templates use `(area|floor)` alternatives and `(name…;area…)` permutations
  to match many slot combinations in one line. The new format wants one signature
  per file, so each must be split into one template per combo. The scaffolder
  flags these `multi-combo` and does **not** auto-place them.

- **Very dense templates are flagged `complex template`, not analyzed.** Slot
  enumeration is exponential, so the scaffolder bails out on templates with a huge
  number of signatures (rather than hanging). Build those by hand from the
  reference language. For big multi-domain intents (`HassTurnOn`/`HassTurnOff`)
  the scaffolder's auto-placed _sentences_ are unreliable anyway — treat the
  **already-migrated `en` files as authoritative** and use the report mainly for
  its combo list, `unresolved`/`complex` flags, and old-files list.

- **Don't write symmetric duplicate templates.** A permutation `(a;b)` already
  matches both orders, so adding explicit `a b` _and_ `b a` templates creates
  duplicates that can't each be uniquely test-exercised. Prefer the permutation.

- **Mind `recognize_best` collisions.** Phrasings shared across combos (e.g.
  `overal`/`<all>` between `domain_only`, `area_domain`, `domain_all`) can get
  matched to the wrong combo. Restrict an ambiguous phrasing to the single combo
  that should win.

- **Composite rules can't be referenced inside one combo.** Rules like
  `<timer_duration>`/`<my_timer>`/`<name_area>` span multiple combos, so inline
  the specific fragment each combo needs (as `en`'s timer files do) instead of
  referencing the composite rule.

- **Some value lists Step 0 can't copy — add them by hand.** Lists whose values
  contain `<rule>`/`{list}` references (e.g. `cover_classes`) are skipped by
  `migrate_common`, and a few slots that were literal in the old format (e.g.
  `volume_step` direction) need a value list in the new one. Add these to
  `lists/<lang>/` additively, inlining any rule refs, mirroring `en`.

### Writing the new tests

- **Test `response:` must be a plain quoted string, not a `|` block scalar.**
  Rendered responses are compared without a trailing newline, so a block scalar
  (which adds one) will mismatch.

- **Fixture counts couple to the response.** Some responses depend on how many
  fixtures exist (e.g. `HassCancelAllTimers` counts _all_ timer fixtures;
  `HassTimerStatus` switches wording with more than one timer). Trim fixtures to
  exactly what makes the asserted response render.

- **`is_active: true` is not defaulted** on timer fixtures — set it explicitly
  when a test needs an active timer.

- **Wildcard name slots are greedy.** A wildcard `{timer_name:name}` can swallow a
  leading article or out-rank `{area}` (the matcher prefers the `name` slot). Give
  area tests their own `areas:` fixture so `{area}` resolves, keep the wildcard
  terminal in the template, and avoid solid compounds like "keukentimer" that
  don't match `{area}[ ]<timer>` (which needs a space).

- **Slots that abut a prepositional phrase over-absorb (Romance languages).** In
  languages where modifiers attach with a preposition (es/fr/it/pt "puerta **del
  garaje**", "lumière **du salon**"), a wildcard (`{search_query}`) or even
  `{area}`/`{name}` placed next to such a phrase tends to swallow it, capturing the
  wrong slot. Two recurring traps from the es migration: `{search_query} [el|la]
{media_class}` let the wildcard eat "Avatar **la película**" (no clean boundary —
  drop the article-between ordering), and `{area}` named "garaje" stole "**del
  garaje**" from a `{device_class: garage}` match (an inherent ambiguity with no
  dedicated combo). Prefer a required preposition/literal as a boundary, keep
  wildcards terminal, and accept that some "X de[l] <area>" phrasings are genuinely
  ambiguous when an area shares the noun.

### Intent-shape gotchas

- **One intent spans several old domain files.** `HassTurnOn` has eight
  `<domain>_HassTurnOn.yaml` sentence files (plus tests). The report lists every
  one under "Old files to delete when done" — delete them all.

- **A combo may need a response key the language lacks.** Add it additively to
  `responses/<lang>/<Intent>.yaml` (e.g. `cover_device_class`), mirroring `en`.

- **`HassGetState` is fully migrated upstream.** `en` now ships all twelve
  `HassGetState` combos (`name_only`, `name_state`/`_area`/`_floor`, `name_where`,
  `name_zone`, `domain_state`/`_area`/`_floor`,
  `device_class_state`/`_area`/`_floor`) with no old-format `*_HassGetState` files
  — mirror that full set. Note the slot-combination model has **no combo for
  attribute queries** (brightness, volume, "what's playing", color temperature), so
  those old per-domain phrasings are dropped for every language and any responses
  they used (`get_brightness`, etc.) become orphaned — prune them (see final
  cleanup). (Earlier revisions of this guide called `HassGetState` a partial
  migration; that is no longer the case.)

## Migration checklist

**Step 0 — once per language, before any intent.** Copy the shared resources out
of `_common.yaml` so per-intent work can reference them (the test harness only
reads `rules/<lang>/` and `lists/<lang>/`, not `_common.yaml`):

```bash
python3 -m script.intentfest migrate_common --language <lang>
```

This **copies** (does not move) `lists:` into `lists/<lang>/` and
`expansion_rules:` into `rules/<lang>/`; `_common.yaml` stays put for the old
files. Resolve its flags: inline fully-optional rules and any value lists that
reference rules/lists. Doing this first keeps templates readable (clean `<rule>`
references instead of inlined bloat) and lets parallel per-intent agents share a
stable `rules/<lang>/` instead of fighting over it. Run
`python3 -m script.intentfest validate --language <lang>` to confirm it's clean.

**Then, per intent.** Run
`python3 -m script.intentfest migrate_language --language <lang> --intent <Intent>`
and:

1. Look up the intent's `slot_combinations` in `intents.yaml` and skim the
   generated `migration_reports/<lang>/<Intent>.md`.
2. Resolve every flag: **split multi-combo templates** into one template per
   combo, fix **unmapped signatures**, resolve any `unresolved rule`/`unresolved
list` (they should be rare after Step 0), and confirm the `response` keys.
3. Confirm the scaffolded `sentences/<lang>/<Intent>/<combo>.yaml` files: each
   starts at `data:` (no `intents:` nesting), carries the right
   `name_domains:`/`inferred_domain:`, and **all `required` domains are covered**.
4. Inline any remaining list-bearing rules (`<name>` → `[<the>] {name}`) and
   flatten nested rules in the templates you keep.
5. Remove any list references from inside `(...)` alternatives and `[...]`
   optionals — split such templates in two.
6. Finish the tests in `tests/<lang>/<Intent>/<combo>.yaml`: every scaffolded
   combo needs a test, every template must be exercised, fixtures must be
   self-contained, and `response:` holds the expected text.
7. Delete the old `sentences/<lang>/<domain>_<intent>.yaml` and
   `tests/<lang>/<domain>_<intent>.yaml` files.
8. Run `python3 -m script.intentfest validate --language <lang>` and the tests;
   iterate until green.
9. **Format the generated YAML with prettier** before committing — the tools emit
   PyYAML, which isn't prettier-formatted, and CI runs the prettier pre-commit
   hook: `pre-commit run prettier --all-files` (this reformats the new
   `rules/<lang>/`, `lists/<lang>/`, and scaffolded test files; it's formatting
   only and won't change matches).
10. **Commit this intent on its own** — one commit per intent (e.g.
    `Migrate <lang> <Intent> to slot-combination format`), covering just that
    intent's sentence files, test files, and old-file deletions. This keeps the
    history reviewable intent-by-intent and easy to revert in isolation. Don't
    batch several intents into one commit.

**Final cleanup — only once _no_ old-format files remain.** When the language has
no `<domain>_<intent>.yaml` files left, the copies left behind in Step 0 are dead
weight. Delete the blocks that have moved to their new homes:

- Remove the `lists:` and `expansion_rules:` blocks from
  `sentences/<lang>/_common.yaml` (keep `responses:`, `settings:`, `skip_words:`,
  which still live there).
- Remove `tests/<lang>/_fixtures.yaml` (each new test file is self-contained).

  > The old-format harness (`tests/test_language_sentences.py`) generates a
  > `test_<stem>` for every flat test file across **all** languages and runs each
  > against **every** language, so it would otherwise eagerly load this language's
  > `_fixtures.yaml`. The `lang_fixtures` fixture treats a missing `_fixtures.yaml`
  > as empty (those per-file tests skip early for a fully migrated language), so
  > it's safe to delete. (`en` still ships one only because it predates this.)
  >
  > Note: deleting `_fixtures.yaml` also disables the `parse` CLI's name/area/floor
  > resolution for this language (it reads that file). If you still need `parse`
  > during the adversarial review, restore it temporarily and delete it again.

- **Add the language to `LANGUAGES_TO_TEST` in `tests/test_slot_combinations.py`.**
  Until the language is in this set, the suite runs the matching/coverage checks
  for any combo files that exist but does **not** enforce that every `required`
  combo actually has a sentence+test file (`do_test_slot_combination` only asserts
  the file exists for languages in `LANGUAGES_TO_TEST`). Adding it turns on that
  required-coverage gate — do it last and fix any newly-failing required combos.

Then run `validate` + the tests one last time to confirm the language is green
with `_common.yaml` slimmed down.

> **Caveat:** if a language _intentionally_ keeps any old-format
> `<domain>_<intent>.yaml` files, this cleanup does **not** apply to it: those
> files still resolve their rules/lists from `_common.yaml` and their fixtures
> from `_fixtures.yaml`, so both must stay. (As of this writing no upstream intent
> is kept in the old format — `en` is fully migrated, `HassGetState` included.)

## Adversarial review (final step)

A green `validate` and a passing test suite are **necessary but not sufficient**:
they confirm each test sentence matches _some_ template and that response keys
exist, but they do **not** catch dropped user phrasings, over-matching, wrong
domain/response mappings, trivially-passing tests, or dead/dangling rules. So the
last step of a language migration is an adversarial review loop.

The easiest way to run it is the `/goal` command, which keeps a sub-agent loop
going until you're satisfied:

```
/goal Run adversarial review as a sub agent. Process and fix the findings. Repeat. Stop at your discretion.
```

(If `/goal` isn't available in your environment, run the same loop by hand:
spawn a read-only reviewer sub-agent each pass, fix the real findings as
individual commits, and repeat on a fresh angle.)

Each pass should spawn a **read-only** reviewer sub-agent that hunts for defects
the green checks miss, then you fix the real findings (committing each), and
repeat. Make every pass attack a **different angle** — repeating the same angle
converges to nothing. Angles that proved productive:

1. **Dropped phrasings (under-coverage).** Diff the old source against the new
   combo files: user phrasings/verbs that existed before but match nothing now.
   Use the **pre-migration** ref for the old files — `git show main:...` works
   while migrating on a branch, but once the migration is merged the old files are
   gone from `main`, so use the merge-base or the commit before Step 0
   (`git show <pre-migration-sha>:sentences/<lang>/<domain>_<intent>.yaml`).
   **Filter every candidate through `en`/`intents.yaml` before calling it a
   regression:** a phrasing is only a real loss if a slot combination exists to
   hold it (i.e. `en` covers it, or `intents.yaml` declares a fitting combo). If
   there is no combo for it — e.g. all-lights-on-a-floor (no `domain_floor`),
   all-locks-in-an-area, whole-house fans on `HassTurnOn`, or attribute/measurement
   queries on `HassGetState` — it is a by-design model limitation, not a migration
   bug, and "restoring" it has nowhere to go. This filter avoids chasing the many
   acceptable drops the raw old-vs-new diff surfaces.
2. **Over-matching / wrong-slot (false positives).** Templates that now match
   utterances they shouldn't, capture the wrong slot, or whose file's templates
   don't actually match the combo's declared signature. The per-test harness
   asserts `intent.name == expected`, so it **cannot** catch cross-intent
   over-matching (e.g. a `HassTurnOn` template stealing a `HassTurnOff` utterance);
   verify this with a probe that merges _all_ intents into one `Intents` and calls
   `recognize_best`, then checks which intent wins.
3. **Mappings.** Wrong `name_domains`/`inferred_domain` or `response` keys vs the
   old `requires_context`/`slots` and `intents.yaml`; uncovered `required` domains.
4. **Test rigor.** Tests that pass trivially (asserting only a static response),
   slots that don't match what the sentence should extract, or combos whose tests
   don't exercise every template.
5. **Tooling + fidelity.** Bugs in `migrate_common`/`migrate_language`; whether
   `rules/<lang>/`/`lists/<lang>/` faithfully copy `_common.yaml`; dead or
   dangling rules left to prune.
6. **Symmetry + completeness.** Sibling intents (TurnOn vs TurnOff, the media
   group, Increase vs Decrease) that diverge for non-`intents.yaml` reasons;
   `usable`/`complete` combos the old language covered but the migration dropped;
   response-file integrity. Watch asymmetric _structure_: e.g. `HassTurnOn` has no
   `domain_all` combo — its "all (the) lights" quantifier lives in `domain_only` —
   while `HassTurnOff` has a dedicated `domain_all`, so it's easy to drop the "all"
   phrasing from `HassTurnOn` when splitting.

When using the `parse` CLI during review, note it resolves `{name}`/`{area}`/
`{floor}` from `tests/<lang>/_fixtures.yaml`; once final cleanup deletes that file,
parses stop matching names, so temporarily restore it (and delete it again — never
commit it) or drive matching through `pytest tests/test_slot_combinations.py`.

Insist that every finding cite a specific `file:line` or command output, and that
findings be split into **must-fix** correctness/coverage bugs vs nits. Stop when a
pass comes back with no must-fix findings (in practice two or three escalating
passes). Fixes are commits like any other; re-run `validate` + tests after each.
