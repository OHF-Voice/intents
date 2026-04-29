---
name: ha-intents-review
description: Review a contributor's pull request or pasted YAML diff for a Home Assistant intents language. Use when reviewing contributions to OHF-Voice/intents, checking sentence templates before merge, validating new test sentences, or auditing a branch for syntax and naturalness issues. Assumes a local clone of OHF-Voice/intents.
---

# Review HA intents contributions

You are reviewing a contribution to one or more sentence/test/response files in [OHF-Voice/intents](https://github.com/OHF-Voice/intents). The audience is the language leader, who will paste your review into a PR comment or use it to decide whether to merge.

## Inputs to confirm

1. **Repo path** — absolute path to the cloned `intents` repo. The branch should already be checked out, OR the user gives a base ref to diff against (default `main`).
2. **Scope** — one of:
   - A branch / PR (compare `HEAD` against `main`).
   - A specific commit range or file list.
   - A pasted YAML snippet (no repo diff; review syntax only).
3. **Language** — inferred from changed paths or asked.

If anything is ambiguous, AskUserQuestion before reviewing.

## Procedure

### 1. Enumerate the diff

```bash
git diff --name-status main...HEAD -- 'sentences/**' 'tests/**' 'responses/**' 'rules/**' 'lists/**'
git diff main...HEAD -- <paths>
```

Group changes by `(language, intent, slot_combination)`. For each group, run the rest of the procedure.

### 2. Run the full test suite first

```bash
script/test
```

This runs both `intentfest validate` and `pytest` in one shot. Report any failures before doing anything else — a failing test suite is an automatic blocking issue. If `script/test` is unavailable:

```bash
python3 -m script.intentfest validate --language <lang>
pytest tests/test_language_sentences.py -k "<lang>" -q --no-header --tb=short
```

### 3. Static checks (per changed file)

**Format check**
- Non-English languages must use the **legacy format** (`sentences/<lang>/<domain>_<intent>.yaml`). The slot-combination format (`sentences/<lang>/<Intent>/<combo>.yaml`) is English-only and not ready for other languages. Flag any non-English slot-combination file as a **blocking issue**.

**Template syntax (HassIL)**
- Unbalanced `(` `)`, `[` `]`, `<` `>`, `{` `}`.
- A list inside an alternative: `(foo|{name})` — forbidden in slot-combination files.
- A list inside an optional: `[{name}]` — forbidden in slot-combination files.
- `{list:slot}` where `slot` is not declared in `intents.yaml` for this intent.
- Template explosion: any template producing >10k permutations.

**Expansion rule usage**
- Every word or phrase that already exists as an expansion rule in `sentences/<lang>/_common.yaml` must use the rule reference (`<rule>`) — not the inlined text. Flag any hardcoded verb lists, article groups, or locative phrases that duplicate an existing rule. This is the most common authoring oversight.
- Check that the rule reference matches what the author intended: `<le>` does not include partitive articles ("de la", "du", "des"); `<dans>` typically includes "des". Know what the rule expands to before approving.
- If a phrase repeats 3+ times in the file without a rule, suggest extracting it to `_common.yaml`.

**`requires_context` correctness**
- `requires_context: area: slot: true` — for sentences without an explicit area mention. The active area is injected into the `area` slot.
- `requires_context: domain: <domain>` — for `{name}` slot sentences targeting a specific device type.
- Sentences with an explicit `{area}` or `{floor}` slot do **not** need `requires_context`.

**Slot-combination clustering (legacy format)**
- Each `data:` group should be commented with the slot combination it covers.
- All sentences within one group must produce the same set of slots. Sentences producing different slots must be in separate groups.

**Test parity**
- Every new sentence template needs at least one realised test sentence in `tests/<lang>/<domain>_<intent>.yaml`.
- `requires_context: area: slot: true` groups **must** have both `context: area: "X"` AND `slots: area: "X"` in the test block. Missing `context:` causes silent recognition failure.
- `{name}` slot values used in tests must exist in `tests/<lang>/_fixtures.yaml`.
- List slot values (e.g. `media_class`) must use the `out:` value, not the `in:` value (e.g. `music` not `musique`).
- No duplicate realised sentences across test blocks — the validator rejects these.
- Sentences producing different slot values must be in separate test blocks.

**Lists in `_common.yaml`**
- New wildcard slots (e.g. `search_query`) must be declared as `wildcard: true` in `_common.yaml`. A missing wildcard list causes `MissingListError` and breaks all tests for the language.
- List `in:` values must be individual strings — regex alternation `(a|b|c)` inside an `in:` field is invalid and silently breaks `_common.yaml` loading, causing unrelated tests to fail.

**Responses**
- `response:` keys referenced in sentence files must exist in `responses/<lang>/<Intent>.yaml`.

### 4. Naturalness pass (the part the validator can't do)

For each new template, ask:
- Would a native speaker really say this, or is it a literal translation of the English source?
- Are formal/informal forms handled? Regional variants?
- Do determiners and conjugation work across all expansions?
  ```bash
  python3 -m script.intentfest parse --language <lang> --sentence '<a realised sentence>'
  ```

Call out specific lines (file + line number) when something reads off.

### 5. Write the review

```markdown
## Summary
<2-3 sentence overview: what changed, risk level (low / medium / high)>

## Blocking issues
- `<file>:<line>` — <issue>. Suggested fix: `<replacement>`.

## Suggestions (non-blocking)
- `<file>:<line>` — <suggestion>.

## Verification
- `script/test`: <pass / fail + summary>
- Validator: <pass / fail>
- Tests: <N passed / N failed>
```

Blocking = `script/test` failure, syntax violation, missing `context:` on a context-area test, wrong list value format (`in:` regex alternation), slot-combination format on a non-English language, or templates matching the wrong intent. Everything else is a suggestion.

## Common issues to watch for

- **Inlined words that should be expansion rules** — always cross-check `_common.yaml`.
- **Missing `context:` block** on tests for `requires_context: area: slot: true` groups — silent failure, hard to spot.
- **List `in:` values using regex alternation** `(a|b)` — breaks the entire `_common.yaml`, causing unrelated tests to fail across all intents.
- **Missing wildcard list** for free-text slots (e.g. `search_query`) — causes `MissingListError` across all tests for the language.
- **Wrong slot value in tests** — using the `in:` value instead of the `out:` value (e.g. `musique` instead of `music`).
- **Entity name in test not in `_fixtures.yaml`** — `{name}` slot silently returns `None`.
- **Copy-paste from English** leaving English determiners in the target language.
- **Sentences with different slot values in the same test block** — must be split.
- **Slot-combination format on a non-English language** — blocking; use legacy format.
- **Response references that don't exist** in `responses/<lang>/<Intent>.yaml`.

## Output

End with a clear verdict: `Approve` / `Approve with suggestions` / `Request changes`, plus the markdown review block ready to paste.
