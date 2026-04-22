# DATASCI 350 Final Project

## Overview
World Bank World Development Indicators analysis project for DATASCI 350.

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