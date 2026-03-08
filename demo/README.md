# Demo: Factory-Based Backend Swapping

## Overview

This demo showcases how GitHub Copilot (GHCP), connected to an **Azure AI Search MCP server**, can retrieve knowledge from an indexed Microsoft Quantum research paper (_QDK/Chemistry: A Modular Toolkit for Quantum Chemistry Applications_) and use it to implement working code - all in a single prompt.

[main.py](main.py) starts as a skeleton: the abstract interface and entry point are in place, but the backends and factory are missing. The agent fills them in using the factory-registry pattern it retrieves from the indexed QDK docs.

## Demo query

```txt
implement the factory-registry pattern from QDK/Chemistry in demo/main.py add a `BackendFactory` class with a decorator-based register/create API (mirroring `algo.create`), a `MockBackend` that returns a hard-coded energy, and a `PySCFBackend` that runs a real RHF/STO-3G calculation. Wire `run_simulation()` to use the factory so backends can be swapped by name without changing workflow code.
```

## What "success" looks like

```
=== Mock backend ===
[mock] E(H2) = -1.117000 Hartree

=== PySCF backend ===
converged SCF energy = -1.11675930739643
[pyscf] E(H2) = -1.116759 Hartree
```

The key proof point: `run_simulation()` is **backend-agnostic** — only the factory
registry and backend classes were filled in, following the pattern the agent
retrieved from the indexed QDK docs via the MCP search tool.

## Troubleshooting: PySCF on Windows

PySCF does **not** ship pre-built wheels for Windows (neither x64 nor ARM64).
`pip install pyscf` will attempt to compile from source and fail unless you
have MSVC + CMake installed. The easiest workaround is **WSL**.

### WSL setup (one-time)

```powershell
# 1. Install WSL + Ubuntu (requires a reboot after the first run)
wsl --install Ubuntu-22.04
# ↳ Reboot, then re-open your terminal

# 2. Install pip inside WSL
wsl -e bash -c "sudo apt update && sudo apt install -y python3-pip"

# 3. Install PySCF (Linux wheels exist — this just works)
wsl -e bash -c "pip3 install pyscf"
```

### Running the demo through WSL

```powershell
wsl -e bash -c "cd '/mnt/c/ai-for-research/demo' && python3 main.py"
```

WSL mounts your Windows drives at `/mnt/c/`, so no file copying is needed.
