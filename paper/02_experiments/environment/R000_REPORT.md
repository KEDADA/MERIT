# R000 Environment Inventory Report

**Status:** Inventory completed; execution stopped before sanity checks or experiments.

## Repository and ARIS

- Repository HEAD was verified exactly as `4280484e035191b66f77618b7729dbd465d8b828`.
- All seven required vendored ARIS files are present. `third_party/ARIS` was not updated or replaced.
- Codex dry-run: 5 selected skills plus one support link; 6 creates, 0 conflicts.
- Claude dry-run: dependency-expanded selection of 18 skills plus one support link; 19 creates, 0 conflicts.
- Project-level installation succeeded for both Codex and Claude after using the installers' documented non-interactive mode. Active manifests and links point into the current Linux project snapshot; no link is broken or targets Windows.
- `.aris/tools` was regenerated as a project-local link.
- The installer could not create an optional user-global ARIS pointer because the user-level location was read-only. Project-level installation remains intact.
- The inactive `.aris/installed-skills.txt.prev` backup retains the prior Windows manifest paths. It is not an active manifest or link and was not forcibly deleted.

## CLI configuration

- Codex CLI: `0.144.6`; authentication check succeeded.
- Claude Code: unavailable (`claude` command not found).
- Required Claude base URL and API credential were not present in this session. No credential value was read or printed.
- Codex MCP for Claude: not configured because Claude Code is unavailable. `claude mcp add` was not run.
- User action required in a private terminal: install/provide Claude Code, configure `ANTHROPIC_BASE_URL=https://api.aipaibox.com` and the user's own private Anthropic credential, then add/list the `codex` MCP server and restart Claude Code. Do not place credentials in this repository or in chat.

## Hardware and software result

- GPU: 8 × NVIDIA H20, 97,871 MiB (95.58 GiB) each.
- Driver / CUDA: NVIDIA 580.126.20; driver-reported CUDA 13.0.
- GPU topology: every GPU pair reports `NV18`; 18 NVLinks per GPU. MIG is disabled on all GPUs.
- Capture state: all GPUs at 0 MiB used and 0% utilization; no compute process reported.
- PyTorch environment: Python 3.12.13, PyTorch 2.11.0+cu130, CUDA available, 8 devices, cuDNN 9.19.0, NCCL 2.28.9.
- CPU: 2 sockets, 90 physical cores, 180 logical CPUs, Intel Xeon Platinum 8457C.
- Memory: 1.9 TiB total, 1.8 TiB available at capture, no swap.
- Project disk: NFSv4, 14 TiB total, 2.2 TiB available, 85% used.
- OS: Ubuntu 22.04.1 LTS, Linux 5.15.0-91-generic, x86_64.
- Tool gaps: `nvcc` and Slurm are absent; Docker client exists but daemon access is denied; mamba/micromamba are absent.

## Readiness verdict

**NO-GO for sanity checks at this point.** The 8-GPU hardware and existing PyTorch environment pass basic visibility checks, but the workflow minimum is incomplete:

1. Claude Code, its private configuration, and Codex MCP are unavailable.
2. The verified repository revision contains no MERIT experiment implementation or executable R001/R002 sanity entry point.
3. No project-pinned MERIT experiment environment or dependency manifest exists; the inspected isolated environment has not been designated as the project runtime.

Docker daemon access is a likely later blocker for WebArena-style replayability. Missing `nvcc` and Slurm are recorded capability gaps but are not independently declared fatal for all sanity work. NFS utilization, sandbox GPU visibility, and the inactive Windows-path manifest backup should be monitored.

## Files created

- `paper/02_experiments/environment/SYSTEM_PROFILE.md`
- `paper/02_experiments/environment/SYSTEM_PROFILE.json`
- `paper/02_experiments/environment/R000_REPORT.md`

## Boundary confirmation

- No training, benchmark, all-reduce test, paper experiment, model download, or data download was run.
- No software was installed, upgraded, or removed.
- No paper source, protocol, placeholder ledger, review file, or `EXPERIMENT_TRACKER.md` was modified.
- No placeholder was backfilled.
- No Git commit or push was performed.
- Work stopped after R000 and awaits user confirmation.

