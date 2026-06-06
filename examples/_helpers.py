"""Shared export helper for the lessons.

build123d exports two formats you care about for 3D printing:
- STEP: exact B-rep CAD geometry. Use to re-open/edit in CAD (FreeCAD, etc.).
- STL : triangle mesh. Use to slice and print.
"""

from pathlib import Path

from build123d import Compound, export_step, export_stl

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"


def save(part: Compound | None, name: str) -> None:
    """Write both <name>.step and <name>.stl into output/.

    `part` is Optional because BuildPart().part is None until something is
    built; guard so callers can pass `p.part` directly.
    """
    if part is None:
        raise ValueError(f"cannot save '{name}': part is None (nothing built)")
    OUTPUT_DIR.mkdir(exist_ok=True)
    step_path = OUTPUT_DIR / f"{name}.step"
    stl_path = OUTPUT_DIR / f"{name}.stl"
    export_step(part, str(step_path))
    export_stl(part, str(stl_path))
    print(f"saved {step_path.name} + {stl_path.name}")
