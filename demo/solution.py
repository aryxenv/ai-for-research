"""Molecular simulation runner with swappable chemistry backends.

Uses the factory-registry pattern from QDK/Chemistry (algo.create)
so backends can be swapped by name without changing workflow code.
"""

from abc import ABC, abstractmethod
from typing import Type


class ChemistryBackend(ABC):
    """Base interface that every chemistry backend must implement."""

    @abstractmethod
    def compute_energy(self, molecule: dict) -> float:
        """Return the ground-state energy (in Hartree) for *molecule*."""
        ...


class BackendFactory:
    """Factory registry mirroring QDK/Chemistry's ``algo.create`` pattern.

    Register backends with the ``@BackendFactory.register("name")`` decorator,
    then instantiate them via ``BackendFactory.create("name")``.
    """

    _registry: dict[str, Type[ChemistryBackend]] = {}

    @classmethod
    def register(cls, name: str):
        """Decorator that registers a backend class under *name*."""
        def decorator(backend_cls: Type[ChemistryBackend]):
            if name in cls._registry:
                raise ValueError(f"Backend '{name}' is already registered")
            if not issubclass(backend_cls, ChemistryBackend):
                raise TypeError(
                    f"{backend_cls.__name__} must subclass ChemistryBackend"
                )
            cls._registry[name] = backend_cls
            return backend_cls
        return decorator

    @classmethod
    def create(cls, name: str, **kwargs) -> ChemistryBackend:
        """Instantiate and return the backend registered as *name*."""
        if name not in cls._registry:
            available = ", ".join(sorted(cls._registry)) or "(none)"
            raise KeyError(
                f"Unknown backend '{name}'. Available: {available}"
            )
        return cls._registry[name](**kwargs)

    @classmethod
    def available(cls) -> list[str]:
        """Return sorted list of registered backend names."""
        return sorted(cls._registry)


# ---------------------------------------------------------------------------
# Concrete backends
# ---------------------------------------------------------------------------

@BackendFactory.register("mock")
class MockBackend(ChemistryBackend):
    """Returns a hard-coded H2/STO-3G RHF energy for testing."""

    def compute_energy(self, molecule: dict) -> float:
        return -1.1175


@BackendFactory.register("pyscf")
class PySCFBackend(ChemistryBackend):
    """Runs a real RHF/STO-3G calculation via PySCF."""

    def compute_energy(self, molecule: dict) -> float:
        from pyscf import gto, scf

        mol = gto.Mole()
        mol.atom = [
            (sym, coord) for sym, coord in molecule["atoms"]
        ]
        mol.basis = molecule.get("basis", "sto-3g")
        mol.charge = molecule.get("charge", 0)
        mol.spin = molecule.get("multiplicity", 1) - 1
        mol.verbose = 0
        mol.build()

        mf = scf.RHF(mol)
        energy = mf.kernel()
        return float(energy)


# ---------------------------------------------------------------------------
# Workflow
# ---------------------------------------------------------------------------

def run_simulation(backend_name: str) -> None:
    """Run an H2 energy simulation using the named backend."""

    molecule = {
        "atoms": [("H", (0.0, 0.0, 0.0)), ("H", (0.0, 0.0, 0.74))],
        "basis": "sto-3g",
        "charge": 0,
        "multiplicity": 1,
    }

    backend = BackendFactory.create(backend_name)
    energy = backend.compute_energy(molecule)
    print(f"Backend : {backend_name}")
    print(f"Energy  : {energy:.6f} Hartree")


if __name__ == "__main__":
    print("=== Mock backend ===")
    run_simulation("mock")

    print("\n=== PySCF backend ===")
    run_simulation("pyscf")
