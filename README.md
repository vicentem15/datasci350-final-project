# DATASCI 350 Final Project
Vicente Martinez, Theo Burns, Saahil Mardhekar, Arush Singhania

## Overview
World Bank World Development Indicators analysis project for DATASCI 350.

## View the Report
📊 **[View the interactive HTML report](https://vicentem15.github.io/datasci350-final-project/report.html)**

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd datasci350-final-project
```

### 2. Create Virtual Environment
```bash
chmod +x setup.sh
./setup.sh
```

Or manually:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Render the Report
```bash
source venv/bin/activate
quarto render report.qmd
```

This generates:
- `report.html` - Interactive HTML version
- `report.pdf` - PDF version

## Requirements
- Python 3.13+
- Quarto (https://quarto.org/docs/get-started/)
- Dependencies listed in `requirements.txt`

## Running the Analysis
All analysis code is embedded in the Quarto report (`report.qmd`). The code cells are displayed in the rendered reports for transparency and reproducibility.

## Project Structure

```
datasci350-final-project/
├── README.md                           # Project documentation
├── requirements.txt                    # Python dependencies
├── setup.sh                           # Environment setup script
├── render.sh                          # Report rendering script
├── _quarto.yml                        # Quarto configuration
├── report.qmd                         # Main analysis report (Quarto)
├── report.html                        # Rendered HTML report
├── report.pdf                         # Rendered PDF report
├── index.html                         # GitHub Pages entry point
│
├── data/                              # Data files (gitignored)
│   └── ...
│
├── scripts/                           # Python analysis scripts
│   ├── edu_analysis.ipynb            # Analysis notebook
│   ├── join_data.py                  # Data joining script
│   └── clean_joined_data.py          # Data cleaning script
│
├── figures/                           # Generated figures
│   ├── primary_trend.png
│   ├── secondary_trend.png
│   ├── tertiary_trend.png
│   └── boxplot_enrollment.png
│
├── documentation/                     # Project documentation
│   ├── CODEBOOK.md                   # Data dictionary
│   └── ENTITY_RELATIONSHIP_DIAGRAM.md # ER diagram
│
├── report_files/                      # Quarto output dependencies
│   ├── figure-html/                  # Rendered figures
│   └── libs/                         # CSS and JavaScript libraries
│
└── venv/                             # Python virtual environment (gitignored)