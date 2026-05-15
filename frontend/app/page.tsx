'use client';
import { useState, useCallback } from 'react';

const API = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000';

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [page, setPage] = useState(1);
  const [dpi, setDpi] = useState(300);
  const [format, setFormat] = useState('dxf');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    const f = e.dataTransfer.files[0];
    if (f?.type === 'application/pdf') setFile(f);
  }, []);

  const handleConvert = async () => {
    if (!file) return;
    setLoading(true);
    setError('');
    const form = new FormData();
    form.append('file', file);
    try {
      const res = await fetch(`${API}/convert?page=${page}&dpi=${dpi}&output_format=${format}`, {
        method: 'POST',
        body: form,
      });
      if (!res.ok) throw new Error(await res.text());
      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `output.${format}`;
      a.click();
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main style={{ maxWidth: 640, margin: '60px auto', fontFamily: 'sans-serif', padding: '0 20px' }}>
      <h1 style={{ fontSize: 28, marginBottom: 8 }}>PDF → CAD Renderer</h1>
      <p style={{ color: '#666', marginBottom: 32 }}>Upload a PDF schematic and download a production-ready DXF or SVG.</p>

      <div
        onDrop={handleDrop}
        onDragOver={e => e.preventDefault()}
        onClick={() => document.getElementById('fileInput')?.click()}
        style={{
          border: '2px dashed #ccc', borderRadius: 12, padding: 40,
          textAlign: 'center', cursor: 'pointer', marginBottom: 24,
          background: file ? '#f0fff4' : '#fafafa'
        }}
      >
        {file ? <span>📄 {file.name}</span> : <span>Drop PDF here or click to browse</span>}
        <input id="fileInput" type="file" accept=".pdf" hidden onChange={e => setFile(e.target.files?.[0] ?? null)} />
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 16, marginBottom: 24 }}>
        <label>Page<br/><input type="number" min={1} value={page} onChange={e => setPage(+e.target.value)} style={{ width: '100%', padding: 8, borderRadius: 6, border: '1px solid #ddd' }} /></label>
        <label>DPI<br/><select value={dpi} onChange={e => setDpi(+e.target.value)} style={{ width: '100%', padding: 8, borderRadius: 6, border: '1px solid #ddd' }}>
          <option value={150}>150</option><option value={300}>300</option><option value={600}>600</option>
        </select></label>
        <label>Format<br/><select value={format} onChange={e => setFormat(e.target.value)} style={{ width: '100%', padding: 8, borderRadius: 6, border: '1px solid #ddd' }}>
          <option value="dxf">DXF</option><option value="svg">SVG</option><option value="both">Both (ZIP)</option>
        </select></label>
      </div>

      {error && <p style={{ color: 'red', marginBottom: 16 }}>{error}</p>}

      <button
        onClick={handleConvert}
        disabled={!file || loading}
        style={{
          width: '100%', padding: '14px', borderRadius: 8, border: 'none',
          background: loading ? '#aaa' : '#01696f', color: '#fff',
          fontSize: 16, cursor: loading ? 'not-allowed' : 'pointer'
        }}
      >
        {loading ? 'Converting...' : 'Convert to CAD'}
      </button>
    </main>
  );
}
