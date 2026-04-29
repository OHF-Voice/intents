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

## Format: always use legacy

**Always use the legacy format** (`sentences/<lang>/<domain>_<intent>.yaml`) for all non-English languages. The slot-combination format (`sentences/<lang>/<Intent>/<combo>.yaml`) is the new English-leading format and is **not ready** for other languages — do not use it, even if the user asks.

Legacy file structure:
```yaml
language: <lang>
intents:
  <IntentName>:
    data:
      # <slot combination comment>
      - sentences:
          - "<template 1>"
          - "<template 2>"
        requires_context:        # optional
          area:
            slot: true           # copies active area into `area` slot
        response: default        # or a specific response key
```

Cluster sentences by slot combination within the file, one `data:` group per combination, with a short comment. Look at `sentences/fr/cover_HassTurnOn.yaml` for the canonical example of this style.

## Syntax cheatsheet (HassIL)

- **Alternatives**: `(red|green|blue)` — one of. Can apply mid-word: `turn(s|ed|ing)`.
- **Optionals**: `[the]` — present or absent. Mid-word: `light[s]`.
- **Lists**: `{name}` matches a list value and stores it in the slot. The stored value is the `out:` value, not the `in:` value. Use `{list:slot}` if names differ.
- **Expansion rules**: `<rule_name>` — replaced with the rule body. Always prefer these over inlining.
- **Permutations**: `(a;b)` — both must appear, any order.
- **Inline expansion rules**: can be defined inside a `data:` group under `expansion_rules:` for local reuse within that group.

## Expansion rules: always prefer them over inlining

**This is the most important authoring rule.** Before writing any word or phrase into a template, check `sentences/<lang>/_common.yaml` for an existing expansion rule. If one exists, use it — never inline the equivalent text.

