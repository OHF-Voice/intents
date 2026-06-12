# Migration Guide: Old Template Syntax → Slot Combinations

This guide explains how to migrate sentences written in the original
[HassIL template format](templates.md) (as documented in
[`hassil`](../../hassil/docs/template_syntax.md)) to the new
**slot combination** format described in [`slot_combinations.md`](slot_combinations.md).

The *template syntax itself* (alternatives `(a|b)`, optionals `[x]`, lists
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
- [Migration checklist](#migration-checklist)


## At a glance

| Concern            | Old format                                              | New format                                                            |
| ------------------ | ------------------------------------------------------- | --------------------------------------------------------------------- |
| Sentence files     | `sentences/<lang>/<domain>_<intent>.yaml`               | `sentences/<lang>/<intent>/<slot_combination>.yaml`                   |
| File root          | `intents: <Intent>: data:`                              | `data:` (intent & slot combination come from the path)               |
| Grouping           | By intent (and ad‑hoc by domain in the filename)        | By **slot combination**, declared in `intents.yaml`                  |
| Target domain      | `requires_context: { domain: ... }` / `slots: { domain }` | `name_domains:` / `inferred_domain:` in each sentence group        |
| Lists              | `sentences/<lang>/_common.yaml` → `lists:`              | `lists/<lang>/<group>.yaml` (or shared `lists/<group>.yaml`)         |
| Rules              | `sentences/<lang>/_common.yaml` → `expansion_rules:`    | `rules/<lang>/<group>.yaml`                                          |
| Tests              | `tests/<lang>/<domain>_<intent>.yaml`                   | `tests/<lang>/<intent>/<slot_combination>.yaml` (self‑contained)     |


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
    example: "turn on the overhead light"  # use names from tests
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
    response: "default"
```


## Migration checklist

For each old `sentences/<lang>/<domain>_<intent>.yaml`:

1. Look up the intent's `slot_combinations` in `intents.yaml`.
2. Sort the old sentence groups by which slots they match, and move each into the
   matching `sentences/<lang>/<intent>/<slot_combination>.yaml` file.
3. Drop the `intents:`/`<Intent>:` nesting — start the file at `data:`.
4. Replace every `requires_context: { domain: ... }` (and domain-only `slots:`)
   with `name_domains:` or `inferred_domain:`, matching the domains declared in
   `intents.yaml`. Ensure all `required` domains are covered.
5. Move `lists:` out of `_common.yaml` into `lists/<lang>/<group>.yaml` (or shared
   `lists/<group>.yaml` for ranges/wildcards).
6. Move `expansion_rules:` out of `_common.yaml` into `rules/<lang>/<group>.yaml`;
   inline any list-bearing rules and flatten nested rules.
7. Remove any list references from inside `(...)` alternatives and `[...]`
   optionals — split such templates in two.
8. Move and split the corresponding tests into
   `tests/<lang>/<intent>/<slot_combination>.yaml`, adding the fixtures each file
   needs.
