# Demo: Factory-Based Backend Swapping

## Agent expectations

The agent should pull internal research knowledge through an MCP server connection to a custom Azure AI Search instance.

[main.py](main.py) has a skeleton for a molecular-simulation workflow.
The abstract interface and entry point are in place, but the backends
and factory are missing.

## Demo query

> How does the QDK/Chemistry toolkit use a factory-based interface to let me
> swap out algorithm backends, like switching to PySCF, without rewriting my
> main Python workflow? Implement in #demo/main.py

## What "success" looks like

```
=== Mock backend ===
Backend : mock
Energy  : -1.0 Hartree

=== PySCF backend ===
Backend : pyscf
Energy  : -1.117 Hartree
```

The key proof point: `run_simulation()` is **unchanged** — only the factory
registry and backend classes were filled in, following the pattern the agent
retrieved from the indexed QDK docs.
