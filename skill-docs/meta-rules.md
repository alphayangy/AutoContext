# AutoContext Meta-Rules

These rules govern how AutoContext executes. They are not rendered into user project files.

1. **Generate less, not more**: Don't invent undetected project facts; don't recall unnecessary atoms.
2. **Review before writing**: Generate a proposal and write directly after Review by default; do not write when Review fails.
3. **Do not overwrite existing files**: Existing context files go through review/patch mode.
4. **CLAUDE.md < 200 lines**: When exceeded, split into `.claude/rules/` instead of making the file longer.
5. **Profile is a recall dimension, not an artifact**: Do not write the Profile name into the final `CLAUDE.md`.
6. **Processes don't go into CLAUDE.md**: Multi-step processes should be suggested as `.claude/skills/`, not stuffed into project context files.
7. **Same rule in one place only**: Do not duplicate it in both `CLAUDE.md` and `AGENTS.md`.
8. **Detect Agent before selecting artifact**: Decide output files based on `detected_agents`, do not default to `CLAUDE.md` for every project.
9. **Multi-agent uses AGENTS.md as single source**: Native files for each tool only import / reference `AGENTS.md`, without copying content.
10. **Project facts and atoms must be separated**: Project facts only go into `Project Overview` / `Commands` / `Reference Docs`; atoms only go into `Working Rules` / `Verification` / `Safety`.
11. **Global CLAUDE.md does not exempt project atoms**: When a global `~/.claude/CLAUDE.md` is detected, do not omit universal atoms for this project because of it. Global is user preference; project is project constraint; they are not mutually exclusive.
12. **Self-review before writing**: After every proposal generation, run the Step 6.5 Review checklist. If it fails, fix and then write; do not write problematic files directly to disk.
13. **Atom rewriting is forbidden**: `Working Rules` / `Verification` / `Safety` must be rendered by `tools/render-atoms.py`; LLM hand-rewriting, compressing, or rephrasing is not allowed.
14. **High-priority atoms kept by default**: Atoms with `priority: high` and `profiles: [all]` are not casually omitted. Omission must provide evidence of "what specific error would occur if not kept."
15. **Review must spot-check**: Randomly sample 3 rendered atoms and `diff` the script output against atom source. Core sentence + expansion must be identical (except indentation and bullet markers).
16. **Review must not be all ✅**: Any proposal has at least one improvement. All ✅ means the Review was too lenient and needs re-review.
17. **Rules must include expansion**: `Working Rules` / `Verification` / `Safety` cannot be one-line slogans. Every entry must contain the atom core sentence + indented expansion so the agent knows exactly what to do.
18. **Executable scripts take priority over data files**: When classifying profile, if the project has both `*.py` / `*.sh` / `Makefile` / `Snakefile` / `inference*` / `batch_*` / `run.sh` and `.sql` / `.parquet` / `.csv`, prioritize `coding`; data-related atoms are only auxiliary recalls.
19. **Scan efficiently**: During project detection, use `tree -L 2` once to get the structure, then pick key files and read the first 30 lines. Do not `ls` directories one by one, do not read whole files, and do not use the shell to explore the skill's own file structure.
20. **Rules sections must be rendered by script**: After selecting atoms, invoke `tools/render-atoms.py` to generate `Working Rules` / `Verification` / `Safety`, without hand-assembling.
21. **Placeholders must not replace script output**: `Working Rules` / `Verification` / `Safety` in the proposal must be the script's real output; placeholders like `[rendered content]`, `<!-- to be rendered -->`, ellipses, or shorthand are not allowed.
