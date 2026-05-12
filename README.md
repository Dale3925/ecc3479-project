# Do Team Winning Streaks Increase AFL Match Attendance?

## Overview

This project investigates whether team winning streaks are associated with AFL match attendance. Using AFL match-level data from 2000 to 2024, the project constructs pre-match winning streak variables, performs exploratory data analysis, and estimates primary econometric models of attendance.

This project's primary analysis is **descriptive rather than causal**. The regression results should be interpreted as conditional associations, not as causal treatment effects.

## Research question

**Do team winning streaks increase AFL match attendance?**

## Claim type

This is a descriptive analysis, not a causal design. The estimates should be interpreted as conditional correlations, not proof that winning streaks cause higher attendance.

## Repository structure

```
ecc3479-project/
├── data/
│   ├── raw/
│   │   └── afl_matches_raw.csv
│   └── clean/
│       ├── afl_matches_with_streaks.csv
│       └── codebook.md
├── src/
│   ├── collect_afl_data.py
│   ├── build_streaks.py
│   ├── eda.py
│   ├── primary_analysis.py
│   ├── robustness_analysis.py
│   ├── analysis.py
│   └── analysis_checks.py
├── notebooks/
│   └── eda_afl_attendance.ipynb
├── docs/
│   ├── eda_report.md
│   ├── primary_analysis_report.md
│   └── robustness_checks.md
├── outputs/
│   ├── eda/
│   ├── primary_analysis/
│   └── robustness/
├── requirements.txt
└── README.md
```

## Data

- `data/raw/afl_matches_raw.csv`: Raw AFL match-level data collected by the scraping pipeline
- `data/clean/afl_matches_with_streaks.csv`: Cleaned analysis-ready dataset with constructed winning streak variables
- `data/clean/codebook.md`: Variable definitions for the cleaned dataset

## Code

- `src/collect_afl_data.py`: Collects raw AFL match data
- `src/build_streaks.py`: Cleans the raw data and constructs streak variables
- `src/eda.py`: Runs the exploratory data analysis and saves figures/tables to `outputs/eda/`
- `src/primary_analysis.py`: Runs the primary econometric analysis and saves outputs to `outputs/primary_analysis/`
- `src/robustness_analysis.py`: Runs the robustness checks and saves outputs to `outputs/robustness/`
- `src/analysis.py`: Earlier analysis script retained in the repository
- `src/analysis_checks.py`: Optional sanity checks

## Software information

This project uses Python 3.10+ and the packages listed in `requirements.txt`.

Main packages used:

- pandas
- numpy
- requests
- beautifulsoup4
- statsmodels
- matplotlib
- seaborn

## How to run the project from scratch

### 1. Clone the repository

```
git clone https://github.com/Dale3925/ecc3479-project.git
cd ecc3479-project
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

### 3. Run the full pipeline

Run the scripts in the following order:

```
python src/collect_afl_data.py
python src/build_streaks.py
python src/eda.py
python src/primary_analysis.py
python src/robustness_analysis.py
```

### 4. Optional checks

Optional sanity checks can also be run with:

```
python src/analysis_checks.py
```

## Manual steps outside the code

No manual editing should be performed on raw data files. All cleaning, variable construction, EDA, and regression analysis are intended to be reproducible through the scripts above. If data collection fails because of a temporary source or connection issue, rerun `python src/collect_afl_data.py`.

## Main outputs

After running the pipeline, the main outputs are:

- Raw dataset: `data/raw/afl_matches_raw.csv`
- Clean dataset: `data/clean/afl_matches_with_streaks.csv`
- EDA outputs: `outputs/eda/`
- Primary analysis outputs: `outputs/primary_analysis/`
- Robustness analysis outputs: `outputs/robustness/`

## EDA deliverable

- Written EDA discussion: `docs/eda_report.md`
- Reproducible EDA code: `src/eda.py`
- Optional notebook version: `notebooks/eda_afl_attendance.ipynb`
- Generated EDA figures and tables: `outputs/eda/`

## Primary analysis deliverable

- Primary analysis code: `src/primary_analysis.py`
- Written primary analysis discussion: `docs/primary_analysis_report.md`
- Regression tables, summaries, and figures: `outputs/primary_analysis/`

## Robustness analysis deliverable

- Robustness analysis code: `src/robustness_analysis.py`
- Written robustness discussion: `docs/robustness_checks.md`
- Robustness tables, summaries, notes, and figures: `outputs/robustness/`

## Main finding

In the preferred primary analysis specification, each additional game in the match's maximum pre-match winning streak is associated with approximately a 2.7 per cent higher attendance, holding finals status, match margin, season, and venue constant. This is a descriptive conditional association, not a causal estimate.

## Reproducibility note

This repository is intended to be fully reproducible. Following the steps in this README should allow the marker to obtain the cleaned dataset and reproduce the EDA, primary econometric analysis, and robustness checks from scratch.