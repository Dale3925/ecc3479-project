from pathlib import Path
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

warnings.filterwarnings("ignore")

REQUIRED_COLUMNS = [
    "attendance",
    "max_pre_streak",
    "margin",
    "season",
    "is_finals",
    "venue",
]

MODEL_SPECIFICATIONS = {
    "Model 1": "log_attendance ~ max_pre_streak",
    "Model 2": "log_attendance ~ max_pre_streak + is_finals + margin + C(season)",
    "Model 3": "log_attendance ~ max_pre_streak + is_finals + margin + C(season) + C(venue)",
}


def find_repo_root() -> Path:
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
    out_dir = repo_root / "outputs" / "primary_analysis"
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir


def standardise_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )
    return df


def add_log_attendance(df: pd.DataFrame) -> pd.DataFrame:
    if "attendance" not in df.columns:
        return df
    df = df.copy()
    df["log_attendance"] = np.where(df["attendance"] > 0, np.log(df["attendance"]), np.nan)
    return df


def check_required_columns(df: pd.DataFrame) -> None:
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(
            "Missing required column(s) for primary analysis: "
            + ", ".join(missing)
        )


def parse_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "match_date" in df.columns:
        df["match_date"] = pd.to_datetime(df["match_date"], errors="coerce")

    numeric_candidates = ["attendance", "max_pre_streak", "margin", "season"]
    for col in numeric_candidates:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "is_finals" in df.columns:
        if df["is_finals"].dtype == object:
            df["is_finals"] = (
                df["is_finals"]
                .map({
                    "True": 1,
                    "true": 1,
                    "TRUE": 1,
                    "False": 0,
                    "false": 0,
                    "FALSE": 0,
                })
                .fillna(df["is_finals"])
            )
        df["is_finals"] = pd.to_numeric(df["is_finals"], errors="coerce")

    return df


def fit_model(formula: str, data: pd.DataFrame, required_columns: list[str]) -> tuple[smf.OLS, pd.DataFrame]:
    model_data = data.dropna(subset=required_columns).copy()
    model = smf.ols(formula=formula, data=model_data).fit(cov_type="HC3")
    return model, model_data


def format_coef(coef: float | int, se: float | int) -> str:
    return f"{coef:.3f}\n({se:.3f})"


def build_regression_tables(models: dict[str, smf.OLS]) -> pd.DataFrame:
    rows = ["max_pre_streak", "is_finals", "margin", "N", "R_squared", "Season_FE", "Venue_FE"]
    table = pd.DataFrame(index=rows, columns=models.keys(), dtype=object)

    for label, model in models.items():
        params = model.params
        bse = model.bse
        table.at["max_pre_streak", label] = (
            format_coef(params.get("max_pre_streak", np.nan), bse.get("max_pre_streak", np.nan))
            if "max_pre_streak" in params else "—"
        )
        table.at["is_finals", label] = (
            format_coef(params.get("is_finals", np.nan), bse.get("is_finals", np.nan))
            if "is_finals" in params else "—"
        )
        table.at["margin", label] = (
            format_coef(params.get("margin", np.nan), bse.get("margin", np.nan))
            if "margin" in params else "—"
        )
        table.at["N", label] = int(model.nobs)
        table.at["R_squared", label] = round(model.rsquared, 3)
        table.at["Season_FE", label] = "Yes" if "C(season)" in model.model.formula else "No"
        table.at["Venue_FE", label] = "Yes" if "C(venue)" in model.model.formula else "No"

    return table


def table_to_markdown(df: pd.DataFrame) -> str:
    header = ["Variable"] + df.columns.tolist()
    lines = ["| " + " | ".join(header) + " |", "|" + "|".join(["---"] * len(header)) + "|"]
    for row in df.index:
        cells = [row]
        for label in df.columns:
            cell = df.at[row, label]
            if pd.isna(cell) or cell == "" or cell == "—":
                cells.append("—")
            else:
                rendered = str(cell).replace("\n", "<br>")
                cells.append(rendered)
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def save_outputs(
    out_dir: Path,
    regression_table: pd.DataFrame,
    model_summaries: dict[str, dict],
    sample_summary: pd.DataFrame,
    coef_plot_path: Path,
    notes: str,
) -> None:
    regression_table.to_csv(out_dir / "regression_table_main.csv")
    md = table_to_markdown(regression_table)
    (out_dir / "regression_table_main.md").write_text(md, encoding="utf-8")

    summary_df = pd.DataFrame.from_records(
        [
            {
                "model_label": label,
                "formula": info["formula"],
                "n": info["n"],
                "r_squared": info["r_squared"],
                "coef_max_pre_streak": info["coef"],
                "se_max_pre_streak": info["se"],
                "p_value_max_pre_streak": info["p_value"],
            }
            for label, info in model_summaries.items()
        ]
    )
    summary_df.to_csv(out_dir / "model_summary.csv", index=False)
    sample_summary.to_csv(out_dir / "sample_summary_primary_analysis.csv")
    (out_dir / "primary_analysis_notes.txt").write_text(notes, encoding="utf-8")


