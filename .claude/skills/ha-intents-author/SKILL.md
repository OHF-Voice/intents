---
name: ha-intents-author
description: Author new sentence templates for a Home Assistant intent in a specific language. Use when adding sentences to a language file, expanding coverage of an intent, starting a new slot combination, or translating an intent into a new language. Assumes a local clone of OHF-Voice/intents.
---

# Author HA intent sentences

You are helping a language leader write **sentence templates** for one intent in one language in the [OHF-Voice/intents](https://github.com/OHF-Voice/intents) repo. Your job is to produce natural, idiomatic templates plus matching tests, and verify them against the repo's tooling.

## Inputs to confirm

Before writing anything, confirm with the user (use AskUserQuestion if any are missing):

1. **Repo path** — absolute path to the cloned `intents` repo. If unknown, ask. Default to the workspace folder if a folder named `intents/` is present.
2. **Language code** — e.g. `fr`, `de`, `pt-BR`. Cross-check against `languages.yaml`.
3. **Intent + slot combination** — e.g. `HassTurnOn / name_only`, or just `HassClimateSetTemperature`. If only an intent is given, list its slot combinations from `intents.yaml` and ask which one(s).
4. **Format mode** — auto-detect:
   - If `sentences/<lang>/<Intent>/` exists → **slot-combination format** (new, English-leading).
   - Else → **legacy format** (`sentences/<lang>/<domain>_<intent>.yaml`).
   The user can override.

## Syntax cheatsheet (HassIL)

Templates use the [HassIL](https://github.com/home-assistant/hassil) syntax:

- **Alternatives**: `(red|green|blue)` — one of. Can apply mid-word: `turn(s|ed|ing)`.
- **Optionals**: `[the]` — present or absent. Mid-word: `light[s]`.
- **Lists**: `{name}` matches a list value and stores it in the slot of the same name. Use `{list:slot}` if names differ.
- **Expansion rules**: `<rule_name>` — replaced with the rule body. Defined in `rules/<lang>/*.yaml` (new) or `_common.yaml` (legacy).
- **Permutations**: `(a;b)` — both must appear, any order.

**Slot-combination format restrictions** (enforced by validator for English, recommended elsewhere):
- A list reference cannot appear inside an alternative: `(text|{list})` is forbidden.
- A list reference cannot be optional: `[{list}]` is forbidden.
- Rules should not contain `{lists}` or other `<rules>`.

## Procedure

### 1. Survey context

Read these in order — quote the exact paths back to the user as you go:

- `intents.yaml` → find the target intent. Note: `slot_combinations`, `slots`, `name_domains` / `inferred_domains` and their importance (`required`/`usable`/`complete`/`optional`), the English `example`. The example is your seed.
- `sentences/en/<Intent>/<combo>.yaml` (or `sentences/en/<domain>_<intent>.yaml`) → reference implementation.
- `sentences/<lang>/_common.yaml` (legacy) and `rules/<lang>/*.yaml` + `lists/<lang>/*.yaml` (new) → existing rules and lists you should reuse instead of inlining.
- `tests/<lang>/...` for the same intent → existing tests; new sentences need parallel test entries.
- `responses/<lang>/<Intent>.yaml` → response keys you can reference via `response: "..."` in the sentence file.

### 2. Draft sentences

Write 3-10 templates per `data:` group. Group sentences that share the same `slots`, `name_domains` / `inferred_domain`, and `response`. Aim for:

- **Natural phrasings a native speaker actually uses** — not literal translations of English. Ask the user for regional variants if unsure.
- **Reuse rules**: prefer `<turn>` over re-listing `(turn|switch)`. If a phrase repeats 3+ times across the file, propose a new rule in `rules/<lang>/`.
- **Cover the `required` domains/combinations** in `intents.yaml`. Split into multiple `data:` groups when domains diverge (e.g. lights vs covers).
- **Keep template explosion in check** — every optional doubles permutations; every alternative multiplies. Flag any single template producing >10k permutations.

For each new template, mentally sample it and confirm it reads naturally in 2-3 expansions.

### 3. Pair tests

For every `data:` group you add, add a matching `tests:` block in `tests/<lang>/...`. The shape differs by format — match whatever the existing file uses:

**Slot-combination format** (`tests/<lang>/<Intent>/<combo>.yaml`) — intent is implied by the path:
```yaml
language: "<lang>"
entities:
  - { name: "Overhead Light", domain: "light" }
tests:
  - sentences: ["turn on Overhead Light"]
    slots: { name: "Overhead Light" }
    response: "Turned on the light"
```

**Legacy format** (`tests/<lang>/<domain>_<intent>.yaml`) — intent is named explicitly, fixtures live in `_fixtures.yaml`:
```yaml
language: "<lang>"
tests:
  - sentences: ["turn on the kitchen light"]
    intent:
      name: HassTurnOn
      slots: { area: "Kitchen", domain: "light" }
    response: "Turned on the lights"
```

Either way, every new template needs at least one realised test sentence. Provide enough variety to catch under-specification (sentences that match too much) and missed permutations.

Provide enough variety to catch under-specification (sentences that match too much) and missed permutations.

### 4. Validate before finishing

Run from the repo root and report any failures verbatim:

```bash
python3 -m script.intentfest validate --language <lang>
python3 -m script.intentfest count_sentences --language <lang> --summary
pytest tests --language <lang> -k <Intent>
```

For ad-hoc spot checks while drafting:

```bash
# Expand a single template to see real sentences
python3 -m script.intentfest sample_template '<your template>' \
  --rule turn '(turn|switch)' --values name "kitchen light"

# Confirm a sentence parses to the right intent and slots
python3 -m script.intentfest parse --language <lang> --sentence 'allume la lumière'
```

### 5. Hand back

Report:

1. Files changed (paths).
2. New sentences (count) and test sentences (count).
3. Validator output and pytest result.
4. Any rules or lists you added (and why).
5. Open questions for the language leader (e.g. regional spelling, formal vs informal forms).

## Anti-patterns to avoid

- Translating English word-by-word instead of writing what users actually say.
- Stuffing one `data:` group with sentences that have different slot expectations — split them.
- Adding a sentence without a corresponding test (validator passes, real users break it).
- Inlining a phrase that already exists as a rule (`<turn>`, `<the>`, `<here>`).
- Putting `{name}` inside `[ ]` or `( | )` in slot-combination files — validator will reject it.
- Wide-open templates like `[anything] {name} [please]` that explode into millions of permutations.

## Output

When you are done, present a short summary in chat plus a link to the changed files via `computer://` paths.
