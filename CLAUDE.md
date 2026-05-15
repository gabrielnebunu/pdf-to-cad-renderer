# CLAUDE.md — Instructions for Claude Code

This file tells Claude Code how to work in this repo.

## Project Overview
Convert PDF schematics → production-ready DXF/SVG CAD files.
Backend: Python/FastAPI. Frontend: Next.js/TypeScript.

## Stack
- Python 3.11, FastAPI, PyMuPDF, OpenCV, potracer, ezdxf, svgpathtools
- Node 20, Next.js 14, TypeScript, TailwindCSS

## Workflow
1. Backend lives in `/backend`. Run with `uvicorn main:app --reload`.
2. Frontend lives in `/frontend`. Run with `npm run dev`.
3. Full stack: use `docker-compose up`.

## Key Files
- `backend/pipeline/` — the 5-step conversion pipeline
- `backend/main.py` — FastAPI routes
- `frontend/app/page.tsx` — UI

## When Adding Features
- New pipeline step → add a file in `backend/pipeline/`
- Update `main.py` to wire it in
- Update `requirements.txt` if adding packages
- Keep each pipeline step single-responsibility

## Testing
- Drop a PDF into `examples/`
- Call `POST /convert` via curl or the frontend
- Inspect output DXF with FreeCAD or LibreCAD

## Conventions
- Use `loguru` for all logging (`from loguru import logger`)
- Use type hints everywhere
- Keep pipeline functions pure: in_path + out_dir → out_path
