# Infinity Research: Reproducible Data and Analysis Scripts

This repository contains the complete dataset and reproduction scripts for the article **"Infinity Research: A Modular and Transparent AI Platform for Automated Systematic Reviews"**.

## 🎯 Purpose

Provides **complete reproducibility** of all figures and analyses presented in the article using extracted JSON data from the Infinity Research platform.

## 📁 Repository Structure

```
infinity-research-paper/
├── json/                    # Raw extracted data (19 articles)
│   ├── Article_01/         # Individual article JSONs
│   │   ├── vision_json.json       # Vision extraction results
│   │   ├── apis_clean_json.json   # API consensus results
│   │   ├── llm_topics_json.json   # LLM topic analysis
│   │   ├── questions_json.json    # Questions phase
│   │   └── final_json.json        # Consolidated results
│   └── ... (Article_02 to Article_19)
├── scripts/                 # Reproduction scripts
│   ├── generate_cost_chart.py     # Figure 2: Cost Distribution
│   ├── generate_token_chart.py    # Figure 3: Token Consumption  
│   ├── generate_time_chart.py     # Figure 4: Processing Time
│   ├── generate_figure5_chart.py  # Figure 5: Vision vs Consensus
│   ├── generate_figure6_chart.py  # Figure 6: API Specialization Matrix
│   ├── *.png                      # Generated charts
│   └── *_legend.txt              # Generated figure legends
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🚀 Quick Start

### Prerequisites
```bash
pip install -r requirements.txt
```

### Reproduce All Figures
```bash
cd infinity-research-paper

# Generate all figures
python scripts/generate_cost_chart.py      # Figure 2
python scripts/generate_token_chart.py     # Figure 3  
python scripts/generate_time_chart.py      # Figure 4
python scripts/generate_figure5_chart.py   # Figure 5
python scripts/generate_figure6_chart.py   # Figure 6
```

### Output Files
Each script generates:
- **Chart**: `scripts/figureX_chart.png`
- **Legend**: `scripts/figureX_legend.txt`

## 📊 Generated Figures

| Script | Figure | Description | Key Metrics |
|--------|--------|-------------|-------------|
| `generate_cost_chart.py` | **Figure 2** | Cost Distribution | $0.833 total, 29.98% Vision, 58.03% Topics |
| `generate_token_chart.py` | **Figure 3** | Token Consumption | 540K tokens, 13.04% Vision, 54.33% Consensus |
| `generate_time_chart.py` | **Figure 4** | Processing Time | 45.5 min total, 17.93% Vision, 53.85% APIs |
| `generate_figure5_chart.py` | **Figure 5** | Vision vs Consensus | 87.1% → 94.3% (+7.2% improvement) |
| `generate_figure6_chart.py` | **Figure 6** | API Specialization Matrix | 159 Vision, 138 Europe PMC, 124 CrossRef |

## 🔬 Data Sources

### Article Processing Pipeline
1. **Vision JSON**: Claude 3.5 Sonnet baseline extraction
2. **APIs Clean JSON**: 11-API consensus with field_sources tracking
3. **LLM Topics JSON**: DeepSeek V3 topic classification  
4. **Questions JSON**: Question generation phase
5. **Final JSON**: Consolidated platform results

### Field Sources Tracking
- **`|` (pipe)**: Multi-source validation (e.g., `crossref|openalex`)
- **`+` (plus)**: Complementary data merging (e.g., `vision+europe_pmc`)
- **Single**: Single-source extraction (e.g., `vision`)

## ✅ Validation

All scripts reproduce the **exact numbers** reported in the article:
- ✅ **273/304** field combinations populated
- ✅ **159 Vision instances** (58.2% primary contributor)
- ✅ **87.1% → 94.3%** completion improvement
- ✅ **62.6% multi-source validation**

## 🔧 Technical Details

- **Data Format**: Standard JSON with nested cost_tracking and processing_time_ms
- **Visualization**: Matplotlib + Seaborn with official platform styling
- **Extraction Logic**: Mirrors core platform database queries
- **Independence**: No database connection required - uses extracted JSONs only

## 📈 Reproducibility

This repository ensures **complete scientific reproducibility** by:
1. **Raw Data**: All 19 articles with modular JSONs
2. **Exact Scripts**: Mirror platform's chart generation logic  
3. **Verified Numbers**: Match article figures precisely
4. **Independence**: Self-contained with no external dependencies

---

**Article**: "Infinity Research: A Modular and Transparent AI Platform for Automated Systematic Reviews"   
**Dataset**: 19 articles from "Comparison" project