# Vendored ARIS version

This project includes a clean source snapshot of ARIS under `third_party/ARIS/`.

- Upstream repository: https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep.git
- Upstream commit: `c5f3d5bfc694a812012729841e9697223e4f2130`
- Snapshot date: 2026-07-19
- Local source used for vendoring: `E:\Project\ARIS`
- Excluded from the snapshot: the upstream `.git/` directory and machine-local runtime state

The bundled ARIS code remains subject to its upstream license, included at
`third_party/ARIS/LICENSE`.

Claude and Codex integrations are deliberately not preconfigured. On every new
machine, rerun the appropriate installers from `third_party/ARIS/tools/` and
configure each CLI's authentication outside Git-tracked files.
