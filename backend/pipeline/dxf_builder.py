"""Step 4: Parse SVG paths and map them to DXF entities using ezdxf."""
import ezdxf
from ezdxf.enums import TextEntityAlignment
import svgpathtools
import os
from loguru import logger


def svg_to_dxf(svg_path: str, output_dir: str) -> str:
    """
    Parse SVG paths and write DXF entities:
    - Bezier curves → approximated LWPOLYLINE
    - Lines → LINE
    - Circles → CIRCLE
    Returns path to .dxf file.
    """
    doc = ezdxf.new(dxfversion="R2010")
    msp = doc.modelspace()

    # Setup layers
    doc.layers.add("SCHEMATIC", color=7)    # white/black
    doc.layers.add("DIMENSIONS", color=3)   # green
    doc.layers.add("ANNOTATION", color=2)   # yellow

    paths, attributes = svgpathtools.svg2paths(svg_path)
    logger.info(f"Parsing {len(paths)} SVG paths")

    for path in paths:
        points = []
        for seg in path:
            seg_type = type(seg).__name__
            if seg_type == "Line":
                start = (seg.start.real, -seg.start.imag)  # flip Y for CAD
                end = (seg.end.real, -seg.end.imag)
                msp.add_line(start, end, dxfattribs={"layer": "SCHEMATIC"})
            elif seg_type in ("CubicBezier", "QuadraticBezier"):
                # Approximate bezier as polyline
                pts = _bezier_to_points(seg, steps=20)
                if len(pts) >= 2:
                    msp.add_lwpolyline(
                        pts, dxfattribs={"layer": "SCHEMATIC", "closed": False}
                    )
            elif seg_type == "Arc":
                pts = _arc_to_points(seg, steps=24)
                if len(pts) >= 2:
                    msp.add_lwpolyline(
                        pts, dxfattribs={"layer": "SCHEMATIC", "closed": False}
                    )

    out_path = os.path.join(output_dir, "output.dxf")
    doc.saveas(out_path)
    logger.info(f"DXF built → {out_path}")
    return out_path


def _bezier_to_points(seg, steps: int = 20):
    return [
        (seg.point(t / steps).real, -seg.point(t / steps).imag)
        for t in range(steps + 1)
    ]


def _arc_to_points(seg, steps: int = 24):
    return [
        (seg.point(t / steps).real, -seg.point(t / steps).imag)
        for t in range(steps + 1)
    ]
