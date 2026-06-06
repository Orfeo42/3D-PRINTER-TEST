# printer3d — learning build123d

Code-CAD for 3D printing. Python + [build123d](https://build123d.readthedocs.io)
(OpenCASCADE B-rep kernel → real fillets/chamfers, STEP + STL export).

## Setup

```bash
uv sync          # install deps into .venv
```

- Python pinned to **3.13** (build123d/OCP have no 3.14 wheels yet).
- Deps: `build123d` (modeling), `ocp_vscode` (live 3D viewer).

## Viewer (ocp_vscode)

Two ways to see models. Both read the `show(...)` call in each script.

**VS Code (best loop):**
1. Install the **OCP CAD Viewer** extension.
2. Command palette → `OCP CAD Viewer: Open`.
3. Run a script → model appears live, updates on every re-run.

**Standalone / external terminal:**
```bash
uv run python -m ocp_vscode      # terminal 1: viewer server on port 3939 (leave it)
export OCP_PORT=3939             # terminal 2: tell scripts where the viewer is
uv run python examples/01_first_box.py
```
ocp_vscode locates the viewer via the `OCP_PORT` env var. VS Code's OCP CAD
Viewer sets it automatically in its integrated terminal; an external shell must
export it.

No viewer / `OCP_PORT` unset → scripts skip the live view cleanly and still
export to `output/` (the `view()` helper guards this).

## Run a lesson

```bash
uv run python examples/01_first_box.py
```

Each script calls `show(...)` (viewer) and `save(...)` (writes
`output/<name>.step` + `output/<name>.stl`).

- **.step** → re-open/edit in CAD (FreeCAD).
- **.stl** → slice and print.

## Lessons (in order)

| # | file | teaches |
|---|------|---------|
| 1 | `01_first_box.py` | builder mode, `Box`, `show`, export |
| 2 | `02_fillet_chamfer.py` | edge selectors, `fillet`, `chamfer` |
| 3 | `03_sketch_extrude_holes.py` | sketch → `extrude` → subtract holes, `Locations` |
| 4 | `04_algebra_mode.py` | the other API: `+ - &` operators, `Pos` |
| 5 | `05_parametric_bracket.py` | parametric real part: L-bracket |

## Two APIs

build123d gives you both — same kernel, pick per taste:

- **Builder mode**: `with BuildPart() as p: Box(...)` — imperative, context-driven.
- **Algebra mode**: `part = Box(...) - Cylinder(...)` — values + operators.

Lessons 1–3 + 5 use builder; lesson 4 shows algebra side-by-side.

## Docs

- API: https://build123d.readthedocs.io
- Cheat sheet: https://build123d.readthedocs.io/en/latest/cheat_sheet.html
- Examples: https://build123d.readthedocs.io/en/latest/examples_1.html
