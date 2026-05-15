"""Step 1: PDF page → high-resolution raster image using PyMuPDF (fitz)."""
import fitz  # PyMuPDF
import os
from loguru import logger


def extract_pages(pdf_path: str, output_dir: str, page: int = 1, dpi: int = 300) -> str:
    """
    Render a single PDF page to a PNG at the given DPI.
    Returns the path to the rendered PNG.
    """
    doc = fitz.open(pdf_path)
    page_index = page - 1  # 0-based

    if page_index >= len(doc):
        raise ValueError(f"Page {page} does not exist. PDF has {len(doc)} pages.")

    pg = doc[page_index]
    zoom = dpi / 72  # PDF native DPI is 72
    mat = fitz.Matrix(zoom, zoom)
    pix = pg.get_pixmap(matrix=mat, alpha=False)

    out_path = os.path.join(output_dir, f"page_{page}.png")
    pix.save(out_path)
    logger.info(f"Extracted page {page} → {out_path} ({pix.width}x{pix.height} px)")
    return out_path
