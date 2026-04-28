---
name: ha-intents-coverage
description: Analyze intent and slot-combination coverage for a Home Assistant language vs the canonical reference, and produce a prioritized gap report. Use when planning a sprint of contributions, onboarding a new contributor, comparing a language against English, hunting for missing required intents, or building a roadmap for a language's progress. Assumes a local clone of OHF-Voice/intents.
---

# HA intents coverage & gap analysis

You are producing a coverage report for one language in [OHF-Voice/intents](https://github.com/OHF-Voice/intents). The output is a roadmap the language leader can use to plan work — what's missing, what's required vs optional, and where to start.

## Inputs to confirm

1. **Repo path** — absolute path to the cloned `intents` repo.
2. **Target language** — e.g. `pt-BR`. Must exist in `languages.yaml`.
3. **Reference language** — defaults to `en` (the canonical leader). The user can pick another for comparative purposes.
4. **Output format** — markdown report (default), CSV, or interactive widget. Ask if not specified.

## Procedure

### 1. Build the canonical inventory

Parse `intents.yaml` to enumerate every (intent, slot_combination) pair plus its importance metadata. For each combo capture:

- `importance` (when no name/domain split): `required` / `usable` / `complete` / `optional`.
- `name_domains` by importance level (when `{name}` slot present).
- `inferred_domains` by importance level (when `{domain}` slot present).
- The English `example` sentence — useful as a seed.

Filter to `supported: true` intents only. This is the universe the language could cover.

### 2. Inspect target language sentence coverage

Detect format:

- **Slot-combination format**: `sentences/<lang>/<Intent>/<combo>.yaml` files exist.
- **Legacy format**: `sentences/<lang>/<domain>_<intent>.yaml` files only.

For the new format, a combo is "covered" iff its file exists, parses, and includes templates whose `name_domains` / `inferred_domain` cover all `required` entries in `intents.yaml`.

For legacy format, infer coverage by reading the file and matching `slots:` / `inferred_domain` / `requires_context.domain` in `data:` groups against the slot combinations defined in `intents.yaml`. This is approximate — flag intents where you cannot map cleanly.

### 3. Compute the gap

Categorise every combo as one of:

- **Missing — required**: must exist; the language fails validation without it.
- **Missing — usable**: expected by users; the leader should add it next.
- **Missing — complete**: needed for a 100% score.
- **Missing — optional**: nice to have.
- **Partial**: file exists but doesn't cover all `required` domains in `name_domains` / `inferred_domains`. List which domains are missing.
- **Covered**: present and complete.

Pull the language's score and counts from the project's own tooling for cross-checks:

```bash
python3 -m script.intentfest count_sentences --language <lang> --summary
python3 -m script.intentfest count_sentences --language <ref> --summary
python3 -m script.intentfest validate --language <lang> 2>&1 | tail -50
```

### 4. Identify quick wins

Flag combos where the language is close to coverage:

- **Partial** combos missing only 1-2 domains.
- **Missing — required** combos with very simple English templates (`HassNevermind`, `HassGetCurrentTime`).
- Intents with a finished response file but no sentence file — content is half-built.
- Intents the LLM template tool can bootstrap:
  ```bash
  python3 -m script.intentfest llm_template <lang> <Intent>
  ```

### 5. Produce the report

Default markdown structure:

```markdown
# Coverage report: <lang> vs <ref>

_Generated <date> against intents repo at commit <short-sha>._

## Headline
- **Score**: <X%> covered (<covered>/<total> combos)
- **Required gaps**: <N> combos blocking 100% required coverage
- **Format**: <legacy | slot-combination | mixed>

## Required gaps (do these first)
| Intent | Combo | English example | Notes |
| --- | --- | --- | --- |
| HassTurnOn | name_only | turn on the overhead light | covers `light` `switch`, missing `cover` |

## Usable gaps
…

## Partial coverage
…

## Quick wins
- `HassNevermind / default` — single short sentence in `en`, easy port.
- `HassGetCurrentTime / default` — formulaic, LLM template recommended.

## Suggested next sprint
1. <Intent / combo> — <why>
2. …

## Appendix: full combo matrix
<table or collapsed details>
```

For an interactive view, build an artifact (`mcp__cowork__create_artifact`) with a filterable table — useful when the leader will return to this weekly.

### 6. Save outputs

Write the markdown report to `<repo>/../<lang>-coverage-<YYYY-MM-DD>.md` (or wherever the user prefers — ask). Surface a `computer://` link in chat so they can open it.

## Tips

- Don't double-count the same combo appearing under multiple `data:` groups in legacy files.
- A combo with `context_area: true` only counts as covered if the templates use a `<here>` rule or equivalent — note when you can't tell.
- `name_domains.required` is the bar for "covers `required`". `complete` and `optional` lift the score but aren't strictly needed.
- Cross-reference `languages.yaml` for the language's leader handles — useful if the report is being passed back to them.
- If the target language is on legacy format, suggest migration to slot-combination format as a separate, larger effort — don't bury that recommendation.

## Output

Return: the path to the report, headline numbers in chat, and the top 3 recommended next actions.
