# Do Team Winning Streaks Increase AFL Match Attendance?

## Overview

This project investigates whether team winning streaks are associated with AFL match attendance. Using AFL match-level data from 2000 to 2024, the project constructs pre-match winning streak variables, performs exploratory data analysis, and estimates primary econometric models of attendance.

This project’s primary analysis is **descriptive rather than causal**. The regression results should be interpreted as conditional associations, not as causal treatment effects.

## Research question

**Do team winning streaks increase AFL match attendance?**

## Repository structure

```text
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
│   ├── analysis.py
│   └── analysis_checks.py
├── notebooks/
│   └── eda_afl_attendance.ipynb
├── docs/
│   ├── eda_report.md
│   └── primary_analysis_report.md
├── outputs/
│   ├── eda/
│   └── primary_analysis/
├── requirements.txt
└── README.md

Data
data/raw/
afl_matches_raw.csv: raw AFL match-level data collected by the scraping pipeline
data/clean/
afl_matches_with_streaks.csv: cleaned analysis-ready dataset with constructed winning streak variables
codebook.md: variable definitions for the cleaned dataset
Code
src/
collect_afl_data.py: collects raw AFL match data
build_streaks.py: cleans the raw data and constructs streak variables
eda.py: runs the exploratory data analysis and saves figures/tables to outputs/eda/
primary_analysis.py: runs the primary econometric analysis and saves outputs to outputs/primary_analysis/
analysis.py: earlier analysis script retained in the repository
analysis_checks.py: optional sanity checks
Software information

This project uses Python 3.10+ and the packages listed in requirements.txt.

Main packages used:

pandas
numpy
requests
beautifulsoup4
statsmodels
matplotlib
seaborn
How to run the project from scratch
1. Clone the repository
git clone https://github.com/Dale3925/ecc3479-project.git
cd ecc3479-project
2. Install dependencies
pip install -r requirements.txt
3. Run the full pipeline

Run the scripts in the following order:

python src/collect_afl_data.py
python src/build_streaks.py
python src/eda.py
python src/primary_analysis.py

Optional sanity checks can also be run with:

python src/analysis_checks.py
Manual steps outside the code
No manual editing should be performed on raw data files.
All cleaning, variable construction, EDA, and regression analysis are intended to be reproducible through the scripts above.
If data collection fails because of a temporary source or connection issue, rerun python src/collect_afl_data.py.
Main outputs

After running the pipeline, the main outputs are:

Raw dataset: data/raw/afl_matches_raw.csv
Clean dataset: data/clean/afl_matches_with_streaks.csv
EDA outputs: outputs/eda/
Primary analysis outputs: outputs/primary_analysis/
EDA deliverable
Written EDA discussion: docs/eda_report.md
Reproducible EDA code: src/eda.py
Optional notebook version: notebooks/eda_afl_attendance.ipynb
Generated EDA figures and tables: outputs/eda/
Primary analysis deliverable
Primary analysis code: src/primary_analysis.py
Written primary analysis discussion: docs/primary_analysis_report.md
Regression tables, summaries, and figures: outputs/primary_analysis/

This primary analysis is descriptive rather than causal and estimates conditional associations between pre-match winning streaks and AFL match attendance.

Main finding

In the preferred primary analysis specification, each additional game in the match’s maximum pre-match winning streak is associated with approximately a 2.7 per cent increase in attendance, holding finals status, match margin, season, and venue constant.

This is a descriptive result and should not be interpreted as a causal effect.

Reproducibility note

This repository is intended to be fully reproducible. Following the steps in this README should allow the marker to obtain the cleaned dataset and reproduce the EDA and primary econometric analysis from scratch.