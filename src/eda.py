from pathlib import Path
import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.formula.api as smf

warnings.filterwarnings("ignore")
pd.set_option("display.max_columns", 200)
pd.set_option("display.width", 140)
pd.set_option("display.float_format", lambda x: f"{x:,.3f}")

sns.set_theme(style="whitegrid")


def find_repo_root() -> Path:
    """
    Try to identify the repo root whether the script is run from the root,
    from src/, or from another working directory.
    """
    cwd = Path.cwd().resolve()
    candidates = [
        cwd,
        cwd.parent,
        Path(__file__).resolve().parent.parent,
        Path(__file__).resolve().parent,
    ]
    for path in candidates:
        if (path / "data" / "clean" / "afl_matches_with_streaks.csv").exists():
            return path
    raise FileNotFoundError(
        "Could not find data/clean/afl_matches_with_streaks.csv from the repo root. "
        "Run this script from inside your ECC3479 project folder."
    )


def choose_output_dir(repo_root: Path) -> Path:
    """
    Use output/eda if present or create it. If your repo already uses outputs/,
    the function falls back to that directory instead.
    """
    if (repo_root / "outputs").exists() and not (repo_root / "output").exists():
        out_dir = repo_root / "outputs" / "eda"
    else:
        out_dir = repo_root / "output" / "eda"
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir


def save_fig(fig, out_dir: Path, name: str) -> None:
    fig.savefig(out_dir / name, dpi=300, bbox_inches="tight")


def add_log_attendance(df: pd.DataFrame) -> pd.DataFrame:
    if "log_attendance" not in df.columns and "attendance" in df.columns:
        df["log_attendance"] = np.where(df["attendance"] > 0, np.log(df["attendance"]), np.nan)
    return df


def standardise_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )
    return df


