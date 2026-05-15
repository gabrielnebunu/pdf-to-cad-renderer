"""Step 3: Raster (PNG) → SVG using Potrace (pure Python port)."""
import os
import subprocess
from loguru import logger
from PIL import Image


def vectorize_to_svg(img_path: str, output_dir: str) -> str:
    """
    Convert a binarized PNG to SVG using potrace (system) or potracer (Python).
    Falls back to system potrace CLI if available, else uses potracer package.
    Returns path to SVG.
    """
    out_svg = os.path.join(output_dir, "vectorized.svg")

    # Try system potrace first (best quality)
    try:
        # potrace works on BMP
        bmp_path = img_path.replace(".png", ".bmp")
        img = Image.open(img_path).convert("L")
        img.save(bmp_path)
        result = subprocess.run(
            ["potrace", "-s", "-o", out_svg, bmp_path],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode == 0:
            logger.info(f"Vectorized (system potrace) → {out_svg}")
            return out_svg
        logger.warning(f"System potrace failed: {result.stderr}")
    except (FileNotFoundError, subprocess.TimeoutExpired):
        logger.warning("System potrace not found, falling back to potracer Python")

    # Fallback: potracer (pure Python)
    import potracer
    img = Image.open(img_path).convert("1")  # pure B&W
    bm = potracer.Bitmap(img)
    path = bm.trace(
        turdsize=2,
        turnpolicy=potracer.TURNPOLICY_MINORITY,
        alphamax=1.0,
        opticurve=True,
        opttolerance=0.2,
    )
    with open(out_svg, "w") as f:
        f.write(path.to_svg())
    logger.info(f"Vectorized (potracer) → {out_svg}")
    return out_svg
