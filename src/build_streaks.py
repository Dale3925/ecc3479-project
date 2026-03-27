from __future__ import annotations

from pathlib import Path

import pandas as pd

INPUT_PATH = Path("data/raw/afl_matches_raw.csv")
OUTPUT_PATH = Path("data/clean/afl_matches_with_streaks.csv")


def load_data(path: Path) -> pd.DataFrame:
    """Load raw AFL match data."""
    df = pd.read_csv(path, parse_dates=["match_date"])

    required_columns = [
        "match_id",
        "season",
        "round",
        "match_date",
        "day_of_week",
        "team1",
        "team2",
        "team1_score",
        "team2_score",
        "winner",
        "margin",
        "attendance",
        "venue",
        "is_finals",
    ]

    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    return df


def build_streaks(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build season-reset pre-match winning streak variables.

    team1_pre_streak = number of consecutive wins team1 had BEFORE this match
                        within the current season only
    team2_pre_streak = number of consecutive wins team2 had BEFORE this match
                        within the current season only
    """
    df = df.copy()

    df["match_date"] = pd.to_datetime(df["match_date"])
    df["is_finals"] = df["is_finals"].astype(bool)

    # Sort into chronological order within season
    df = df.sort_values(["season", "match_date", "match_id"]).reset_index(drop=True)

    team1_pre_streaks = []
    team2_pre_streaks = []

    current_season = None
    current_streaks: dict[str, int] = {}

    for _, row in df.iterrows():
        season = row["season"]
        team1 = row["team1"]
        team2 = row["team2"]
        winner = row["winner"]

        # Reset streak tracker when new season starts
        if current_season != season:
            current_streaks = {}
            current_season = season

        # Record pre-match streaks
        team1_pre = current_streaks.get(team1, 0)
        team2_pre = current_streaks.get(team2, 0)

        team1_pre_streaks.append(team1_pre)
        team2_pre_streaks.append(team2_pre)

        # Update streaks after the match
        if winner == "Draw":
            current_streaks[team1] = 0
            current_streaks[team2] = 0
        elif winner == team1:
            current_streaks[team1] = team1_pre + 1
            current_streaks[team2] = 0
        elif winner == team2:
            current_streaks[team2] = team2_pre + 1
            current_streaks[team1] = 0
        else:
            raise ValueError(
                f"Winner '{winner}' does not match team1 '{team1}' or team2 '{team2}' "
                f"for match_id '{row['match_id']}'"
            )

    df["team1_pre_streak"] = team1_pre_streaks
    df["team2_pre_streak"] = team2_pre_streaks

    # Useful derived variables
    df["max_pre_streak"] = df[["team1_pre_streak", "team2_pre_streak"]].max(axis=1)
    df["min_pre_streak"] = df[["team1_pre_streak", "team2_pre_streak"]].min(axis=1)
    df["streak_diff"] = df["team1_pre_streak"] - df["team2_pre_streak"]

    df["team1_higher_streak"] = (df["team1_pre_streak"] > df["team2_pre_streak"]).astype(int)
    df["team2_higher_streak"] = (df["team2_pre_streak"] > df["team1_pre_streak"]).astype(int)
    df["equal_pre_streak"] = (df["team1_pre_streak"] == df["team2_pre_streak"]).astype(int)

    return df


def main() -> None:
    print("Loading raw match data...")
    df = load_data(INPUT_PATH)

    print("Building season-reset pre-match winning streak variables...")
    df_out = build_streaks(df)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df_out.to_csv(OUTPUT_PATH, index=False)

    print("\nDone.")
    print(f"Saved to: {OUTPUT_PATH}")
    print(f"Rows: {len(df_out):,}")
    print("\nAdded columns:")
    print(
        [
            "team1_pre_streak",
            "team2_pre_streak",
            "max_pre_streak",
            "min_pre_streak",
            "streak_diff",
            "team1_higher_streak",
            "team2_higher_streak",
            "equal_pre_streak",
        ]
    )
    print("\nPreview:")
    print(
        df_out[
            [
                "season",
                "match_date",
                "team1",
                "team2",
                "winner",
                "team1_pre_streak",
                "team2_pre_streak",
                "max_pre_streak",
                "attendance",
            ]
        ].head(15).to_string(index=False)
    )


if __name__ == "__main__":
    main()