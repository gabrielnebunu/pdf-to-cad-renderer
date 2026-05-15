# Windows Setup Guide

This project runs on **Windows** with Python 3.10+. Follow these steps exactly.

---

## 1. Install Python dependencies

```powershell
cd pdf-to-cad-renderer\backend
pip install -r requirements.txt
```

## 2. Install system tools (Windows)

You need **Potrace** for vectorization. The `apt` command does NOT work on Windows.

### Option A — Chocolatey (recommended if you have it)
```powershell
choco install potrace ghostscript
```

### Option B — Manual install
1. Download potrace `.exe` from https://potrace.sourceforge.net/#downloading
2. Extract and add the folder to your PATH:
   ```powershell
   # Example — adjust path to where you extracted it:
   $env:PATH += ";C:\tools\potrace"
   # To make it permanent:
   [System.Environment]::SetEnvironmentVariable("PATH", $env:PATH + ";C:\tools\potrace", "User")
   ```
3. Verify: `potrace --version`

> **Note**: Ghostscript and Inkscape are optional — the pipeline works without them.
> If you skip potrace, the Python `potracer` package is used as fallback (slower, lower quality).

---

## 3. Run the backend

```powershell
# From backend/ folder:
python -m uvicorn main:app --reload
```

Use `python -m uvicorn` (not just `uvicorn`) — this avoids PATH issues on Windows.

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

---

## 4. Run the frontend

```powershell
cd ..\frontend
npm install
npm run dev
```

Open http://localhost:3000

---

## 5. Quick test via curl (no frontend needed)

```powershell
# From any folder, with backend running:
curl -X POST http://localhost:8000/convert `
  -F "file=@C:\path\to\your\schematic.pdf" `
  -F "page=1" `
  -F "dpi=300" `
  -F "output_format=dxf" `
  --output output.dxf
```

---

## Troubleshooting

| Error | Fix |
|---|---|
| `uvicorn not recognized` | Use `python -m uvicorn main:app --reload` |
| `potracer==1.0.7 not found` | Already fixed in latest `requirements.txt` — uses `0.0.4` |
| `apt not recognized` | Use Chocolatey or manual install (see Step 2) |
| `ModuleNotFoundError: fitz` | `pip install PyMuPDF` (fitz is included in PyMuPDF) |
| `cairosvg` install fails | Run `pip install cairosvg` — may need GTK on Windows, see https://cairosvg.org/documentation/ |
