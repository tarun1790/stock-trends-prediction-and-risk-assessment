"""
System Design Specification (SDD) & Engineering Blueprint PDF Compiler.
Assembles Section 1 through Section 5, integrates 13 traditional monochrome vector SVG diagrams,
and compiles the publication-grade PDF via Google Chrome Headless.

Author: Tarun Jampani (tarun1790)
Email: tarun.jampani45@gmail.com
Hardware Substrate: NVIDIA GeForce RTX 3070 Ti Laptop GPU (CUDA 12.x)
Release: Version 3.0.0 (Production Operational)
"""

import os
import sys
import shutil
import subprocess

# Ensure repo root and docs/design_spec are in sys.path
REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
DESIGN_SPEC_DIR = os.path.join(REPO_ROOT, "docs", "design_spec")
for p in [REPO_ROOT, DESIGN_SPEC_DIR]:
    if p not in sys.path:
        sys.path.insert(0, p)

from docs.design_spec import section1_system_arch as s1
from docs.design_spec import section2_module_design as s2
from docs.design_spec import section3_database_design as s3
from docs.design_spec import section4_uml_diagrams as s4
from docs.design_spec import section5_data_flow_design as s5

HTML_OUT = os.path.join(REPO_ROOT, "StockTrend_AI_System_Design_Specification.html")
PDF_OUT = os.path.join(REPO_ROOT, "StockTrend_AI_System_Design_Specification.pdf")

DOWNLOADS_DIR = os.path.join(os.path.expanduser("~"), "Downloads")
VERIFY5_DIR = os.path.join(DOWNLOADS_DIR, "verify5")
os.makedirs(VERIFY5_DIR, exist_ok=True)

PDF_DEST_VERIFY5 = os.path.join(VERIFY5_DIR, "StockTrend_AI_System_Design_Specification.pdf")
PDF_DEST_DOWNLOADS = os.path.join(DOWNLOADS_DIR, "StockTrend_AI_System_Design_Specification.pdf")

print("Compiling Traditional Monochrome System Design Specification HTML Document...")

