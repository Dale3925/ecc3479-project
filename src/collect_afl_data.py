from __future__ import annotations

import re
from pathlib import Path
from typing import Optional

import pandas as pd
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://afltables.com/afl/seas/{year}.html"
START_YEAR = 2000
END_YEAR = 2024
OUTPUT_PATH = Path("data/raw/afl_matches_raw.csv")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    )
}

TEAM_NAMES = {
    "Adelaide", "Brisbane Bears", "Brisbane Lions", "Carlton", "Collingwood",
    "Essendon", "Fitzroy", "Fremantle", "Geelong", "Gold Coast", "Greater Western Sydney",
    "GWS", "Hawthorn", "Melbourne", "North Melbourne", "Port Adelaide", "Richmond",
    "St Kilda", "Sydney", "West Coast", "Western Bulldogs", "Footscray"
}

ROUND_LABELS = {
    "Qualifying Final", "Elimination Final", "Semi Final",
    "Preliminary Final", "Grand Final"
}

SCORE_LINE_RE = re.compile(r"^\d+\.\d+\s+\d+\.\d+\s+\d+\.\d+\s+\d+\.\d+$")
FINAL_SCORE_RE = re.compile(r"^\d+$")
DATE_LINE_RE = re.compile(
    r"^(Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s+\d{2}-[A-Za-z]{3}-\d{4}\s+\d{1,2}:\d{2}\s+[AP]M"
)
ROUND_RE = re.compile(r"^Round\s+\d+$")
ATTENDANCE_RE = re.compile(r"^[\d,]+$")
MARGIN_RE = re.compile(r"won by\s+(\d+)\s+pts", re.IGNORECASE)


def clean_line(text: str) -> str:
    text = text.replace("\xa0", " ")
    text = text.replace("`", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def fetch_page_lines(year: int) -> list[str]:
    url = BASE_URL.format(year=year)
    response = requests.get(url, headers=HEADERS, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text("\n")
    lines = [clean_line(line) for line in text.splitlines()]
    return [line for line in lines if line]


def is_round_label(line: str) -> bool:
    return bool(ROUND_RE.match(line)) or line in ROUND_LABELS


def is_team_name(line: str) -> bool:
    return line in TEAM_NAMES


def is_finals(round_name: Optional[str]) -> bool:
    if not round_name:
        return False
    return round_name in ROUND_LABELS


def parse_datetime(text: str) -> pd.Timestamp:
    text = re.sub(r"\s+\([^)]*\)", "", text).strip()
    return pd.to_datetime(text, format="%a %d-%b-%Y %I:%M %p")


def parse_result(team1: str, team2: str, score1: int, score2: int) -> tuple[str, int]:
    if score1 > score2:
        return team1, score1 - score2
    if score2 > score1:
        return team2, score2 - score1
    return "Draw", 0


def parse_match(lines: list[str], start_idx: int, season: int, current_round: Optional[str]) -> tuple[Optional[dict], int]:
    i = start_idx

    if i >= len(lines) or not is_team_name(lines[i]):
        return None, i + 1

    team1 = lines[i]
    i += 1

    if i >= len(lines) or not SCORE_LINE_RE.match(lines[i]):
        return None, i
    i += 1

    if i >= len(lines) or not FINAL_SCORE_RE.match(lines[i]):
        return None, i
    team1_score = int(lines[i])
    i += 1

    if i >= len(lines) or not DATE_LINE_RE.match(lines[i]):
        return None, i
    match_date = parse_datetime(lines[i])
    i += 1

    if i >= len(lines) or lines[i] != "Att:":
        return None, i
    i += 1

    if i >= len(lines) or not ATTENDANCE_RE.match(lines[i]):
        return None, i
    attendance = int(lines[i].replace(",", ""))
    i += 1

    if i >= len(lines) or lines[i] != "Venue:":
        return None, i
    i += 1

    if i >= len(lines):
        return None, i
    venue = lines[i]
    i += 1

    if i >= len(lines) or not is_team_name(lines[i]):
        return None, i
    team2 = lines[i]
    i += 1

    if i >= len(lines) or not SCORE_LINE_RE.match(lines[i]):
        return None, i
    i += 1

    if i >= len(lines) or not FINAL_SCORE_RE.match(lines[i]):
        return None, i
    team2_score = int(lines[i])
    i += 1

    # Result text is often split across several lines:
    # Richmond / won by / 2 pts / [ / Match stats / ]
    result_parts = []
    while i < len(lines):
        line = lines[i]

        if is_round_label(line) or is_team_name(line):
            break

        result_parts.append(line)
        i += 1

        if "pts" in line.lower():
            # consume trailing [ Match stats ] junk if present
            while i < len(lines) and lines[i] in {"[", "]", "Match stats"}:
                i += 1
            break

    winner, margin = parse_result(team1, team2, team1_score, team2_score)

    match_id = (
        f"{season}_{(current_round or 'Unknown').replace(' ', '_')}_"
        f"{team1.replace(' ', '_')}_vs_{team2.replace(' ', '_')}"
    )

    row = {
        "match_id": match_id,
        "season": season,
        "round": current_round,
        "match_date": match_date,
        "day_of_week": match_date.day_name(),
        "team1": team1,
        "team2": team2,
        "team1_score": team1_score,
        "team2_score": team2_score,
        "winner": winner,
        "margin": margin,
        "attendance": attendance,
        "venue": venue,
        "is_finals": is_finals(current_round),
    }

    return row, i


def parse_season(year: int) -> list[dict]:
    lines = fetch_page_lines(year)

    matches = []
    current_round: Optional[str] = None
    i = 0

    while i < len(lines):
        line = lines[i]

        if is_round_label(line):
            current_round = line
            i += 1
            continue

        match, next_i = parse_match(lines, i, year, current_round)
        if match is not None:
            matches.append(match)
            i = next_i
        else:
            i = max(next_i, i + 1)

    return matches


def main() -> None:
    all_matches = []

    for year in range(START_YEAR, END_YEAR + 1):
        print(f"Scraping {year}...")
        season_matches = parse_season(year)
        print(f"  -> {len(season_matches)} matches")
        all_matches.extend(season_matches)

    if not all_matches:
        raise RuntimeError("No matches were scraped.")

    df = pd.DataFrame(all_matches)
    df = df.sort_values(["season", "match_date", "team1"]).reset_index(drop=True)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print("\nDone.")
    print(f"Saved to: {OUTPUT_PATH}")
    print(f"Total matches: {len(df):,}")
    print(df.head(10).to_string(index=False))


if __name__ == "__main__":
    main()