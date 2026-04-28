---
name: ha-intents-review
description: Review a contributor's pull request or pasted YAML diff for a Home Assistant intents language. Use when reviewing contributions to OHF-Voice/intents, checking sentence templates before merge, validating new test sentences, or auditing a branch for syntax and naturalness issues. Assumes a local clone of OHF-Voice/intents.
---

# Review HA intents contributions

You are reviewing a contribution to one or more sentence/test/response files in [OHF-Voice/intents](https://github.com/OHF-Voice/intents). The audience for your review is the language leader, who will paste it into a PR comment or use it to decide whether to merge.

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
git -C <repo> diff --name-status main...HEAD -- 'sentences/**' 'tests/**' 'responses/**' 'rules/**' 'lists/**'
git -C <repo> diff main...HEAD -- <paths>
```

Group changes by `(language, intent, slot_combination)`. For each group, run the rest of the procedure.

### 2. Static checks (per changed file)

Run the validator first — many issues come back already labeled:

```bash
python3 -m script.intentfest validate --language <lang>
```

Then read the diff yourself and look for:

**Template syntax (HassIL)**
- Unbalanced `(` `)`, `[` `]`, `<` `>`, `{` `}`.
- A list inside an alternative: `(foo|{name})` — forbidden in slot-combination files.
- A list inside an optional: `[{name}]` — forbidden in slot-combination files.
- A rule that contains `{list}` or `<other_rule>` — discouraged (see `docs/slot_[combinations.md](http://combinations.md)`).
- `{list:slot}` where `slot` is not declared in `intents.yaml` for this intent.
- Template explosion: any template producing >10k permutations. Run:
  ```bash
  python3 -m script.intentfest count_sentences --language <lang>
  ```

**Slot-combination consistency**
- Sentences with `{name}` must declare `name_domains:` covering at least the `required` set in `intents.yaml`.
- Sentences with `{domain}` must declare `inferred_domain:` (single, not plural).
- The combination's slots in the file must exactly match `slot_combinations.<combo>.slots` in `intents.yaml`.

**Test parity**
- Every new sentence template needs at least one realised test sentence in `tests/<lang>/...` that exercises it.
- Test fixtures (`entities`, `areas`, `floors`) referenced by `slots:` must be defined in the same file (new format) or in `_fixtures.yaml` (legacy).
- `response:` in tests must match what the sentence file declares (or the rendered string).

**Responses**
- If a sentence references a `response:` key, that key must exist in `responses/<lang>/<Intent>.yaml`.

### 3. Naturalness pass (the part the validator can't do)

For each new template, ask out loud:
- Would a native speaker really say this, or is it a literal translation of the English source?
- Are formal/informal forms handled? Regional variants?
- Are determiners (the/a/my) and conjugation correct across all expansions? Sample a few:
  ```bash
  python3 -m script.intentfest sample_template '<template>' --rule ... --values ...
  ```
- Does `parse` recover the right slots?
  ```bash
  python3 -m script.intentfest parse --language <lang> --sentence '<a realised sentence>'
  ```

Call out specific lines (file + line number) when something reads off — don't generalise.

### 4. Run the tests

```bash
pytest tests --language <lang> -k <Intent> -n auto
```

If the contribution touches multiple intents, run per-intent so failures are easier to attribute.

### 5. Write the review

Format the output as a PR-ready review with three sections:

```markdown
## Summary
<2-3 sentence overview: what changed, what's the risk level (low / medium / high)>

## Blocking issues
- `<file>:<line>` — <issue>. Suggested fix: `<replacement>`.

## Suggestions (non-blocking)
- `<file>:<line>` — <suggestion>.

## Verification
- Validator: <pass/fail + summary>
- Tests: <pass/fail + N tests>
- Permutation counts: <any concerning numbers>
```

Keep blocking vs non-blocking strict: blocking = validator failure, test failure, syntax that violates slot-combination rules, or templates that match wrong intents. Everything else is a suggestion.

## Common issues to watch for

- **Copy-paste from English** that left English determiners (`the`, `a`) in the target language.
- **Missing `name_domains`** when a `{name}` slot was added.
- **A new rule that duplicates an existing rule** in `rules/<lang>/`.
- **Tests that pass but only cover one expansion** of a template with many.
- **Response references that don't exist** because someone added a sentence with `response: "lights_floor"` but didn't add that key.
- **Whitespace/encoding** issues in non-Latin scripts (zero-width spaces, Arabic shaping).

## Output

End with a clear verdict: `Approve` / `Approve with suggestions` / `Request changes`, plus the markdown review block ready to paste.
