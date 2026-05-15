"""Step 5: Package and export final files."""
import os
import shutil
from loguru import logger


def export_package(dxf_path: str, svg_path: str, output_dir: str, fmt: str = "dxf") -> str:
    """
    Return the appropriate output file based on requested format.
    fmt: 'dxf' | 'svg' | 'both' (returns zip)
    """
    if fmt == "dxf":
        logger.info(f"Export: DXF → {dxf_path}")
        return dxf_path
    elif fmt == "svg":
        logger.info(f"Export: SVG → {svg_path}")
        return svg_path
    elif fmt == "both":
        zip_base = os.path.join(output_dir, "cad_export")
        export_folder = os.path.join(output_dir, "cad_export_files")
        os.makedirs(export_folder, exist_ok=True)
        shutil.copy(dxf_path, export_folder)
        shutil.copy(svg_path, export_folder)
        zip_path = shutil.make_archive(zip_base, "zip", export_folder)
        logger.info(f"Export: ZIP → {zip_path}")
        return zip_path
    else:
        raise ValueError(f"Unknown format: {fmt}")
