# Demo: Factory-Based Backend Swapping

Demonstrates that an AI agent can **pull knowledge through MCP** (Azure AI Search over QDK/Chemistry docs) and **apply it correctly in code**.

## The scenario

[main.py](main.py) contains a skeleton for a molecular-simulation workflow
with `TODO` placeholders. The agent's job is to:

1. Search the knowledge base via the MCP `hybrid_search` tool.
2. Learn how the QDK/Chemistry toolkit uses a **factory-based interface** to
   swap algorithm backends (Mock ↔ PySCF) without touching the main workflow.
3. Fill in the TODOs so `main.py` runs end-to-end.

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