def plot_coefficients(models: dict[str, smf.OLS], out_path: Path) -> None:
    labels = []
    estimates = []
    lower = []
    upper = []
    for label, model in models.items():
        coef = model.params["max_pre_streak"]
        se = model.bse["max_pre_streak"]
        ci = model.conf_int().loc["max_pre_streak"]
        labels.append(label)
        estimates.append(coef)
        lower.append(coef - 1.96 * se)
        upper.append(coef + 1.96 * se)

    fig, ax = plt.subplots(figsize=(7, 4))
    x = np.arange(len(labels))
    ax.errorbar(x, estimates, yerr=[np.array(estimates) - np.array(lower), np.array(upper) - np.array(estimates)], fmt="o", color="black", ecolor="grey", capsize=5)
    ax.axhline(0, color="black", linewidth=0.75, linestyle="--")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel("Coefficient on max_pre_streak")
    ax.set_title("Max pre-match winning streak coefficient")
    ax.grid(axis="y", linestyle=":", color="grey", alpha=0.6)
    fig.tight_layout()
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def build_notes(models: dict[str, smf.OLS]) -> str:
    lines = [
        "Primary analysis notes:",
    ]
    for label, model in models.items():
        coef = model.params["max_pre_streak"]
        se = model.bse["max_pre_streak"]
        pval = model.pvalues["max_pre_streak"]
        lines.append(
            f"{label}: max_pre_streak coefficient = {coef:.3f} (SE = {se:.3f}, p = {pval:.3f})."
        )
    return "\n".join(lines)


def main() -> None:
    repo_root = find_repo_root()
    data_path = repo_root / "data" / "clean" / "afl_matches_with_streaks.csv"
    out_dir = choose_output_dir(repo_root)

    df = pd.read_csv(data_path)
    df = standardise_columns(df)
    check_required_columns(df)
    df = parse_columns(df)
    df = add_log_attendance(df)

    print(f"Loaded data from: {data_path}")
    print(f"Output directory: {out_dir}")
    print(f"Original rows: {len(df):,}")

    model_data = {}
    models = {}
    model_summaries = {}

    for label, formula in MODEL_SPECIFICATIONS.items():
        required = ["log_attendance", "max_pre_streak"]
        if label in ["Model 2", "Model 3"]:
            required.extend(["is_finals", "margin", "season"])
        if label == "Model 3":
            required.append("venue")
        model, sample = fit_model(formula, df, required)
        models[label] = model
        model_data[label] = sample
        model_summaries[label] = {
            "formula": formula,
            "n": int(model.nobs),
            "r_squared": round(model.rsquared, 3),
            "coef": round(model.params["max_pre_streak"], 3),
            "se": round(model.bse["max_pre_streak"], 3),
            "p_value": float(model.pvalues["max_pre_streak"]),
        }
        print(f"{label} sample rows: {len(sample):,}")
        print(
            f"{label} max_pre_streak coef: {model.params['max_pre_streak']:.3f} "
            f"(SE = {model.bse['max_pre_streak']:.3f})"
        )

    full_sample = model_data["Model 3"].copy()
    summary_cols = ["attendance", "log_attendance", "max_pre_streak", "margin", "season"]
    sample_summary = full_sample[summary_cols].describe().T

    regression_table = build_regression_tables(models)
    plot_path = out_dir / "streak_coefficient_plot.png"
    plot_coefficients(models, plot_path)
    notes = build_notes(models)
    save_outputs(
        out_dir=out_dir,
        regression_table=regression_table,
        model_summaries=model_summaries,
        sample_summary=sample_summary,
        coef_plot_path=plot_path,
        notes=notes,
    )

    print(f"Saved main regression outputs to: {out_dir}")


if __name__ == "__main__":
    main()
