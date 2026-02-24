# kano-from-interviews

An end-to-end skill for generating KANO model analysis and visualizations from qualitative user interview transcripts.

## What It Does

1. **Extract** `.doc`/`.docx` interview transcripts and merge them into plain text
2. **Search** for feature-related user quotes using customizable keyword lists
3. **Count** mention frequency per feature (offline vs. online interviews)
4. **Classify** features into KANO categories using qualitative inference
5. **Generate** a hand-drawn academic-style HTML visualization

## Output

- `kano_evidence.json` — Structured evidence with user quotes per feature
- `summary.txt` — Mention frequency ranking table
- `kano_chart.html` — Interactive KANO quadrant chart (open in browser)

## Quick Start

```bash
pip install python-docx pywin32

# 1. Extract transcripts
python scripts/extract_transcripts.py --offline path/to/offline --online path/to/online --out ./output

# 2. Define features in features.json (see references/feature_keywords_example.md)

# 3. Analyze
python scripts/analyze_kano.py --features features.json --offline output/merged_offline.txt --online output/merged_online.txt --out ./output
```

## Files

```
kano-from-interviews/
├── SKILL.md                          # Main skill instructions (for Antigravity AI)
├── scripts/
│   ├── extract_transcripts.py        # Step 1: Extract & merge .doc/.docx files
│   └── analyze_kano.py               # Step 2: Keyword search & frequency counting
└── references/
    ├── feature_keywords_example.md   # How to define features & keywords
    ├── kano_classification_guide.md  # KANO classification decision guide
    └── chart_template_guide.md       # HTML chart visual specs & data format
```

## Requirements

- Python 3.8+
- `python-docx` (for .docx files)
- `pywin32` (for .doc files, Windows only)