# HTML Header with traditional academic print styles, A4 geometry, running headers/footers, and serif typography
html_head = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>AlphaTemporal: System Design Specification (SDD) &amp; Engineering Architecture</title>
<style>
  @page {
    size: A4;
    margin: 14mm 14mm 16mm 14mm;
    @top-center {
      content: "StockTrend AI / AlphaTemporal System Design Specification (SDD)";
      font-family: "Times New Roman", Times, "TeX Gyre Termes", Georgia, serif;
      font-size: 8pt;
      font-variant: small-caps;
      letter-spacing: 0.5px;
      color: #333333;
      border-bottom: 0.5pt solid #000000;
      padding-bottom: 2pt;
      width: 100%;
    }
    @bottom-right {
      content: "Page " counter(page);
      font-size: 8pt;
      font-family: "Times New Roman", Times, "TeX Gyre Termes", Georgia, serif;
      color: #000000;
      border-top: 0.5pt solid #000000;
      padding-top: 3pt;
    }
    @bottom-left {
      content: "AlphaTemporal Formal Architecture Blueprint | Author: Tarun Jampani";
      font-size: 8pt;
      font-family: "Times New Roman", Times, "TeX Gyre Termes", Georgia, serif;
      color: #333333;
      border-top: 0.5pt solid #000000;
      padding-top: 3pt;
    }
  }

  *, *:before, *:after { box-sizing: border-box; }

  body {
    font-family: "Times New Roman", Times, "TeX Gyre Termes", Georgia, serif;
    color: #000000;
    background: #ffffff;
    line-height: 1.55;
    font-size: 9.3pt;
    margin: 0;
    padding: 0;
  }

  h1, h2, h3, h4, h5 {
    font-family: "Times New Roman", Times, "TeX Gyre Termes", Georgia, serif;
    color: #000000;
    font-weight: bold;
    line-height: 1.25;
    margin-top: 1.2em;
    margin-bottom: 0.4em;
    page-break-after: avoid;
  }

  h1 { 
    font-size: 19pt; 
    border-bottom: 2pt solid #000000; 
    padding-bottom: 4px; 
    margin-top: 0; 
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
  h2 { 
    font-size: 13pt; 
    border-bottom: 1.2pt solid #000000; 
    padding-bottom: 3px; 
    margin-top: 1.3em; 
    text-transform: uppercase;
    letter-spacing: 0.3px;
  }
  h3 { 
    font-size: 10.8pt; 
    margin-top: 1em; 
    border-left: none; 
    padding-left: 0;
    font-style: normal;
  }
  h4 { 
    font-size: 9.8pt; 
    font-style: italic;
    margin-top: 0.8em; 
  }

  p { margin: 0.5em 0; text-align: justify; }
  ul, ol { margin: 0.45em 0; padding-left: 22px; }
  li { margin-bottom: 0.3em; text-align: justify; }

  /* Traditional Academic Booktabs Tables */
  table {
    width: 100%;
    border-collapse: collapse;
    margin: 10pt 0;
    font-size: 8.3pt;
    font-family: "Times New Roman", Times, "TeX Gyre Termes", Georgia, serif;
    page-break-inside: avoid;
  }

  th, td {
    border: none;
    border-bottom: 0.5pt solid #cccccc;
    padding: 4.5pt 6pt;
    text-align: left;
    vertical-align: top;
    color: #000000;
  }

  th {
    border-top: 1.5pt solid #000000;
    border-bottom: 1pt solid #000000;
    background: #f2f2f2;
    color: #000000;
    font-weight: bold;
    font-size: 8.5pt;
  }

  tr:nth-child(even) td { background: #fafafa; }
  tr:last-child td { border-bottom: 1.5pt solid #000000; }

  /* Traditional Monospace Code */
  code {
    background: #f4f4f4;
    color: #000000;
    padding: 1px 3px;
    border: 0.5pt solid #999999;
    font-family: "Courier New", Courier, monospace;
    font-size: 8.2pt;
  }

  pre {
    background: #fafafa;
    border: 1pt solid #000000;
    padding: 8pt;
    font-size: 8pt;
    color: #000000;
    line-height: 1.4;
    font-family: "Courier New", Courier, monospace;
    page-break-inside: avoid;
  }

  /* Traditional Technical Report Title Block */
  .title-block {
    border-top: 2.5pt solid #000000;
    border-bottom: 1pt solid #000000;
    padding: 16pt 0 14pt 0;
    margin-bottom: 16pt;
    text-align: center;
  }
  .title-block .sub-heading {
    font-size: 10pt;
    font-weight: bold;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 6pt;
    color: #333333;
  }
  .title-block h1 {
    font-size: 22pt;
    font-weight: bold;
    margin: 4pt 0 6pt 0;
    border: none;
    padding: 0;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #000000;
  }
  .title-block .description {
    font-size: 11.5pt;
    font-style: italic;
    margin-bottom: 10pt;
    color: #222222;
  }
  .title-block .meta-grid {
    font-size: 9pt;
    line-height: 1.6;
    color: #000000;
    margin-top: 10pt;
    border-top: 0.5pt solid #cccccc;
    padding-top: 8pt;
  }

  .formal-box {
    border: 1pt solid #000000;
    background: #fafafa;
    padding: 10pt 14pt;
    margin: 12pt 0;
    page-break-inside: avoid;
  }
  .formal-box .box-title {
    font-weight: bold;
    font-size: 9.5pt;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    border-bottom: 0.5pt solid #000000;
    padding-bottom: 3pt;
    margin-bottom: 6pt;
  }

  .diagram-container {
    text-align: center;
    margin: 10pt 0;
    padding: 6pt;
    border: 1pt solid #000000;
    background: #ffffff;
    page-break-inside: avoid;
  }
  .diagram-container svg {
    max-width: 100%;
    height: auto;
  }

  .page-break { page-break-before: always; }

  /* Native MathML styling in Traditional Serif */
  math {
    font-family: 'Cambria Math', 'STIX Two Math', 'Latin Modern Math', 'Times New Roman', serif;
    font-style: normal;
  }
  div.math-display {
    background: #fafafa;
    border: 0.75pt solid #000000;
    padding: 6pt 10pt;
    margin: 8pt 0;
    text-align: center;
    overflow-x: auto;
    page-break-inside: avoid;
  }
  div.math-display math {
    font-size: 10.5pt;
    display: inline-block;
  }
</style>
</head>
<body>
"""

# Traditional Cover Page Header
cover_html = """
<div class="title-block">
  <div class="sub-heading">Formal Engineering Design Specification &bull; Traditional Academic Standard</div>
  <h1>StockTrend AI / AlphaTemporal</h1>
  <div class="description">System Design Specification (SDD), Relational Database Schema, UML 2.5 Catalog &amp; Multi-Level Data Flow Architecture</div>
  <div class="meta-grid">
    <strong>Author / Lead Architect:</strong> Tarun Jampani (<code>tarun1790</code>) &nbsp;|&nbsp; 
    <strong>Email:</strong> <code>tarun.jampani45@gmail.com</code><br/>
    <strong>Hardware Acceleration Substrate:</strong> NVIDIA GeForce RTX 3070 Ti Laptop GPU (CUDA 12.x, 8,191.5 MB VRAM)<br/>
    <strong>Document Classification:</strong> System Architecture &amp; Engineering Specification (IEEE/ISO Compliant)<br/>
    <strong>Production Version:</strong> 3.0.0 &nbsp;|&nbsp; 
    <strong>Publication Date:</strong> September 2026
  </div>
</div>

<div class="formal-box">
  <div class="box-title">Document Scope &amp; Engineering Charter</div>
  <p style="margin: 0; font-size: 8.8pt; color: #000000; line-height: 1.55;">
    This document constitutes the definitive formal System Design Specification (SDD) for the AlphaTemporal institutional trading and predictive intelligence platform. It details the complete physical and logical architecture, 10 primary software modules, 3NF relational database schema across 12 relations, all 8 required formal UML 2.5 diagrams (Use Case, Class, Sequence, Collaboration, Activity, Component, Deployment, and State-Chart), and 3 levels of Data Flow Diagrams (DFD Level 0, Level 1, and Level 2) formatted strictly according to traditional monochrome technical publication standards.
  </p>
</div>

<h3>Table of Contents</h3>
<ol style="font-size: 9pt; line-height: 1.65;">
  <li><strong>Section 1: System Architecture &amp; Hardware Substrate</strong> &mdash; 5-tier architecture, layer interactions, hardware boundaries, and vector system blueprint.</li>
  <li><strong>Section 2: Detailed Module Design</strong> &mdash; Comprehensive specification of all 10 modules: Data Ingestion &amp; Session Locking, 26-Indicator Vectorization, Fractional Differentiation, Temporal Deep Learning (TCN &amp; TFT), Stacking Meta-Ensemble, Chow Selective Classification, Merton &amp; Altman Credit Risk, Dynamic Triple-Barrier Backtesting, FastAPI Gateway, and UI Terminal.</li>
  <li><strong>Section 3: Relational Database Design</strong> &mdash; Vector ER Diagram, 12 normalized relational database tables (3NF), primary/foreign keys, check constraints, and composite B-Tree indexing.</li>
  <li><strong>Section 4: Formal UML Diagram Catalog (UML 2.5)</strong> &mdash; Complete suite of 8 diagrams: Use Case, Class, Sequence, Collaboration, Activity, Component, Deployment, and State-Chart diagrams.</li>
  <li><strong>Section 5: Data Flow Design (DFD Levels 0, 1, and 2)</strong> &mdash; Context Level 0, Subsystem Level 1, Detailed Level 2 DFDs, and exhaustive Data Flow Dictionary.</li>
</ol>
"""

# Assemble All Sections
full_html = (
    html_head
    + cover_html
    + s1.get_section1_html()
    + s2.get_section2_html()
    + s3.get_section3_html()
    + s4.get_section4_html()
    + s5.get_section5_html()
    + "\n</body>\n</html>"
)

with open(HTML_OUT, "w", encoding="utf-8") as f:
    f.write(full_html)

print(f"Generated HTML successfully: {len(full_html)} chars (~{len(full_html)//1024} KB)")

# Compile PDF via Google Chrome Headless
chrome_exe = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(chrome_exe):
    # Try alternate location
    chrome_exe = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

if os.path.exists(chrome_exe):
    cmd = [
        chrome_exe,
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--run-all-compositor-stages-before-draw",
        f"--print-to-pdf={PDF_OUT}",
        HTML_OUT
    ]
    print("Compiling Traditional Monochrome Master PDF via Google Chrome Headless...")
    res = subprocess.run(cmd, capture_output=True, text=True)

    if os.path.exists(PDF_OUT):
        size = os.path.getsize(PDF_OUT)
        print(f"SUCCESS: Compiled Traditional Monochrome PDF ({size:,} bytes) at {PDF_OUT}")
        shutil.copy2(PDF_OUT, PDF_DEST_VERIFY5)
        shutil.copy2(PDF_OUT, PDF_DEST_DOWNLOADS)
        print(f"Replicated PDF to:\n  - {PDF_DEST_VERIFY5}\n  - {PDF_DEST_DOWNLOADS}")
    else:
        print(f"Error: PDF was not generated! Chrome stderr: {res.stderr}")
else:
    print(f"Warning: Chrome not found at {chrome_exe}. HTML written at {HTML_OUT}.")
