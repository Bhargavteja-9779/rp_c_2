"""Assemble GENETICS supplementary files and check size limits (<= 2 MB each, <= 10 MB total).

File S1: pre-specified design + deviation log (PDF, via headless Chromium; Markdown copy kept)
File S2: supplementary tables (XLSX, one sheet per table; all machine-generated)
File S3: code archive (ZIP of code/ without data, caches and per-job outputs)
"""
from __future__ import annotations

import json
import subprocess
import sys
import zipfile
from pathlib import Path

import markdown
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_pdf import CSS, chromium  # noqa: E402
from kincp.utils import CODE_ROOT, PKG_ROOT, RESULTS_DIR, TAB_DIR, dump_json  # noqa: E402

SUP = PKG_ROOT / "supplementary"
MB = 2 ** 20


def file_s1():
    md = "# File S1. Pre-specified study design and log of deviations\n\n"
    md += (SUP / "S0_preregistered_design.md").read_text().replace("# Pre-specified", "## Pre-specified", 1)
    md += "\n\n" + (SUP / "S9_deviations.md").read_text().replace("# Deviations", "## Deviations", 1)
    (SUP / "File_S1_design_and_deviations.md").write_text(md)
    html = SUP / "File_S1.html"
    html.write_text(f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>"
                    f"{markdown.markdown(md, extensions=['tables'])}</body></html>")
    pdf = SUP / "File_S1_design_and_deviations.pdf"
    subprocess.run([chromium(), "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={pdf}", html.as_uri()], check=True, capture_output=True, timeout=300)
    html.unlink()
    return pdf


def file_s2():
    sheets = {
        "README": pd.DataFrame({"sheet": [], "content": []}),
        "S1_all_units": pd.read_csv(TAB_DIR / "TableS_all_units.csv"),
        "S2_stats_GBLUP_all": pd.read_csv(TAB_DIR / "Table3_statistics_GBLUP.csv"),
        "S3_stats_RKHS_LightGBM": pd.read_csv(TAB_DIR / "TableS_statistics_other_bases.csv"),
        "S4_stats_species": pd.read_csv(RESULTS_DIR / "statistics_species.csv"),
        "S5_maxkin_endpoint": pd.read_csv(RESULTS_DIR / "alt_relatedness_statistics.csv"),
        "S6_oracle_rescaling": pd.read_csv(RESULTS_DIR / "oracle_inflation_statistics.csv"),
        "S7_dedup": pd.read_csv(TAB_DIR / "TableS_dedup.csv"),
        "S8_simulation": pd.read_csv(TAB_DIR / "Table6_simulation.csv"),
        "S9_pev_calibration": pd.read_csv(RESULTS_DIR / "pev_calibration.csv"),
        "S10_sensitivity": pd.read_csv(TAB_DIR / "Table8_sensitivity.csv"),
        "S11_runtime": pd.read_csv(TAB_DIR / "Table7_runtime.csv"),
        "S12_scaling": pd.read_csv(RESULTS_DIR / "scaling.csv"),
        "S13_selection": pd.read_csv(TAB_DIR / "Table9_selection.csv"),
        "S14_error_units": pd.read_csv(RESULTS_DIR / "error_analysis_units.csv"),
    }
    raw = pd.read_csv(RESULTS_DIR / "raw_results.csv")
    keep = ["tag", "base", "regime", "dataset", "trait", "method", "alpha", "coverage", "cond_err", "worst_bin_cov", "width", "iscore"]
    extra = raw[raw.tag.isin(["granularity", "families", "explore", "competitor"]) & (raw.alpha == 0.10)][keep]
    sheets["S15_robustness_units"] = extra
    sheets["README"] = pd.DataFrame({"sheet": list(sheets)[1:], "content": [
        "Per dataset x trait unit: all methods, base predictors and regimes (alpha = 0.10)",
        "Paired Wilcoxon tests, GBLUP, all endpoints and families (baselines, ablations)",
        "Paired Wilcoxon tests, RKHS and LightGBM",
        "Species-level paired tests (10 units)",
        "Conditional coverage on quintiles of maximum genomic relationship (independent of d)",
        "Oracle width-rescaling analysis (Reviewer 8)",
        "Near-duplicate removal sensitivity",
        "Simulation on real genotypes",
        "Calibration of d for true genetic values (simulation)",
        "Bandwidth, mass floor and nominal-level sensitivity",
        "Per-fold runtime from main runs (contended)",
        "Controlled single-thread scaling benchmark",
        "Selection-conditional analysis",
        "Error analysis per unit",
        "Granularity (k=3,10), family-out, exploratory and group-CV+ runs, per unit"]})
    out = SUP / "File_S2_supplementary_tables.xlsx"
    with pd.ExcelWriter(out) as xw:
        for name, df in sheets.items():
            df.to_excel(xw, sheet_name=name[:31], index=False)
    return out


def file_s3():
    out = SUP / "File_S3_code.zip"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(CODE_ROOT.rglob("*")):
            rel = p.relative_to(CODE_ROOT)
            top_level_excluded = rel.parts[0] in ("data", "cache")
            if p.is_file() and not top_level_excluded and not any(part in ("__pycache__", ".pytest_cache") for part in rel.parts):
                z.write(p, Path("code") / rel)
    return out


def main():
    files = [file_s1(), file_s2(), file_s3()]
    sizes = {f.name: round(f.stat().st_size / MB, 3) for f in files}
    report = dict(sizes_mb=sizes, total_mb=round(sum(sizes.values()), 3),
                  each_le_2mb=all(v <= 2 for v in sizes.values()), total_le_10mb=sum(sizes.values()) <= 10)
    dump_json(report, SUP / "supplement_size_check.json")
    print(json.dumps(report, indent=1))


if __name__ == "__main__":
    main()
