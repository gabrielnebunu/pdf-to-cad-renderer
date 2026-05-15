from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import tempfile, os, shutil
from loguru import logger

from pipeline.pdf_extractor import extract_pages
from pipeline.preprocessor import preprocess_image
from pipeline.vectorizer import vectorize_to_svg
from pipeline.dxf_builder import svg_to_dxf
from pipeline.exporter import export_package

app = FastAPI(title="PDF to CAD Renderer", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/convert")
async def convert_pdf(
    file: UploadFile = File(...),
    page: int = 1,
    dpi: int = 300,
    output_format: str = "dxf",  # dxf | svg | both
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(400, "Only PDF files are supported")

    with tempfile.TemporaryDirectory() as tmpdir:
        pdf_path = os.path.join(tmpdir, "input.pdf")
        with open(pdf_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        logger.info(f"Processing {file.filename} page={page} dpi={dpi}")

        # Step 1: PDF → raster
        img_path = extract_pages(pdf_path, tmpdir, page=page, dpi=dpi)

        # Step 2: Preprocess
        clean_img_path = preprocess_image(img_path, tmpdir)

        # Step 3: Vectorize
        svg_path = vectorize_to_svg(clean_img_path, tmpdir)

        # Step 4: Build DXF
        dxf_path = svg_to_dxf(svg_path, tmpdir)

        # Step 5: Export
        result_path = export_package(dxf_path, svg_path, tmpdir, output_format)

        return FileResponse(
            result_path,
            filename=f"output.{output_format if output_format != 'both' else 'zip'}",
            media_type="application/octet-stream",
        )
