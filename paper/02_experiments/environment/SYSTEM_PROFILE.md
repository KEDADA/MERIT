# MERIT R000 System Profile

- Collected: 2026-07-19T05:37:34Z (UTC)
- Scope: read-only environment inventory only
- Repository revision: `4280484e035191b66f77618b7729dbd465d8b828`
- Redaction: hostname, username, IP addresses, GPU UUIDs, credentials, SSH data, and absolute private paths are omitted.

## Executive summary

| Area | Observed state |
|---|---|
| GPUs | 8 × NVIDIA H20; 97,871 MiB (95.58 GiB) reported per GPU |
| Driver / driver CUDA | NVIDIA 580.126.20 / CUDA 13.0 |
| GPU state | MIG disabled on all GPUs; 0 MiB used and 0% utilization on all GPUs at capture; no compute process reported |
| Interconnect | Every GPU pair reported as `NV18`; 18 NVLink links per GPU, each statically reported at 26.562 GB/s |
| CPU | 2 × Intel Xeon Platinum 8457C sockets; 90 physical cores; 180 logical CPUs; 2 NUMA nodes |
| Memory | 1.9 TiB total; 1.8 TiB available at capture; no swap |
| Project filesystem | NFSv4; 14 TiB total, 12 TiB used, 2.2 TiB available, 85% utilized |
| OS | Ubuntu 22.04.1 LTS; Linux 5.15.0-91-generic; x86_64 |
| Usable PyTorch environment | Python 3.12.13; PyTorch 2.11.0+cu130; CUDA available; 8 devices |
| CUDA libraries | PyTorch CUDA 13.0; cuDNN 9.19.0; NCCL 2.28.9 |
| Tooling | conda 26.3.2 available after private activation; Docker CLI 27.0.3 present; nvcc, mamba/micromamba, and Slurm CLI absent |

## GPU inventory

All eight enumerated devices reported the same properties:

- Model: NVIDIA H20
- Total memory: 97,871 MiB (approximately 95.58 GiB)
- Free memory at capture: 97,622 MiB
- Used memory at capture: 0 MiB
- GPU utilization at capture: 0%
- MIG mode: Disabled
- Driver: 580.126.20
- Temperature range at capture: 29–34 °C
- Performance state at capture: P0
- Compute processes: none reported by `nvidia-smi --query-compute-apps`

### Topology and interconnect

- `nvidia-smi topo -m` reported `NV18` between every pair of GPUs.
- GPUs 0–3 are associated with NUMA node 0 and logical CPUs 0–89.
- GPUs 4–7 are associated with NUMA node 1 and logical CPUs 90–179.
- Five Mellanox-class NIC functions were visible in the topology table; identifiers and network addressing are omitted.
- `nvidia-smi nvlink --status` reported 18 links per GPU and 26.562 GB/s for each link.

These are static driver/topology reports. No NVLink bandwidth benchmark, all-reduce test, or communication workload was run.

## Host resources

### CPU

| Field | Value |
|---|---:|
| Model | Intel Xeon Platinum 8457C |
| Sockets | 2 |
| Cores per socket | 45 |
| Physical cores | 90 |
| Threads per core | 2 |
| Logical CPUs | 180 |
| NUMA nodes | 2 |

### Memory

| Field | Value at capture |
|---|---:|
| Total | 1.9 TiB |
| Used | 71 GiB |
| Free | 882 GiB |
| Buffer/cache | 975 GiB |
| Available | 1.8 TiB |
| Swap | 0 B |

### Project filesystem

| Field | Value at capture |
|---|---:|
| Type | NFSv4 |
| Total | 14 TiB |
| Used | 12 TiB |
| Available | 2.2 TiB |
| Utilization | 85% |

The project location is intentionally represented as `<PROJECT_ROOT>`.

## Operating system

- Distribution: Ubuntu 22.04.1 LTS (Jammy Jellyfish)
- Kernel: Linux 5.15.0-91-generic
- Architecture: x86_64

## Python and accelerator software

### System Python

- `python3`: 3.10.12
- `pip3`: 22.0.2
- `python` alias: unavailable
- PyTorch import: unavailable (`ModuleNotFoundError`)

### Existing isolated environment

An existing private isolated environment was inspected without modifying it. Its absolute path is omitted.

- Python: 3.12.13
- pip: 26.1.2
- PyTorch: 2.11.0+cu130
- `torch.cuda.is_available()`: `true` outside the Codex device sandbox
- `torch.cuda.device_count()`: `8` outside the Codex device sandbox
- `torch.version.cuda`: 13.0
- cuDNN available: `true`; version 9.19.0
- NCCL available: `true`; version 2.28.9

Inside the default Codex filesystem/device sandbox, the same interpreter could not initialize NVML and reported CUDA unavailable with zero devices. The required sandbox-external read-only recheck succeeded. Future GPU commands must account for this execution boundary.

### Package/environment managers

- conda: 26.3.2 after loading the existing private activation hook
- mamba: unavailable
- micromamba: unavailable
- Project `.venv`: absent
- MERIT experiment dependency manifest: absent at this revision; only vendored ARIS MCP-server requirement files were found

## Other runtime tools

| Tool | Status |
|---|---|
| nvcc | Not available on PATH |
| Docker client | 27.0.3 installed |
| Docker daemon | Not accessible to this session; socket permission denied |
| Slurm (`srun`, `sbatch`, `sinfo`) | Not available on PATH |

Driver-reported CUDA 13.0 and the PyTorch CUDA runtime do not establish that a local CUDA toolkit compiler is installed; `nvcc` is absent.

## Readiness and risks

Hardware and the existing PyTorch environment satisfy the basic GPU visibility requirement. The project is not yet cleared for sanity checks because:

1. Claude Code is unavailable and its private API/base-URL configuration is absent, so Codex MCP could not be configured.
2. This repository revision contains planning/paper materials but no MERIT experiment implementation or executable R001/R002 sanity entry point.
3. There is no project-pinned Python environment or MERIT experiment dependency manifest; the existing isolated environment is not yet declared as the approved project runtime.

Additional non-blocking or benchmark-specific risks are Docker daemon permission, absent `nvcc`, absent Slurm, NFS utilization at 85%, Codex sandbox GPU isolation, and zero swap.

## Instrumentation changelog

No profiling instrumentation, training code, benchmark code, or experiment code was created or modified.

| File | Change type | Purpose |
|---|---|---|
| `paper/02_experiments/environment/SYSTEM_PROFILE.md` | created | Human-readable read-only system inventory |
| `paper/02_experiments/environment/SYSTEM_PROFILE.json` | created | Machine-readable read-only system inventory |
| `paper/02_experiments/environment/R000_REPORT.md` | created | R000 completion and readiness report |

