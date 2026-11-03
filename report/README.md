# B.Tech project report (NIT Warangal)

LaTeX source of the Phase I project report. [`main.pdf`](main.pdf) is the latest
compiled copy. The layout follows the institute's *Guidelines for Preparation of B.Tech
Report*; the comments in `main.tex` give the guideline section for each setting.

| Path | What it is |
|---|---|
| `info.tex` | **Edit this first:** title, student names and roll numbers, supervisor, HOD, department, year |
| `main.tex` | Page layout and document order |
| `frontmatter/` | Title sheet, approval, declaration, certificate (Specimens A–D), abstract, abbreviations, publications, acknowledgements |
| `chapters/` | Introduction, literature review, method, results, conclusions, appendices |
| `refs.bib` | References (IEEE style) |
| `figures/`, `generated/` | Copied in by `python scripts/make_paper_figures.py`; do not edit by hand |

Put the institute emblem at `figures/nitw_logo.png` and the title sheet picks it up
automatically.

## Matching the department's sample report

The guideline measurements are set as lengths near the top of `main.tex`. If the
sample report looks different, adjust these instead of editing chapters:
- `\ChapterTop`: extra space above "Chapter N" (default 75 mm)
- `\SecGap`: space around section headings (default 15 mm)
- `\ParGap`: space between paragraphs (default 6 pt)

## Compile

**Overleaf:** zip this `report/` folder, then choose *New Project → Upload Project*.
The default compiler (pdfLaTeX) and BibTeX work without changes.

**Locally:** `tectonic -X compile main.tex`. Tectonic prints harmless font warnings
that pdfLaTeX does not.

## Before submission

- Fill in `info.tex`.
- Check the plagiarism score (the limit is 30%). The report is written separately
  from the paper, but both describe the same study.
- Confirm the literature-review entries for the IEEE letters against their full texts.
  Table 2.1's caption says these entries still need checking.
