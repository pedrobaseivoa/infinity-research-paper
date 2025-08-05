# Infinity Research: Reproducible Data and Analysis Scripts

This repository contains the **complete dataset and reproduction scripts** for the article **"Infinity Research: A Modular and Transparent AI Platform for Automated Systematic Reviews"**.

## 🎯 Purpose

Provides **complete reproducibility** of all figures, tables, and analyses presented in the article using extracted JSON data from the Infinity Research platform.

## 📁 Repository Structure

```
infinity-research-paper/
├── README.md                    # This documentation
├── requirements.txt             # Python dependencies
├── json/                        # Raw extracted data (19 articles)
│   ├── Article_01/             # Individual article JSONs
│   │   ├── vision_json.json           # Claude 3.5 Sonnet baseline extraction
│   │   ├── apis_raw_json.json         # Raw API responses
│   │   ├── apis_clean_json.json       # 11-API consensus with field_sources
│   │   ├── llm_topics_json.json       # DeepSeek V3 topic classification
│   │   └── final_json.json            # Consolidated platform results
│   └── ... (Article_02 to Article_19)
├── analysis/                    # Manual analysis data
│   ├── analysis_claude.json           # Claude 3.5 Sonnet manual evaluation
│   ├── analysis_deepseek.json         # DeepSeek V3 manual evaluation
│   └── conflicts.json                 # Detailed conflict resolution analysis
├── scripts/                     # Reproduction scripts (Python only)
│   ├── generate_cost_chart.py          # Figure 2: Cost Distribution
│   ├── generate_token_chart.py         # Figure 3: Token Consumption
│   ├── generate_time_chart.py          # Figure 4: Processing Time
│   ├── generate_figure5_chart.py       # Figure 5: Vision vs Consensus Performance
│   ├── generate_figure6_chart.py       # Figure 6: API Specialization Matrix
│   ├── generate_concordance_table.py   # Table 4.5: Concordance Performance
│   ├── generate_field_analysis_table.py # Table 4.6: Field-by-Field Analysis
│   ├── generate_conflicts_table_simple.py # Table 4.7: Manual Resolution of Conflicts
│   ├── generate_conflicts_table.py     # Detailed conflict analysis (alternative)
│   ├── generate_accuracy_table_real.py  # Table 4.8: Infinity Research Real Accuracy Performance
│   └── generate_accuracy_table.py      # Alternative accuracy calculation
└── plots/                       # Generated outputs
    ├── *.png                           # Generated charts and figures
    └── *.txt                           # Generated legends and tables
```

## 🚀 Quick Start

### Prerequisites
```bash
pip install -r requirements.txt
```

### Reproduce All Figures
```bash
cd infinity-research-paper

# Generate all figures (2, 3, 4, 5, 6)
python scripts/generate_cost_chart.py      # Figure 2
python scripts/generate_token_chart.py     # Figure 3  
python scripts/generate_time_chart.py      # Figure 4
python scripts/generate_figure5_chart.py   # Figure 5
python scripts/generate_figure6_chart.py   # Figure 6
```

### Reproduce All Tables
```bash
# Generate all tables (4.5, 4.6, 4.7, 4.8)
python scripts/generate_concordance_table.py      # Table 4.5
python scripts/generate_field_analysis_table.py   # Table 4.6
python scripts/generate_conflicts_table_simple.py # Table 4.7
python scripts/generate_accuracy_table_real.py    # Table 4.8
```

## 📊 Generated Figures

| Script | Figure | Description | Key Metrics |
|--------|--------|-------------|-------------|
| `generate_cost_chart.py` | **Figure 2** | Cost Distribution | $0.833 total, 29.98% Vision, 58.03% Topics |
| `generate_token_chart.py` | **Figure 3** | Token Consumption | 540K tokens, 13.04% Vision, 54.33% Consensus |
| `generate_time_chart.py` | **Figure 4** | Processing Time | 45.5 min total, 17.93% Vision, 53.85% APIs |
| `generate_figure5_chart.py` | **Figure 5** | Vision vs Consensus Performance | 87.1% → 94.3% (+7.2% improvement) |
| `generate_figure6_chart.py` | **Figure 6** | API Specialization Matrix | 159 Vision, 138 Europe PMC, 124 CrossRef |

### Output Files (Figures)
Each figure script generates:
- **Chart**: `plots/figureX_chart.png`
- **Legend**: `plots/figureX_legend.txt`

## 📋 Generated Tables

| Script | Table | Description | Key Metrics |
|--------|-------|-------------|-------------|
| `generate_concordance_table.py` | **Table 4.5** | Concordance Performance | Claude: 83.6% vs DeepSeek: 91.4% general concordance |
| `generate_field_analysis_table.py` | **Table 4.6** | Field-by-Field Analysis | Author: 100% concordance, Year: 63.2-68.4% |
| `generate_conflicts_table_simple.py` | **Table 4.7** | Manual Resolution of Conflicts | 27 total conflicts, Infinity: 41%, Manual: 30% |
| `generate_accuracy_table_real.py` | **Table 4.8** | Real Accuracy Performance | 94.7% overall Infinity accuracy (144/152 fields) |

