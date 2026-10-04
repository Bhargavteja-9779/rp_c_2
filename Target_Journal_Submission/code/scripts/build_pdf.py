"""Render manuscript/Final_Manuscript.md (+ figures) to PDF with headless Chromium (review copy).

The DOCX is the submission master; this PDF is a convenience copy for reviewers / single-file upload.
"""
from __future__ import annotations

import glob
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import markdown

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from kincp.utils import FIG_DIR, PKG_ROOT  # noqa: E402

MS = PKG_ROOT / "manuscript"
CSS = """
body{font-family:'Times New Roman',Times,serif;font-size:11pt;line-height:1.6;margin:0 auto;max-width:6.6in;color:#000;background:#fff}
h1{font-size:16pt;text-align:center} h2{font-size:13pt;margin-top:1.4em} h3{font-size:11.5pt}
table{border-collapse:collapse;font-size:7pt;margin:0.6em 0;width:100%} th,td{border-bottom:0.5px solid #888;padding:2px 3px;text-align:left}
img{max-width:100%;display:block;margin:0.8em auto} p{text-align:justify}
@page{size:Letter;margin:0.9in}
"""


def chromium() -> str:
    c = sorted(glob.glob("/opt/pw-browsers/chromium-*/chrome-linux/chrome")) or \
        sorted(glob.glob(os.path.expanduser("~/.cache/ms-playwright/chromium-*/chrome-linux/chrome")))
    for name in ("chromium", "chromium-browser", "google-chrome"):
        if not c:
            p = subprocess.run(["which", name], capture_output=True, text=True).stdout.strip()
            if p:
                c = [p]
    if not c:
        raise FileNotFoundError("no Chromium found")
    return c[-1]


def main():
    md = (MS / "Final_Manuscript.md").read_text()
    figspec = json.load(open(MS / "src" / "figures.json"))
    # embed each figure image directly above its legend
    for f in figspec:
        md = md.replace(f"**{f['label']}** ", f"![{f['label']}]({(FIG_DIR / (f['file'] + '.png')).as_uri()})\n\n**{f['label']}** ", 1)
    html = markdown.markdown(md, extensions=["tables"])
    html = re.sub(r"<p><img", "<p style='page-break-inside:avoid'><img", html)
    out_html = MS / "Final_Manuscript.html"
    out_html.write_text(f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{html}</body></html>")
    pdf = MS / "Final_Manuscript.pdf"
    subprocess.run([chromium(), "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={pdf}", out_html.as_uri()], check=True, capture_output=True, timeout=300)
    out_html.unlink()
    print("wrote", pdf)


if __name__ == "__main__":
    main()
