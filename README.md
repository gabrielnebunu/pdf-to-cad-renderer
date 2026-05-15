# PDF to CAD Renderer 🔧

Convert PDF schematics to production-ready CAD files (DXF/SVG) using computer vision, vectorization, and `ezdxf`.

Built with **Python 3.11+** backend + **Next.js** frontend. Developed in VS Code with Claude.

---

## 🔑 Key Repos Used (as submodules / dependencies)

| Library / Repo | Role |
|---|---|
| [ezdxf](https://github.com/mozman/ezdxf) | Generate & write DXF CAD files |
| [mjecke/pyPDFtoDXF](https://github.com/mjecke/pyPDFtoDXF) | Reference: PDF vector → DXF via Inkscape/pdf2svg |
| [naufraghi/pdf2dxf](https://github.com/naufraghi/pdf2dxf) | Reference: pdfalto + dxfwrite pipeline |
| [surveyorstories/pdfextract](https://github.com/surveyorstories/pdfextract) | PDF → DXF converter (QGIS plugin / standalone) |
| [tatarize/potrace](https://github.com/tatarize/potrace) | Pure Python Potrace — raster → vector tracing |
| [Adam-CAD/CADAM](https://github.com/Adam-CAD/CADAM) | CAD automation reference |
| [Kozea/CairoSVG](https://github.com/Kozea/CairoSVG) | SVG → PDF/PNG conversion |
| [aspose-cad/Aspose.CAD-for-Python](https://github.com/aspose-cad/Aspose.CAD-for-Python) | Advanced CAD format support (DWG/DXF/IFC) |

---

## 🏗️ Architecture

```
pdf-to-cad-renderer/
├── backend/              # Python FastAPI service
│   ├── pipeline/
│   │   ├── pdf_extractor.py   # Step 1: PDF → high-res raster (PyMuPDF)
│   │   ├── preprocessor.py    # Step 2: denoise, deskew, threshold (OpenCV)
│   │   ├── vectorizer.py      # Step 3: raster → SVG paths (potrace)
│   │   ├── dxf_builder.py     # Step 4: SVG paths → DXF entities (ezdxf)
│   │   └── exporter.py        # Step 5: export DXF / SVG / PDF
│   ├── main.py                # FastAPI app
│   └── requirements.txt
├── frontend/             # Next.js UI
│   ├── app/
│   │   └── page.tsx
│   └── package.json
├── examples/             # Sample schematics for testing
├── .env.example
├── docker-compose.yml
└── README.md
```

---

## ⚡ Quick Start

```bash
# 1. Clone
git clone https://github.com/gabrielnebunu/pdf-to-cad-renderer
cd pdf-to-cad-renderer

# 2. Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# 3. Frontend (separate terminal)
cd frontend
npm install
npm run dev
```

Visit `http://localhost:3000` — upload a PDF schematic, download DXF.

---

## 🔄 Pipeline Steps

1. **PDF → Raster** — PyMuPDF renders each page at 300 DPI
2. **Preprocess** — OpenCV: grayscale, adaptive threshold, denoise, deskew
3. **Vectorize** — Potrace traces raster to clean SVG bezier/line paths
4. **Build DXF** — ezdxf maps SVG entities to DXF LWPOLYLINE, LINE, ARC, CIRCLE, TEXT
5. **Export** — DXF (AutoCAD/FreeCAD ready), SVG, or clean PDF

---

## 📦 External Tools (system-level)

```bash
# Ubuntu/Debian
apt install potrace inkscape pdf2svg ghostscript

# Windows (choco)
choco install inkscape ghostscript
```
