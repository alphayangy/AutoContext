# Review Checklist

Detailed reference for AutoContext Step 7: self-review before writing context files.

## Review Checklist

Check the generated `AGENTS.md` / `CLAUDE.md` / `.claude/rules/*.md` item by item:

| # | Check Item | Pass Criteria | If Not Passed |
|---|------------|---------------|---------------|
| 1 | **Atom source traceable** | Every entry in `Working Rules` / `Verification` / `Safety` ends with `[atom-name]` | Delete unsourced entries or add atom annotations |
| 2 | **Script actually invoked** | `Working Rules` / `Verification` / `Safety` in the proposal are real output from `tools/render-atoms.py`, with no `[rendered content]` / `<!-- to be rendered -->` / ellipsis placeholders | Invoke the script and paste the full output into the proposal |
| 3 | **No atom rewriting** | `diff` script output against atom source; identical except for indentation and bullet markers | Revert to atom source; if atom source is unsuitable, omit that atom |
| 4 | **Expansion fully preserved** | Every rule has core sentence + indented expansion; no one-line slogans | Restore atom expansion; re-invoke the script to re-render |
| 5 | **No process leakage** | No "first X, then Y, finally Z" multi-step processes; no numbered steps 1/2/3 | Move to a one-line `Reference Docs` pointer, or suggest making it a skill |
| 6 | **No project facts mixed into Working Rules** | Working Rules do not contain specific commands, directory paths, filenames, or tool parameters | Move project facts to `Project Overview` / `Commands` / `Reference Docs` |
| 7 | **No excessive omissions** | Atoms with `priority: high` and `profiles: [all]` are not omitted; omission reason is not "global already covers" or "looks overlapping" | Add back atoms that should not have been omitted |
| 8 | **Length compliant** | Each file ≤ 200 lines | Split into `.claude/rules/`, or trim low-priority atoms |
| 9 | **No placeholders** | No `[TBD]`, `[to be filled]`, empty brackets, or other unfilled content | Delete or complete; mark `[UNVERIFIED]` with explanation if impossible to complete |
| 10 | **No conflicting rules** | No contradictory instructions (e.g. "always do X" vs. "never do X") | Keep the more relevant/higher-priority one and delete the other |
| 11 | **Agent artifact match** | Generated files match `detected_agents` (Claude → CLAUDE.md, multi-agent → AGENTS.md primary) | Re-select artifacts per artifact guide |
| 12 | **Project facts accurate** | Stack, directories, and commands in `Project Overview` / `Commands` match scanned files | Go back to Step 1 and re-detect |
| 13 | **No large README copy-paste** | No whole paragraphs copied from `README.md` into the context file | Replace with a one-line summary or pointer |
| 14 | **No lint/format rules in prose** | No ESLint/Prettier/black formatting rules written as long natural-language paragraphs | Delete; rely on the project's existing linter |
| 15 | **Context file reference direction correct** | If both `CLAUDE.md` and `AGENTS.md` exist: `CLAUDE.md` references `AGENTS.md`, `AGENTS.md` does not reference `CLAUDE.md`; verified by `tools/verify-context.py` | Fix reference direction, then run the script to verify |

## Spot Check

Spot-check the atom output rendered by the script:

1. Randomly sample 3 rendered atoms.
2. Use `diff` (or re-invoke `tools/render-atoms.py` for that atom alone) to compare script output with atom source.
3. Core sentence + expansion must be identical, except for the following allowed items:
   - Leading indentation spaces
   - Bullet markers `-` / `*`
   - Trailing whitespace
4. Any non-allowed difference -> judged as **atom rewriting**, Review fails.

## Review Must Not Be All ✅

**Any proposal can find at least one improvement.** If all 15 Review items are ✅, the Review was too lenient. You must find at least one:

- An atom that could be deleted (M7: deleting it would not cause a mistake)
- A phrasing that could be closer to the atom source
- An expansion that could be restored or compressed more accurately
- A project fact that could be changed to a shorter pointer
- A section that could be split into `.claude/rules/`

Write at least one improvement into the Review output.

## Review Output Format

Append the self-review results after the proposal:

```md
---

## Auto Context Review

| Check Item | Status | Note |
|------------|--------|------|
| Atom source traceable | ✅ | 8/8 entries annotated with `[atom-name]` |
| No process leakage | ⚠️ | `Pipeline discipline` contains a 4-step process, needs removal |
| Length compliant | ✅ | AGENTS.md ~48 lines, CLAUDE.md ~12 lines |
| No conflicting rules | ✅ | No conflicts found |

### Issues to Fix

1. **Process leakage**: The `## Working Standards` `Pipeline discipline` is a 4-step operation process, not an atom. Change to:
   ```md
   ## Reference Docs (read when relevant)
   - `user_memory_inference/README.md` — production inference run process
   ```

2. **Missing atom source**: The `Prompt Engineering` subsection has no `[atom-name]` and its content comes from README. Delete or change to a Reference Docs pointer.

### Corrected File Preview

[Put the corrected AGENTS.md / CLAUDE.md preview here]
```

## Handling Review Failure

- **Atom rewriting found**: Must revert to atom source. If the atom source is genuinely unsuitable for this project, omit that atom instead of rewriting it.
- **1-2 minor issues found** (process leakage, project fact in wrong place, individual atom wrongly selected): Fix directly without re-asking the user.
- **Structural issues found** (wrong artifact selection, large process leakage, wrong profile, excessive omissions): Fix and regenerate the proposal, then re-Review.
- **Review table all ✅**: Send back for re-review; must find at least one improvement.
- **Uncertain whether it counts as leakage/rewriting**: Handle conservatively — "Is this sentence from the atom file?" If not, delete or change it.
