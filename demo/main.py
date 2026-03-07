"""Molecular simulation runner with swappable chemistry backends."""

from abc import ABC, abstractmethod


class ChemistryBackend(ABC):
    """Base interface that every chemistry backend must implement."""

    @abstractmethod
    def compute_energy(self, molecule: dict) -> float:
        """Return the ground-state energy (in Hartree) for *molecule*."""
        ...


# --- Backends and factory go here ---


def run_simulation(backend_name: str) -> None:
    """Run an H2 energy simulation using the named backend."""

    molecule = {
        "atoms": [("H", (0.0, 0.0, 0.0)), ("H", (0.0, 0.0, 0.74))],
        "basis": "sto-3g",
        "charge": 0,
        "multiplicity": 1,
    }

    raise NotImplementedError


if __name__ == "__main__":
    print("=== Mock backend ===")
    run_simulation("mock")

    print("\n=== PySCF backend ===")
    run_simulation("pyscf")
