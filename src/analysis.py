from pathlib import Path
import pandas as pd
import numpy as np
import statsmodels.api as sm

INPUT_PATH = Path("data/clean/afl_matches_with_streaks.csv")

def main():
    print("Loading data...")
    df = pd.read_csv(INPUT_PATH, parse_dates=["match_date"])

    # Log attendance
    df["log_attendance"] = np.log(df["attendance"])

    # -------------------------
    # SIMPLE REGRESSION
    # -------------------------
    print("\nRunning simple regression...")

    X = df[["max_pre_streak"]]
    X = sm.add_constant(X)  # adds intercept
    y = df["log_attendance"]

    model = sm.OLS(y, X).fit()

    print(model.summary())


if __name__ == "__main__":
    main()