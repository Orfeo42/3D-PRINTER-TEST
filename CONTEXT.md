# Context: build123d learning project

Handoff for a fresh Claude session (or a future me) to continue helping learn this tool.

## Project

- Dir: `/home/orfeo42/sviluppo/personal/3d-printer` (git, remote github `Orfeo42/3D-PRINTER-TEST`)
- Goal: learn build123d (code-CAD) for 3D printing.
- Stack: uv, Python 3.13 (build123d/OCP have NO 3.14 wheels). Deps: build123d 0.10.0, ocp_vscode 3.4.0. Dev: mypy.

## Layout

- `examples/01_first_box.py` … `05_parametric_bracket.py` — progressive lessons, heavily commented for teaching.
- `examples/_helpers.py` → `save(part, name)`: exports `output/<name>.step` + `.stl`.
- `output/` (gitignored stl/step, `.gitkeep` tracked).
- `stubs/ocp_vscode/*.pyi` → mypy stubs (ocp_vscode ships no `py.typed`; build123d HAS `py.typed`).
- `pyrightconfig.json` (venvPath `.venv`) + `.vscode/settings.json` (interpreter=`.venv`, mypy `fromEnvironment`).

## How it runs / viewer

- Run a lesson via VS Code ▶ "Run Python File". Viewer = "OCP CAD Viewer" ext (`bernhard-42.ocp-cad-viewer`).
- **CRITICAL GOTCHA:** the ext autostarts the viewer ONLY when the RUN FILE contains the literal `from ocp_vscode import` (setting `OcpCadViewer.advanced.autostartTriggers`). So every lesson MUST have `from ocp_vscode import show` + call `show(obj)` directly — do NOT hide `show()` inside a helper, or autostart won't fire → viewer never starts → ws connect gets `port=None` → `ValueError` crash.
- Viewer port registers in `~/.ocpvscode` (default 3939). External-terminal alt: `uv run python -m ocp_vscode` then run the script.

## Lesson pattern

```python
from build123d import Box, BuildPart
from ocp_vscode import show          # required: triggers viewer autostart
from _helpers import save
with BuildPart() as p:
    Box(40, 20, 10)
show(p)                              # live preview
save(p.part, "01_first_box")        # STEP + STL to output/
```

## Key API facts

- Two APIs, same kernel: builder mode (`with BuildPart() as p: Box(...)`, `p.part`) and algebra mode (`Box(...) - Cylinder(...)`, `Pos(x,y,z)*solid`).
- Builder `p.part` type = `Part | None` (None before build). Algebra `-` returns `Compound`. `save()` typed `Compound | None` with None guard; `Part` ⊂ `Compound`.
- `export_step` / `export_stl` take a `Shape`; both used in `save()`.
- Selectors: `p.edges()/faces().filter_by(Axis.Z)`, `.sort_by(Axis.Z)[-1]`, `.group_by(Axis.Z)[i]`. `fillet(edges, radius=)`, `chamfer(edges, length=)`. Sketch → `extrude(amount=±, mode=Mode.SUBTRACT)`, `Locations((x,y), ...)`.

## Learning path

01 box+show+export → 02 fillet/chamfer+selectors → 03 sketch/extrude/holes → 04 algebra mode → 05 parametric L-bracket.
Docs: https://build123d.readthedocs.io (+ `/en/latest/cheat_sheet.html`).

## Working conventions

- User runs caveman mode ultra by default (terse replies). Python: uv, type hints, no `Any` (use `object`/unions), `pathlib`, no comments in normal code — but lesson files keep teaching comments on purpose.
- Verify edits with `uvx pyright examples/` and `uv run mypy examples/` (both must be clean).