### Output Files (Tables)
Each table script generates:
- **Table**: `plots/table_name.txt`

## 🔬 Data Sources

### Article Processing Pipeline
1. **Vision JSON** (`vision_json.json`): Claude 3.5 Sonnet baseline extraction
2. **APIs Raw JSON** (`apis_raw_json.json`): Raw responses from 11 scholarly APIs
3. **APIs Clean JSON** (`apis_clean_json.json`): Consensus results with field_sources tracking
4. **LLM Topics JSON** (`llm_topics_json.json`): DeepSeek V3 topic classification  
5. **Final JSON** (`final_json.json`): Consolidated platform results with cost/time tracking

### Field Sources Tracking
- **`|` (pipe)**: Multi-source validation (e.g., `crossref|openalex`)
- **`+` (plus)**: Complementary data merging (e.g., `vision+europe_pmc`)
- **Single**: Single-source extraction (e.g., `vision`)

### Manual Analysis Data
- **`analysis_claude.json`**: evaluation of Claude 3.5 Sonnet extractions (152 field comparisons)
- **`analysis_deepseek.json`**: evaluation of DeepSeek V3 extractions (152 field comparisons)
- **`conflicts.json`**: Detailed analysis of 27 unique conflicts with resolution outcomes

## ✅ Validation

All scripts reproduce the **exact numbers** reported in the article:

### Figures
- ✅ **$0.833** total cost with 29.98% Vision contribution
- ✅ **540K tokens** with 54.33% Consensus consumption
- ✅ **45.5 minutes** total time with 53.85% APIs processing
- ✅ **87.1% → 94.3%** Vision to Consensus improvement (+7.2%)
- ✅ **273/304** field combinations populated in API matrix
- ✅ **159 Vision instances** (58.2% primary contributor)

### Tables
- ✅ **83.6% vs 91.4%** general concordance (Claude vs DeepSeek)
- ✅ **100% Author concordance** for both models
- ✅ **27 total conflicts** with detailed resolution analysis
- ✅ **62.6% multi-source validation** across API ecosystem

## 🔧 Technical Details

### Data Processing
- **Data Format**: Standard JSON with nested cost_tracking and processing_time_ms
- **Extraction Logic**: Mirrors core platform database queries exactly
- **Field Mapping**: Consistent field names across all processing stages

### Visualization
- **Charts**: Matplotlib + Seaborn with official platform styling
- **Heatmaps**: Custom colormaps with dynamic sizing
- **Tables**: Formatted text output matching article presentation

### Dependencies
- **Python 3.8+** with matplotlib, seaborn, numpy
- **No database connection required** - uses extracted JSONs only
- **Self-contained**: All dependencies specified in requirements.txt

## 📈 Reproducibility Features

This repository ensures **complete scientific reproducibility** by:

1. **Raw Data**: All 19 articles with complete modular JSONs (95 files total)
2. **Exact Scripts**: Mirror platform's chart generation and analysis logic  
3. **Verified Numbers**: All figures and tables match article values precisely
4. **Independence**: Self-contained with no external dependencies
5. **Documentation**: Comprehensive analysis files with 152 manual evaluations
6. **Conflict Resolution**: Detailed analysis of 27 conflicts with resolution outcomes

## 🧪 Scientific Validation

### Concordance Analysis
- **152 field comparisons** across 19 articles and 8 scientific fields
- **Six-level classification** (A: Equivalent, B: Concordant with Detail, C: Concordant with gaps, D: Factually Divergent, E: Conceptually Different, F: Incomparable)
- **Dual-model evaluation** comparing Claude 3.5 Sonnet vs DeepSeek V3

### Conflict Resolution
- **27 unique conflicts** identified and manually resolved
- **Temporal metadata precision**: Infinity achieved 6/7 correct resolutions
- **Protocol study handling**: Manual demonstrated appropriate conservative behavior
- **Complementarity patterns**: 67% of conceptual conflicts showed valid different perspectives

### API Ecosystem Analysis
- **11 scholarly APIs** with specialization patterns documented
- **16 metadata fields** across 304 theoretical combinations
- **Multi-source validation**: 62.6% of fields achieved cross-API verification
- **Domain expertise**: Europe PMC (100% PMID), CrossRef (94.7% DOI), Semantic Scholar (78.9% citations)

---

**Article**: "Infinity Research: A Modular and Transparent AI Platform for Automated Systematic Reviews"   
**Dataset**: 19 articles from "Comparison" project  
**Platform**: Infinity Research (https://infinityresearch-09sw.onrender.com/))

*This repository demonstrates the platform's transparency and reproducibility principles by making all data, scripts, and analysis methods publicly available.*
