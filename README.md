# Do Team Winning Streaks Increase AFL Match Attendance?

## Overview
This project investigates whether team winning streaks influence AFL match attendance. The central idea is that sustained on-field success may increase fan engagement, leading to higher crowd turnout.

Using match-level data from the AFL (2000–2024), the project constructs pre-match winning streak variables and applies econometric analysis to estimate their effect on attendance.

---

## Research Question
**Do team winning streaks increase AFL match attendance?**

---

## Methodology

### Data
The dataset consists of AFL match-level observations from 2000 to 2024, including:
- match date and round
- competing teams and scores
- match attendance
- venue and finals status

### Key Variable Construction
For each match, the project constructs **season-reset pre-match winning streaks**:
- `team1_pre_streak`
- `team2_pre_streak`

These measure the number of consecutive wins each team had *prior* to the match.

From these, additional variables are derived:
- `max_pre_streak` (strongest streak in the match)
- `streak_diff` (difference in team streaks)

### Transformation
Attendance is log-transformed:
- `log_attendance = log(attendance)`

This accounts for skewness and allows coefficients to be interpreted in percentage terms.

---

## Empirical Approach

The initial model estimates:

log(attendance) = β₀ + β₁ · max_pre_streak + ε

Where:
- Dependent variable: log attendance  
- Key independent variable: maximum pre-match winning streak  

---

## Initial Findings

- The coefficient on `max_pre_streak` is approximately **0.040**
- Interpretation:  
  > Each additional win in a streak is associated with roughly a **4% increase in attendance**
- The result is **statistically significant (p < 0.001)**

However:
- The model has low explanatory power (R² ≈ 0.02)
- Results are preliminary and do not yet control for confounding factors such as:
  - finals matches
  - scheduling effects (day of week)
  - team popularity
  - venue capacity

---

## Project Structure

```text
ecc3479-project/
│
├── data/
│   ├── raw/
│   │   └── afl_matches_raw.csv
│   └── clean/
│       └── afl_matches_with_streaks.csv
│
├── src/
│   ├── collect_afl_data.py      # scrape AFL match data
│   ├── build_streaks.py         # construct winning streak variables
│   ├── analysis_checks.py       # data validation and sanity checks
│   └── analysis.py              # regression analysis
│
├── outputs/
├── docs/
├── README.md
└── requirements.txt

## Project Structure

Follow these steps to run the project on a new machine.

1. Clone the repository
git clone https://github.com/Dale3925/ecc3479-project.git
cd ecc3479-project

2. Install Python dependencies

Ensure Python 3.10+ is installed, then run:

pip install -r requirements.txt

pandas
numpy
requests
beautifulsoup4
statsmodels

3. Run the project pipeline

Run the scripts in the following order:

python src/collect_afl_data.py
python src/build_streaks.py
python src/analysis.py

Optional sanity checks can also be run with:

python src/analysis_checks.py

4. Outputs

After running the pipeline, the main outputs are:

Raw dataset

data/raw/afl_matches_raw.csv

Clean dataset with streak variables

data/clean/afl_matches_with_streaks.csv

Regression results displayed in the terminal when running analysis.py