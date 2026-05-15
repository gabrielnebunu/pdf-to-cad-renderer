"""Step 3: Raster (PNG) → SVG using Potrace.

Uses system potrace CLI (recommended) or potracer Python package as fallback.
Windows: install potrace from https://potrace.sourceforge.net/#downloading
Linux:   apt install potrace
"""
import os
import subprocess
from loguru import logger
from PIL import Image


def vectorize_to_svg(img_path: str, output_dir: str) -> str:
    """
    Convert a binarized PNG to SVG.
    Returns path to SVG.
    """
    out_svg = os.path.join(output_dir, "vectorized.svg")

    # Try system potrace first (best quality)
    try:
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
        logger.warning("System potrace not found, falling back to potracer Python package")

    # Fallback: potracer 0.0.4 API
    # Note: potracer 0.0.4 has a different API than later versions
    try:
        import potracer
        img_pil = Image.open(img_path).convert("1")  # pure B&W
        width, height = img_pil.size
        # Build pixel data list
        pixels = list(img_pil.getdata())
        bm = potracer.Bitmap(width, height, data=pixels)
        path = bm.trace()
        with open(out_svg, "w") as f:
            f.write(path.to_svg(width=width, height=height))
        logger.info(f"Vectorized (potracer 0.0.4) → {out_svg}")
        return out_svg
    except Exception as e:
        logger.error(f"potracer failed: {e}")
        raise RuntimeError(
            "No vectorizer available. Install potrace: https://potrace.sourceforge.net/#downloading\n"
            f"Original error: {e}"
        )
