from dataclasses import dataclass

from _helpers import save
from build123d import Part, Pos, RectangleRounded, Sketch, loft
from ocp_vscode import show


@dataclass(frozen=True)
class Ring:
    """One rounded-square cross section of a column, at height `z`."""

    z: float
    side: float
    corner_radius: float

    def sketch(self) -> Sketch:
        return RectangleRounded(self.side, self.side, radius=self.corner_radius).moved(
            Pos(0, 0, self.z)
        )


def rounded_column(profile: list[Ring], ruled: bool = True) -> Part:
    """Loft a vertical stack of rounded squares into one solid.

    `profile` is a list of `Ring`s, bottom to top. Use it for tapered / stepped
    square posts - e.g. a pallet foot that flares out, runs straight, then
    cones open again. `ruled=True` keeps each segment a straight cone (crisp
    knees between rings); `False` blends them smoothly.
    """
    if len(profile) < 2:
        raise ValueError("rounded_column needs at least two rings")
    sections: list[Sketch] = [ring.sketch() for ring in profile]
    return loft(sections, ruled=ruled)


FOOT_PROFILE = [
    Ring(z=0.00, side=5.58, corner_radius=0.65),
    Ring(z=0.80, side=7.08, corner_radius=1.25),
    Ring(z=2.60, side=7.08, corner_radius=1.25),
    Ring(z=4.73, side=11.30, corner_radius=3.65),
]

foot = rounded_column(FOOT_PROFILE)

show(foot)
save(foot, "foot")
