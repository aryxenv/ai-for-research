"""
Demo: Molecular Simulation with Swappable Backends
===================================================

Goal: Simulate the energy of a simple molecule (H2) using a factory-based
interface so we can swap algorithm backends (e.g. PySCF, mock) without
rewriting the main workflow.

TASK FOR THE AGENT:
    Using knowledge from the QDK/Chemistry toolkit's factory-based design,
    implement the TODO sections below so that:

    1. `BackendFactory` returns the correct backend based on a string name.
    2. `run_simulation` works unchanged regardless of which backend is used.
    3. Adding a new backend requires ZERO changes to `run_simulation`.

Query to search: "How does the QDK/Chemistry toolkit use a factory-based
interface to let me swap out algorithm backends, like switching to PySCF,
without rewriting my main Python workflow?"
"""

from abc import ABC, abstractmethod


# ---------------------------------------------------------------------------
# 1. Abstract backend interface
# ---------------------------------------------------------------------------
class ChemistryBackend(ABC):
    """Base interface that every backend must implement."""

    @abstractmethod
    def compute_energy(self, molecule: dict) -> float:
        """Return the ground-state energy (in Hartree) for *molecule*."""
        ...


# ---------------------------------------------------------------------------
# 2. Concrete backends — TODO: implement these
# ---------------------------------------------------------------------------

# TODO: Implement a MockBackend that returns a hard-coded energy value
#       (useful for testing without real chemistry libraries).


# TODO: Implement a PySCFBackend that performs a real (or realistic stub)
#       energy calculation using the PySCF pattern from QDK Chemistry docs.


# ---------------------------------------------------------------------------
# 3. Backend factory — TODO: implement this
# ---------------------------------------------------------------------------

# TODO: Implement a BackendFactory that maps backend names (strings) to
#       backend classes, and provides a `create(name)` class method.
#       Follow the factory-based pattern from the QDK/Chemistry toolkit.


# ---------------------------------------------------------------------------
# 4. Main workflow — this must NOT change when backends are swapped
# ---------------------------------------------------------------------------
def run_simulation(backend_name: str) -> None:
    """Run an H2 energy simulation using the named backend."""

    molecule = {
        "atoms": [("H", (0.0, 0.0, 0.0)), ("H", (0.0, 0.0, 0.74))],
        "basis": "sto-3g",
        "charge": 0,
        "multiplicity": 1,
    }

    # TODO: Use BackendFactory to get a backend instance from `backend_name`,
    #       call compute_energy, and print the result.
    raise NotImplementedError("Complete this using the factory pattern.")


# ---------------------------------------------------------------------------
# 5. Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=== Mock backend ===")
    run_simulation("mock")

    print("\n=== PySCF backend ===")
    run_simulation("pyscf")