def main() -> None:
    repo_root = find_repo_root()
    data_path = repo_root / "data" / "clean" / "afl_matches_with_streaks.csv"
    out_dir = choose_output_dir(repo_root)

    df = pd.read_csv(data_path)
    df = standardise_columns(df)

    if "match_date" in df.columns:
        df["match_date"] = pd.to_datetime(df["match_date"], errors="coerce")

    numeric_candidates = [
        "attendance", "max_pre_streak", "margin", "season", "is_finals"
    ]
    for col in numeric_candidates:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df = add_log_attendance(df)

    keep_cols = [c for c in ["attendance", "max_pre_streak"] if c in df.columns]
    analysis_df = df.dropna(subset=keep_cols).copy()

    print(f"Loaded data from: {data_path}")
    print(f"Output directory: {out_dir}")
    print(f"Original rows: {len(df):,}")
    print(f"EDA rows: {len(analysis_df):,}\n")

    # ------------------------------------------------------------------
    # Exhibit A: variable overview and missingness
    # ------------------------------------------------------------------
    overview = pd.DataFrame({
        "column": df.columns,
        "dtype": df.dtypes.astype(str).values,
        "missing_n": df.isna().sum().values,
        "missing_pct": (df.isna().mean() * 100).values,
    }).sort_values(["missing_pct", "column"], ascending=[False, True])
    overview.to_csv(out_dir / "exhibit_a_variable_overview.csv", index=False)

    # ------------------------------------------------------------------
    # Exhibit B: summary statistics
    # ------------------------------------------------------------------
    summary_cols = [
        c for c in ["attendance", "log_attendance", "max_pre_streak", "margin", "season"]
        if c in analysis_df.columns
    ]
    if summary_cols:
        analysis_df[summary_cols].describe().T.to_csv(out_dir / "exhibit_b_summary_statistics.csv")

    # ------------------------------------------------------------------
    # Exhibit C: correlations
    # ------------------------------------------------------------------
    corr_rows = []
    for y in [c for c in ["attendance", "log_attendance"] if c in analysis_df.columns]:
        subset = analysis_df[["max_pre_streak", y]].dropna()
        if len(subset) > 1:
            corr_rows.append({
                "outcome": y,
                "pearson_corr": subset["max_pre_streak"].corr(subset[y], method="pearson"),
                "spearman_corr": subset["max_pre_streak"].corr(subset[y], method="spearman"),
                "n": len(subset),
            })
    if corr_rows:
        pd.DataFrame(corr_rows).to_csv(out_dir / "exhibit_c_correlations.csv", index=False)

    # ------------------------------------------------------------------
    # Exhibit 1: distribution of attendance
    # ------------------------------------------------------------------
    if "attendance" in analysis_df.columns:
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        sns.histplot(analysis_df["attendance"].dropna(), bins=30, ax=axes[0])
        axes[0].set_title("Exhibit 1. Distribution of attendance")
        axes[0].set_xlabel("Attendance")
        sns.boxplot(x=analysis_df["attendance"].dropna(), ax=axes[1])
        axes[1].set_title("Exhibit 2. Box plot of attendance")
        axes[1].set_xlabel("Attendance")
        plt.tight_layout()
        save_fig(fig, out_dir, "exhibit_1_2_attendance_distribution.png")
        plt.close(fig)

    # ------------------------------------------------------------------
    # Exhibit 3: distribution of log attendance
    # ------------------------------------------------------------------
    if "log_attendance" in analysis_df.columns:
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.histplot(analysis_df["log_attendance"].dropna(), bins=30, ax=ax)
        ax.set_title("Exhibit 3. Distribution of log attendance")
        ax.set_xlabel("Log attendance")
        plt.tight_layout()
        save_fig(fig, out_dir, "exhibit_3_log_attendance_distribution.png")
        plt.close(fig)

    # ------------------------------------------------------------------
    # Exhibit 4: distribution of winning streaks
    # ------------------------------------------------------------------
    if "max_pre_streak" in analysis_df.columns:
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.histplot(analysis_df["max_pre_streak"].dropna(), discrete=True, ax=ax)
        ax.set_title("Exhibit 4. Distribution of pre-match winning streaks")
        ax.set_xlabel("Max pre-match winning streak")
        plt.tight_layout()
        save_fig(fig, out_dir, "exhibit_4_streak_distribution.png")
        plt.close(fig)

    # ------------------------------------------------------------------
    # Exhibit 5: attendance over time
    # ------------------------------------------------------------------
    if {"season", "attendance"}.issubset(analysis_df.columns):
        season_att = (
            analysis_df.groupby("season", as_index=False)["attendance"]
            .mean()
            .rename(columns={"attendance": "mean_attendance"})
        )
        season_att.to_csv(out_dir / "exhibit_5_mean_attendance_by_season.csv", index=False)

        fig, ax = plt.subplots(figsize=(9, 5))
        sns.lineplot(data=season_att, x="season", y="mean_attendance", marker="o", ax=ax)
        ax.set_title("Exhibit 5. Mean attendance by season")
        ax.set_xlabel("Season")
        ax.set_ylabel("Mean attendance")
        plt.tight_layout()
        save_fig(fig, out_dir, "exhibit_5_mean_attendance_by_season.png")
        plt.close(fig)

    # ------------------------------------------------------------------
    # Exhibit 6: finals vs regular season
    # ------------------------------------------------------------------
    if {"is_finals", "attendance"}.issubset(analysis_df.columns):
        finals_summary = (
            analysis_df.groupby("is_finals")["attendance"]
            .agg(["count", "mean", "median"])
            .reset_index()
        )
        finals_summary.to_csv(out_dir / "exhibit_6_attendance_by_finals_status.csv", index=False)

        fig, ax = plt.subplots(figsize=(8, 5))
        sns.boxplot(data=analysis_df, x="is_finals", y="attendance", ax=ax)
        ax.set_title("Exhibit 6. Attendance by finals status")
        ax.set_xlabel("Is finals")
        ax.set_ylabel("Attendance")
        plt.tight_layout()
        save_fig(fig, out_dir, "exhibit_6_attendance_by_finals_status.png")
        plt.close(fig)

    # ------------------------------------------------------------------
    # Exhibit 7: venue heterogeneity
    # ------------------------------------------------------------------
    if {"venue", "attendance"}.issubset(analysis_df.columns):
        top_venues = analysis_df["venue"].value_counts().head(10).index
        venue_df = analysis_df[analysis_df["venue"].isin(top_venues)].copy()

        venue_summary = (
            venue_df.groupby("venue")["attendance"]
            .agg(["count", "mean", "median"])
            .sort_values("mean", ascending=False)
            .reset_index()
        )
        venue_summary.to_csv(out_dir / "exhibit_7_top_venue_attendance.csv", index=False)

        fig, ax = plt.subplots(figsize=(11, 6))
        sns.boxplot(data=venue_df, x="venue", y="attendance", ax=ax)
        ax.set_title("Exhibit 7. Attendance by major venue")
        ax.set_xlabel("Venue")
        ax.set_ylabel("Attendance")
        ax.tick_params(axis="x", rotation=45)
        plt.tight_layout()
        save_fig(fig, out_dir, "exhibit_7_attendance_by_major_venue.png")
        plt.close(fig)

    # ------------------------------------------------------------------
    # Exhibit 8 and 9: streak vs attendance
    # ------------------------------------------------------------------
    if {"max_pre_streak", "attendance"}.issubset(analysis_df.columns):
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.regplot(
            data=analysis_df,
            x="max_pre_streak",
            y="attendance",
            scatter_kws={"alpha": 0.4},
            line_kws={"linewidth": 2},
            ax=ax,
        )
        ax.set_title("Exhibit 8. Attendance and winning streak")
        ax.set_xlabel("Max pre-match winning streak")
        ax.set_ylabel("Attendance")
        plt.tight_layout()
        save_fig(fig, out_dir, "exhibit_8_attendance_vs_streak.png")
        plt.close(fig)

    if {"max_pre_streak", "log_attendance"}.issubset(analysis_df.columns):
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.regplot(
            data=analysis_df,
            x="max_pre_streak",
            y="log_attendance",
            scatter_kws={"alpha": 0.4},
            line_kws={"linewidth": 2},
            ax=ax,
        )
        ax.set_title("Exhibit 9. Log attendance and winning streak")
        ax.set_xlabel("Max pre-match winning streak")
        ax.set_ylabel("Log attendance")
        plt.tight_layout()
        save_fig(fig, out_dir, "exhibit_9_log_attendance_vs_streak.png")
        plt.close(fig)

    # ------------------------------------------------------------------
    # Exhibit 10: mean and median attendance by streak
    # ------------------------------------------------------------------
    if {"max_pre_streak", "attendance"}.issubset(analysis_df.columns):
        streak_summary = (
            analysis_df.groupby("max_pre_streak")["attendance"]
            .agg(["count", "mean", "median"])
            .reset_index()
            .sort_values("max_pre_streak")
        )
        streak_summary.to_csv(out_dir / "exhibit_10_attendance_by_streak.csv", index=False)

        fig, ax = plt.subplots(figsize=(9, 5))
        sns.lineplot(data=streak_summary, x="max_pre_streak", y="mean", marker="o", label="Mean", ax=ax)
        sns.lineplot(data=streak_summary, x="max_pre_streak", y="median", marker="o", label="Median", ax=ax)
        ax.set_title("Exhibit 10. Mean and median attendance by winning streak")
        ax.set_xlabel("Max pre-match winning streak")
        ax.set_ylabel("Attendance")
        plt.tight_layout()
        save_fig(fig, out_dir, "exhibit_10_mean_median_attendance_by_streak.png")
        plt.close(fig)

    # ------------------------------------------------------------------
    # Exhibit 11: pooled relationship split by finals status
    # ------------------------------------------------------------------
    if {"max_pre_streak", "attendance", "is_finals"}.issubset(analysis_df.columns):
        fig, ax = plt.subplots(figsize=(9, 5))
        sns.scatterplot(
            data=analysis_df,
            x="max_pre_streak",
            y="attendance",
            hue="is_finals",
            alpha=0.4,
            ax=ax,
        )
        ax.set_title("Exhibit 11. Attendance and streak by finals status")
        ax.set_xlabel("Max pre-match winning streak")
        ax.set_ylabel("Attendance")
        plt.tight_layout()
        save_fig(fig, out_dir, "exhibit_11_streak_by_finals_status.png")
        plt.close(fig)

    # ------------------------------------------------------------------
    # Exhibit 12: within-season partial relationship
    # ------------------------------------------------------------------
    if {"season", "attendance", "max_pre_streak"}.issubset(analysis_df.columns):
        model = smf.ols("np.log(attendance) ~ max_pre_streak + C(season)", data=analysis_df[analysis_df["attendance"] > 0]).fit()
        coef_table = pd.DataFrame({
            "term": model.params.index,
            "coef": model.params.values,
            "std_err": model.bse.values,
            "p_value": model.pvalues.values,
        })
        coef_table.to_csv(out_dir / "exhibit_12_within_season_log_attendance_regression.csv", index=False)

    print("EDA exhibits saved successfully.")


if __name__ == "__main__":
    main()
