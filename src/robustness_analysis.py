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

MODEL_SPECS = {
    "Main spec": "log_attendance ~ max_pre_streak + is_finals + margin + C(season) + C(venue)",
    "No controls": "log_attendance ~ max_pre_streak",
    "Season only": "log_attendance ~ max_pre_streak + is_finals + margin + C(season)",
    "Regular season": "log_attendance ~ max_pre_streak + is_finals + margin + C(season) + C(venue)",
    "Exclude COVID": "log_attendance ~ max_pre_streak + is_finals + margin + C(season) + C(venue)",
    "Levels": "attendance ~ max_pre_streak + is_finals + margin + C(season) + C(venue)",
    "Quadratic": "log_attendance ~ max_pre_streak + max_pre_streak_sq + is_finals + margin + C(season) + C(venue)",
    "Clustered": "log_attendance ~ max_pre_streak + is_finals + margin + C(season) + C(venue)",
}

SAMPLE_DESCRIPTIONS = {
    "Main spec": "Full sample",
    "No controls": "Full sample",
    "Season only": "Full sample",
    "Regular season": "Regular season only",
    "Exclude COVID": "Exclude 2020 and 2021",
    "Levels": "Full sample",
    "Quadratic": "Full sample",
    "Clustered": "Full sample",
}

OUTCOME_LABELS = {
    "Main spec": "log(attendance)",
    "No controls": "log(attendance)",
    "Season only": "log(attendance)",
    "Regular season": "log(attendance)",
    "Exclude COVID": "log(attendance)",
    "Levels": "attendance",
    "Quadratic": "log(attendance)",
    "Clustered": "log(attendance)",
}

SE_TYPES = {
    "Main spec": "HC3",
    "No controls": "HC3",
    "Season only": "HC3",
    "Regular season": "HC3",
    "Exclude COVID": "HC3",
    "Levels": "HC3",
    "Quadratic": "HC3",
    "Clustered": "Clustered by venue",
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
    out_dir = repo_root / "outputs" / "robustness"
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir


def standardise_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("-", "_", regex=False)
    )
    return df


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


def add_log_attendance(df: pd.DataFrame) -> pd.DataFrame:
    if "attendance" not in df.columns:
        return df
    df = df.copy()
    df["log_attendance"] = np.where(df["attendance"] > 0, np.log(df["attendance"]), np.nan)
    return df


