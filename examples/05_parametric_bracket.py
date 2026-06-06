"""Lesson 5 - a real, parametric, printable part: an L-bracket.

Pulls it together: parameters at top, sketch+extrude, an angled second wall,
fillets for strength, and counterbored-style mounting holes.

Change the constants and re-run - everything updates. That's code-CAD's payoff.

Run: uv run python examples/05_parametric_bracket.py
"""

from build123d import (
    Axis,
    BuildPart,
    BuildSketch,
    Circle,
    Locations,
    Mode,
    Plane,
    Rectangle,
    extrude,
    fillet,
)

from ocp_vscode import show

from _helpers import save

# --- parameters (edit these) ---
LENGTH = 60.0
WIDTH = 40.0
THICKNESS = 4.0
WALL_HEIGHT = 35.0
HOLE_D = 5.0
FILLET_R = 3.0

with BuildPart() as bracket:
    # flat base
    with BuildSketch() as base:
        Rectangle(LENGTH, WIDTH)
    extrude(amount=THICKNESS)

    # base mounting holes
    top = bracket.faces().sort_by(Axis.Z)[-1]
    with BuildSketch(top):
        with Locations((-LENGTH / 2 + 10, 0), (LENGTH / 2 - 10, 0)):
            Circle(HOLE_D / 2)
    extrude(amount=-THICKNESS, mode=Mode.SUBTRACT)

    # upright wall on the back edge (YZ-style plane shifted to back)
    back = bracket.faces().sort_by(Axis.Y)[-1]
    with BuildSketch(Plane(back)):
        Rectangle(LENGTH, WALL_HEIGHT, align=None)
    extrude(amount=-THICKNESS)

    # strengthen the inner corner
    inner = bracket.edges().filter_by(Axis.X).group_by(Axis.Z)[1]
    fillet(inner, radius=FILLET_R)

show(bracket)
save(bracket.part, "05_parametric_bracket")
