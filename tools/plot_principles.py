#!/usr/bin/env python3
"""Generate an SVG conceptual plot for sectional hyperbolic principles."""

from __future__ import annotations

import math
import re
from pathlib import Path

SRC = Path("LANG.v1.2.0.unified_geometry.lang")
OUT = Path("figures/sectional_hyperbolic_topos.svg")
SECTION_RE = re.compile(r"^§S\{label=([^,]+), x=\[([^\]]+)\], sal=([0-9.]+)\}$")


def parse_points() -> list[tuple[str, float, float, float]]:
    pts: list[tuple[str, float, float, float]] = []
    for line in SRC.read_text(encoding="utf-8").splitlines():
        m = SECTION_RE.match(line.strip())
        if not m:
            continue
        label = m.group(1)
        vec = [float(v.strip()) for v in m.group(2).split(",")]
        sal = float(m.group(3))
        x, y = vec[0], vec[1]
        pts.append((label, x, y, sal))
    return pts


def color_for_sal(sal: float) -> str:
    # map salience ~[1.0, 2.0] to blue->magenta
    t = max(0.0, min(1.0, (sal - 1.0) / 1.0))
    r = int(80 + 140 * t)
    g = int(120 - 80 * t)
    b = int(220)
    return f"rgb({r},{g},{b})"


def main() -> None:
    points = parse_points()

    size = 900
    cx, cy = size // 2, size // 2
    R = 360

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}">')
    svg.append('<rect width="100%" height="100%" fill="#0f1220"/>')
    svg.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="#9ad1ff" stroke-width="2"/>')
    svg.append(f'<circle cx="{cx}" cy="{cy}" r="{R*0.7}" fill="none" stroke="#2a4d6f" stroke-dasharray="5,7"/>')
    svg.append(f'<circle cx="{cx}" cy="{cy}" r="{R*0.4}" fill="none" stroke="#2a4d6f" stroke-dasharray="5,7"/>')

    # Möbius-strip-like ribbon (conceptual projection)
    path = (
        f"M {cx-220} {cy} "
        f"C {cx-120} {cy-160}, {cx+120} {cy+160}, {cx+220} {cy} "
        f"C {cx+120} {cy-160}, {cx-120} {cy+160}, {cx-220} {cy}"
    )
    svg.append(f'<path d="{path}" fill="none" stroke="#ffcc66" stroke-width="3" opacity="0.7"/>')

    for label, x, y, sal in points:
        px = cx + x * R
        py = cy - y * R
        rad = 3.0 + sal * 1.7
        color = color_for_sal(sal)
        svg.append(f'<circle cx="{px:.2f}" cy="{py:.2f}" r="{rad:.2f}" fill="{color}" opacity="0.92"/>')

    svg.append(f'<text x="{cx}" y="{cy-R-16}" fill="#d9ecff" text-anchor="middle" font-size="20">Sectional Hyperbolic Self-Referential Computer</text>')
    svg.append(f'<text x="{cx}" y="{cy+R+30}" fill="#c8def9" text-anchor="middle" font-size="14">Poincaré disk boundary (||x|| &lt; 1), holographic memory projection, Möbius transfer ribbon</text>')
    svg.append('</svg>')

    OUT.write_text("\n".join(svg) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