def add_quadratic_terms(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "max_pre_streak" in df.columns:
        df["max_pre_streak_sq"] = df["max_pre_streak"] ** 2
    return df


def check_required_columns(df: pd.DataFrame) -> None:
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(
            "Missing required column(s) for robustness analysis: "
            + ", ".join(missing)
        )


def fit_model(formula: str, data: pd.DataFrame, required_columns: list[str], cov_type: str = "HC3", cov_kwds: dict | None = None):
    model_data = data.dropna(subset=required_columns).copy()
    if model_data.empty:
        raise ValueError(
            f"No observations available after dropping missing values for formula: {formula}. "
            f"Required columns: {required_columns}"
        )
    cov_kwds = cov_kwds or {}
    model = smf.ols(formula=formula, data=model_data).fit(cov_type=cov_type, cov_kwds=cov_kwds)
    return model, model_data


def format_coef(coef: float | int, se: float | int) -> str:
    return f"{coef:.3f} ({se:.3f})"


def build_compact_robustness_table(models: dict[str, dict]) -> pd.DataFrame:
    columns = ['(1) Main', '(2) No ctrls', '(3) Season FE', '(4) Reg season', '(5) No COVID', '(6) Levels', '(7) Quadratic', '(8) Clustered']
    labels = ['Main spec', 'No controls', 'Season only', 'Regular season', 'Exclude COVID', 'Levels', 'Quadratic', 'Clustered']
    df = pd.DataFrame(columns=['Variable'] + columns)
    
    # row 0: max_pre_streak
    row0 = ['max_pre_streak']
    for label in labels:
        info = models.get(label, {})
        model = info.get('model')
        if model is not None:
            coef = model.params.get('max_pre_streak')
            if coef is not None:
                row0.append(f"{coef:.3f}")
            else:
                row0.append('—')
        else:
            row0.append('—')
    df.loc[0] = row0
    
    # row 1: '' for SE
    row1 = ['']
    for label in labels:
        info = models.get(label, {})
        model = info.get('model')
        if model is not None:
            se = model.bse.get('max_pre_streak')
            if se is not None:
                row1.append(f"({se:.3f})")
            else:
                row1.append('')
        else:
            row1.append('')
    df.loc[1] = row1
    
    # row 2: max_pre_streak_sq
    row2 = ['max_pre_streak_sq']
    for label in labels:
        info = models.get(label, {})
        model = info.get('model')
        if model is not None:
            coef = model.params.get('max_pre_streak_sq')
            if coef is not None:
                row2.append(f"{coef:.3f}")
            else:
                row2.append('—')
        else:
            row2.append('—')
    df.loc[2] = row2
    
    # row 3: '' for SE sq
    row3 = ['']
    for label in labels:
        info = models.get(label, {})
        model = info.get('model')
        if model is not None:
            se = model.bse.get('max_pre_streak_sq')
            if se is not None:
                row3.append(f"({se:.3f})")
            else:
                row3.append('')
        else:
            row3.append('')
    df.loc[3] = row3
    
    # row 4: N
    row4 = ['N']
    for label in labels:
        info = models.get(label, {})
        model = info.get('model')
        if model is not None:
            row4.append(int(model.nobs))
        else:
            row4.append('—')
    df.loc[4] = row4
    
    # row 5: R-squared
    row5 = ['R-squared']
    for label in labels:
        info = models.get(label, {})
        model = info.get('model')
        if model is not None:
            row5.append(f"{model.rsquared:.3f}")
        else:
            row5.append('—')
    df.loc[5] = row5
    
    return df


def table_to_markdown(df: pd.DataFrame) -> str:
    header = df.columns.tolist()
    lines = ["| " + " | ".join(header) + " |", "|---|" + "|".join(["---:"] * (len(header) - 1)) + "|"]
    for _, row in df.iterrows():
        cells = []
        for col in header:
            cell = row[col]
            if pd.isna(cell):
                cells.append("—")
            elif cell == "":
                cells.append("")
            else:
                cells.append(str(cell))
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def write_markdown_table_with_notes(df: pd.DataFrame, notes: str, out_path: Path) -> None:
    md_table = table_to_markdown(df)
    full_content = md_table + "\n\n" + notes
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(full_content)


def save_outputs(out_dir: Path, table: pd.DataFrame, summary_rows: list[dict], notes: str, plot_path: Path) -> None:
    table.to_csv(out_dir / "robustness_table.csv", index=False)
    write_markdown_table_with_notes(table, notes, out_dir / "robustness_table.md")
    pd.DataFrame(summary_rows).to_csv(out_dir / "robustness_model_summary.csv", index=False)
    (out_dir / "robustness_notes.txt").write_text(notes, encoding="utf-8")
    if plot_path.exists():
        return
    raise FileNotFoundError(f"Expected coefficient plot at {plot_path} not found.")


def plot_coefficients(models: dict[str, dict], out_path: Path) -> None:
    labels = []
    estimates = []
    lower = []
    upper = []
    for label, info in models.items():
        model = info.get("model")
        if model is None or "max_pre_streak" not in model.params:
            continue
        coef = model.params["max_pre_streak"]
        se = model.bse["max_pre_streak"]
        ci = model.conf_int().loc["max_pre_streak"]
        labels.append(label)
        estimates.append(coef)
        lower.append(coef - 1.96 * se)
        upper.append(coef + 1.96 * se)

    fig, ax = plt.subplots(figsize=(8, 4))
    x = np.arange(len(labels))
    ax.errorbar(
        x,
        estimates,
        yerr=[np.array(estimates) - np.array(lower), np.array(upper) - np.array(estimates)],
        fmt="o",
        color="black",
        ecolor="grey",
        capsize=5,
    )
    ax.axhline(0, color="black", linewidth=0.75, linestyle="--")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45, ha="right")
    ax.set_ylabel("Coefficient on max_pre_streak")
    ax.set_title("Robustness check: max_pre_streak coefficient")
    ax.grid(axis="y", linestyle=":", color="grey", alpha=0.6)
    fig.tight_layout()
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def capture_notes(models: dict[str, dict], notes: list[str]) -> str:
    lines = ["Robustness analysis notes:"]
    lines.extend(notes)
    lines.append("")
    lines.append("Model summaries:")
    for label, info in models.items():
        model = info.get("model")
        if model is None:
            lines.append(f"{label}: model estimation failed.")
            continue
        coef = model.params.get("max_pre_streak", np.nan)
        se = model.bse.get("max_pre_streak", np.nan)
        pval = model.pvalues.get("max_pre_streak", np.nan)
        lines.append(
            f"{label}: max_pre_streak = {coef:.3f}, SE = {se:.3f}, p = {pval:.3f}, N = {int(model.nobs)}."
        )
    return "\n".join(lines)


def save_outputs(out_dir: Path, table: pd.DataFrame, summary_rows: list[dict], notes_text: str, plot_path: Path) -> None:
    table.to_csv(out_dir / "robustness_table.csv", index=False)
    pd.DataFrame(summary_rows).to_csv(out_dir / "robustness_model_summary.csv", index=False)
    (out_dir / "robustness_notes.txt").write_text(notes_text, encoding="utf-8")
    notes = """**Notes:** Standard errors in parentheses. Column (1) is the preferred specification with finals status, margin, season fixed effects, and venue fixed effects. Column (2) includes no controls. Column (3) includes finals status, margin, and season fixed effects, but no venue fixed effects. Column (4) restricts the sample to regular-season matches only. Column (5) excludes seasons 2020 and 2021. Column (6) uses attendance in levels rather than log attendance. Column (7) adds a quadratic streak term. Column (8) re-estimates the preferred specification with standard errors clustered by venue. All columns use the full sample unless otherwise noted."""
    write_markdown_table_with_notes(table, notes, out_dir / "robustness_table.md")
    if plot_path.exists():
        # Assuming the plot is already saved in plot_coefficients
        pass


