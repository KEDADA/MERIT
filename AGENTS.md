<!-- ARIS-CODEX:BEGIN -->
## ARIS Codex Skill Scope
ARIS Codex packages installed in this project: skills-codex
Managed entries: 6
Manifest: `.aris/installed-skills-codex.txt`
ARIS repo root: `/mnt/qjh000/zys/src/MERIT/third_party/ARIS`
Project skill path: `.agents/skills/<skill-name>`
For ARIS Codex workflows, prefer the project-local skills under `.agents/skills/`.
When a skill needs ARIS helper scripts, resolve the repo root from the manifest or set it explicitly:
`ARIS_REPO=$(awk -F'\t' '$1=="repo_root"{print $2; exit}' "/mnt/qjh000/zys/src/MERIT/.aris/installed-skills-codex.txt")`
Do not edit or delete symlinked skills in place; update upstream or rerun:
`bash /mnt/qjh000/zys/src/MERIT/third_party/ARIS/tools/install_aris_codex.sh "/mnt/qjh000/zys/src/MERIT" --reconcile`
For copied Codex installs, use:
`bash /mnt/qjh000/zys/src/MERIT/third_party/ARIS/tools/smart_update_codex.sh --project "/mnt/qjh000/zys/src/MERIT"`
<!-- ARIS-CODEX:END -->