Common rules to look for (check your language's `_common.yaml` for the actual expansions):
- Verb groups: `<active>`, `<mets>`, `<eteins>`, `<nettoie>`, `<envoie>`, `<demarre>` — domain-specific verb lists
- Article rules: `<le>`, `<de>` — definite/partitive articles (know their exact content before using them)
- Locative rules: `<dans>`, `<ici>` — prepositions and "here" equivalents
- Domain nouns: `<media>`, `<volume>`, `<minuteur>`, `<serrure>` — object nouns

If a phrase you need does not exist as a rule but appears 3+ times in the file, define it as an inline `expansion_rules:` in the `data:` group (for local reuse) or propose adding it to `_common.yaml`.

**Never** hardcode verb lists when an expansion rule already covers them. **Never** hardcode article+noun combos when a rule already exists.

## Procedure

### 1. Survey context

Read these in order:

- `intents.yaml` → find the target intent. Note: `slot_combinations`, `slots`, `name_domains` / `inferred_domains` and their importance (`required`/`usable`/`complete`/`optional`), the English `example`.
- `sentences/en/<domain>_<intent>.yaml` → reference implementation in English.
- `sentences/<lang>/_common.yaml` → **read this carefully** for all available expansion rules and lists before writing a single template. Know the exact expansion of every rule you plan to use.
- `tests/<lang>/<domain>_<intent>.yaml` → existing tests; new sentences need parallel test entries.
- `tests/<lang>/_fixtures.yaml` → available entity names for `{name}` slot tests. Any `{name}` value used in tests **must** appear here.
- `responses/<lang>/<Intent>.yaml` → response keys to reference via `response: default` or a specific key.

### 2. Draft sentences

Write 2-5 templates per `data:` group. Group sentences that share the same slots and `requires_context`. Aim for:

- **Natural phrasings a native speaker actually uses** — not literal translations of English.
- **Expansion rules first** — check `_common.yaml` before writing any word.
- **Cover all slot combinations** from `intents.yaml`. Use separate `data:` groups for: context-area, explicit area, explicit floor, name-only, name+area.
- **Keep template explosion in check** — every optional doubles permutations; every alternative multiplies.

### 3. `requires_context` rules

- `requires_context: area: slot: true` — fires only when an area is active in context; the active area value is automatically copied into the `area` slot. Use for sentences with no explicit area mention.
- `requires_context: domain: <domain>` — fires only in the context of devices of that domain. Use for `{name}` slots targeting a specific device type (e.g. `media_player`, `fan`, `vacuum`).
- Sentences with an explicit `{area}` or `{floor}` slot in the template do **not** need `requires_context`.

### 4. Pair tests (mandatory)

Tests are not optional. Every `data:` group you add **must** have a matching test block in `tests/<lang>/<domain>_<intent>.yaml`.

Legacy test format:
```yaml
language: <lang>
tests:
  - sentences:
      - "realised sentence 1"
      - "realised sentence 2"
    intent:
      name: <IntentName>
      slots:
        area: "salon"
    response: "Rendered response string"
```

**Critical test rules:**

1. **Context-area tests** — if the sentence group uses `requires_context: area: slot: true`, the test block **must** include both `context:` and the `area` slot:
   ```yaml
   intent:
     name: <IntentName>
     context:
       area: "salon"
     slots:
       area: "salon"
   ```
   Without `context:`, recognition returns `None` and the test fails.

2. **`{name}` slot values** must exist in `tests/<lang>/_fixtures.yaml`. Look up the exact entity name before writing the test sentence.

3. **List slot values** — use the `out:` value from the list definition, not the `in:` value (e.g. `media_class: "music"` not `media_class: "musique"`).

4. **No duplicate sentences** — the same realised sentence cannot appear in two test blocks. The validator detects this.

5. **One test block per slot-value combination** — sentences in the same block must all produce the same slot values. If two sentences produce different values (e.g. different `media_class`), split them into separate blocks.

### 5. Lists in `_common.yaml`

If the intent requires a new list (e.g. `media_class`, `search_query`), add it to `sentences/<lang>/_common.yaml`:

- **Wildcard lists** (free-text slots): `search_query: wildcard: true`
- **Value lists** — each value must be a **separate entry**. Do NOT use regex alternation inside `in:` values:
  ```yaml
  # WRONG
  - in: "(morceau|chanson|piste)"
    out: "track"

  # RIGHT
  - in: "morceau"
    out: "track"
  - in: "chanson"
    out: "track"
  - in: "piste"
    out: "track"
  ```

### 6. Validate before finishing

Always run the full test suite — not just validate:

```bash
script/test
```

This runs both `intentfest validate` and `pytest`. Do not push until `script/test` exits with 0 failures. If `script/test` is unavailable:

```bash
python3 -m script.intentfest validate --language <lang>
pytest tests/test_language_sentences.py -k "<Intent> and <lang>" -q --no-header --tb=short
```

For spot checks while drafting:
```bash
# Confirm a sentence parses to the right intent and slots
python3 -m script.intentfest parse --language <lang> --sentence 'allume la lumière'
```

### 7. Hand back

Report:

1. Files changed (paths).
2. New sentence templates (count) and test sentences (count).
3. `script/test` result (must be 0 failures).
4. Any rules or lists added to `_common.yaml` (and why).
5. Open questions for the language leader (regional spelling, formal vs informal, etc.).

## Anti-patterns to avoid

- Using slot-combination format for non-English languages — always use legacy.
- Inlining words that already exist as expansion rules — check `_common.yaml` first.
- Translating English word-by-word instead of writing what users actually say.
- Putting sentences with different slot expectations in the same `data:` group — split them.
- Pushing without running `script/test` — a passing `validate` alone is not enough.
- Writing a `requires_context: area: slot: true` test without the `context:` block.
- Using an entity name in a test that is not in `_fixtures.yaml`.
- Using regex alternation `(a|b)` inside a list `in:` value — use separate entries.
- Assuming `<le>` includes partitive articles — check the actual rule expansion in `_common.yaml`.
