# Codebook for afl_matches_with_streaks.csv

This codebook describes the variables in the cleaned AFL matches dataset used for the winning streaks and attendance analysis.

## Core Match Variables
- **match_id**: Unique identifier for each AFL match
- **season**: Year of the AFL season (2000-2024)
- **round**: Round number within the season
- **match_date**: Date of the match (YYYY-MM-DD format)
- **day_of_week**: Day of the week the match was played
- **team1**: Name of the first team
- **team2**: Name of the second team
- **team1_score**: Final score of team1
- **team2_score**: Final score of team2
- **winner**: Name of the winning team
- **margin**: Winning margin (points difference)
- **attendance**: Number of spectators at the match
- **venue**: Stadium where the match was played
- **is_finals**: Binary indicator (1 if finals match, 0 if regular season)

## Streak Variables
- **team1_pre_streak**: Pre-match winning streak of team1
- **team2_pre_streak**: Pre-match winning streak of team2
- **max_pre_streak**: Maximum pre-match winning streak between the two teams
- **min_pre_streak**: Minimum pre-match winning streak between the two teams
- **streak_diff**: Difference between team1 and team2 pre-match streaks
- **team1_higher_streak**: Binary indicator (1 if team1 has higher streak than team2)
- **team2_higher_streak**: Binary indicator (1 if team2 has higher streak than team1)
- **equal_pre_streak**: Binary indicator (1 if both teams have equal pre-match streaks)

## Notes
- Streaks are calculated as consecutive wins prior to the match
- All streak variables are based on regular season matches only
- Attendance figures are as reported by AFL
- Dataset covers 4,643 matches from 2000-2024