def main() -> None:
    repo_root = find_repo_root()
    data_path = repo_root / "data" / "clean" / "afl_matches_with_streaks.csv"
    out_dir = choose_output_dir(repo_root)

    df = pd.read_csv(data_path)
    df = standardise_columns(df)
    check_required_columns(df)
    df = parse_columns(df)
    df = add_log_attendance(df)
    df = add_quadratic_terms(df)

    print(f"Loaded data from: {data_path}")
    print(f"Output directory: {out_dir}")
    print(f"Original rows: {len(df):,}")

    models: dict[str, dict] = {}
    notes: list[str] = []

    for label, formula in MODEL_SPECS.items():
        model_data = df
        required = ["max_pre_streak"]
        if "log_attendance" in formula:
            required.append("log_attendance")
        if "is_finals" in formula:
            required.extend(["is_finals", "margin", "season"])
        if "C(venue)" in formula:
            required.append("venue")
        if "max_pre_streak_sq" in formula:
            required.append("max_pre_streak_sq")
        if label == "Regular season":
            model_data = model_data[model_data["is_finals"] == 0].copy()
        if label == "Exclude COVID":
            model_data = model_data[~model_data["season"].isin([2020, 2021])].copy()

        if label == "Clustered":
            try:
                model, sample = fit_model(formula, model_data, required, cov_type="cluster", cov_kwds={"groups": model_data["venue"]})
                models[label] = {
                    "model": model,
                    "n": int(model.nobs),
                    "r_squared": round(model.rsquared, 3),
                    "season_fe": "Yes" if "C(season)" in formula else "No",
                    "venue_fe": "Yes" if "C(venue)" in formula else "No",
                }
            except Exception as exc:
                notes.append(
                    f"Clustered-by-venue inference failed: {type(exc).__name__}: {exc}. "
                    "The main specification is still reported with HC3 robust SEs in the notes."
                )
                models[label] = {
                    "model": None,
                    "n": len(model_data),
                    "r_squared": "—",
                    "season_fe": "Yes" if "C(season)" in formula else "No",
                    "venue_fe": "Yes" if "C(venue)" in formula else "No",
                }
            continue

        try:
            model, sample = fit_model(formula, model_data, required)
            models[label] = {
                "model": model,
                "n": int(model.nobs),
                "r_squared": round(model.rsquared, 3),
                "season_fe": "Yes" if "C(season)" in formula else "No",
                "venue_fe": "Yes" if "C(venue)" in formula else "No",
            }
        except Exception as exc:
            notes.append(f"{label} failed: {type(exc).__name__}: {exc}")
            models[label] = {
                "model": None,
                "n": len(model_data),
                "r_squared": "—",
                "season_fe": "Yes" if "C(season)" in formula else "No",
                "venue_fe": "Yes" if "C(venue)" in formula else "No",
            }

    summary_rows = []
    for label, info in models.items():
        model = info.get("model")
        if model is None:
            summary_rows.append(
                {
                    "model_label": label,
                    "formula": MODEL_SPECS[label],
                    "n": info.get("n", 0),
                    "r_squared": info.get("r_squared", ""),
                    "coef_max_pre_streak": "",
                    "se_max_pre_streak": "",
                    "p_value_max_pre_streak": "",
                }
            )
            continue
        summary_rows.append(
            {
                "model_label": label,
                "formula": MODEL_SPECS[label],
                "n": int(model.nobs),
                "r_squared": round(model.rsquared, 3),
                "coef_max_pre_streak": float(model.params.get("max_pre_streak", np.nan)),
                "se_max_pre_streak": float(model.bse.get("max_pre_streak", np.nan)),
                "p_value_max_pre_streak": float(model.pvalues.get("max_pre_streak", np.nan)),
            }
        )

    regression_table = build_compact_robustness_table(models)
    regression_table.to_csv(out_dir / "robustness_table.csv", index=False)
    notes = """**Notes:** Standard errors in parentheses. Column (1) is the preferred specification with finals status, margin, season fixed effects, and venue fixed effects. Column (2) includes no controls. Column (3) includes finals status, margin, and season fixed effects, but no venue fixed effects. Column (4) restricts the sample to regular-season matches only. Column (5) excludes seasons 2020 and 2021. Column (6) uses attendance in levels rather than log attendance. Column (7) adds a quadratic streak term. Column (8) re-estimates the preferred specification with standard errors clustered by venue. All columns use the full sample unless otherwise noted."""
    write_markdown_table_with_notes(regression_table, notes, out_dir / "robustness_table.md")

    notes_text = capture_notes(models, notes)
    pd.DataFrame(summary_rows).to_csv(out_dir / "robustness_model_summary.csv", index=False)
    (out_dir / "robustness_notes.txt").write_text(notes_text, encoding="utf-8")

    coef_plot_path = out_dir / "robustness_coefficient_plot.png"
    plot_coefficients(models, coef_plot_path)


if __name__ == "__main__":
    main()
