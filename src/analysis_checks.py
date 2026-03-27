from __future__ import annotations

from pathlib import Path

import pandas as pd

INPUT_PATH = Path("data/clean/afl_matches_with_streaks.csv")


def main() -> None:
    print("Loading data...")
    df = pd.read_csv(INPUT_PATH, parse_dates=["match_date"])

    print("\nBasic info")
    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")

    print("\nColumn names:")
    print(df.columns.tolist())

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nSummary of streak variables:")
    streak_cols = [
        "team1_pre_streak",
        "team2_pre_streak",
        "max_pre_streak",
        "min_pre_streak",
        "streak_diff",
    ]
    print(df[streak_cols].describe())

    print("\nFirst 10 matches of each season: streaks should usually start at 0")
    preview = (
        df.sort_values(["season", "match_date", "match_id"])
          .groupby("season")
          .head(10)[
              [
                  "season",
                  "match_date",
                  "team1",
                  "team2",
                  "winner",
                  "team1_pre_streak",
                  "team2_pre_streak",
              ]
          ]
    )
    print(preview.to_string(index=False))

    print("\nTop 20 matches with the largest pre-match streaks:")
    top_streaks = (
        df.sort_values(["max_pre_streak", "season", "match_date"], ascending=[False, True, True])[
            [
                "season",
                "round",
                "match_date",
                "team1",
                "team2",
                "winner",
                "team1_pre_streak",
                "team2_pre_streak",
                "max_pre_streak",
                "attendance",
            ]
        ]
        .head(20)
    )
    print(top_streaks.to_string(index=False))

    print("\nAverage attendance by max pre-match streak:")
    avg_attendance = (
        df.groupby("max_pre_streak", dropna=False)["attendance"]
        .agg(["count", "mean"])
        .reset_index()
        .sort_values("max_pre_streak")
    )
    print(avg_attendance.to_string(index=False))

    print("\nAverage attendance by finals status:")
    finals_summary = (
        df.groupby("is_finals")["attendance"]
        .agg(["count", "mean", "median"])
        .reset_index()
    )
    print(finals_summary.to_string(index=False))

    print("\nAverage attendance by day of week:")
    day_summary = (
        df.groupby("day_of_week")["attendance"]
        .agg(["count", "mean"])
        .reset_index()
    )
    print(day_summary.to_string(index=False))

    print("\nDone.")


if __name__ == "__main__":
    main()
    