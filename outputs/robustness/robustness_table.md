| Variable | (1) Main | (2) No ctrls | (3) Season FE | (4) Reg season | (5) No COVID | (6) Levels | (7) Quadratic | (8) Clustered |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| max_pre_streak | 0.027 | 0.040 | 0.028 | 0.028 | 0.024 | 875.990 | 0.042 | 0.027 |
|  | (0.002) | (0.004) | (0.003) | (0.002) | (0.002) | (77.919) | (0.005) | (0.003) |
| max_pre_streak_sq | — | — | — | — | — | — | -0.002 | — |
|  |  |  |  |  |  |  | (0.000) |  |
| N | 4643 | 4643 | 4643 | 4427 | 4340 | 4643 | 4643 | 4643 |
| R-squared | 0.734 | 0.020 | 0.346 | 0.728 | 0.675 | 0.604 | 0.735 | 0.734 |
| Outcome | log(attendance) | log(attendance) | log(attendance) | log(attendance) | log(attendance) | attendance | log(attendance) | log(attendance) |
| Controls | Finals, Margin, Season FE, Venue FE | None | Finals, Margin, Season FE | Finals, Margin, Season FE, Venue FE | Finals, Margin, Season FE, Venue FE | Finals, Margin, Season FE, Venue FE | Finals, Margin, Season FE, Venue FE, Quadratic | Finals, Margin, Season FE, Venue FE |
| Sample | Full sample | Full sample | Full sample | Regular season only | Exclude 2020 and 2021 | Full sample | Full sample | Full sample |
| SE type | HC3 | HC3 | HC3 | HC3 | HC3 | HC3 | HC3 | Clustered by venue |

**Notes:** Standard errors in parentheses. Column (1) is the preferred specification with finals status, margin, season fixed effects, and venue fixed effects. Column (2) includes no controls. Column (3) includes finals status, margin, and season fixed effects, but no venue fixed effects. Column (4) restricts the sample to regular-season matches only. Column (5) excludes seasons 2020 and 2021. Column (6) uses attendance in levels rather than log attendance. Column (7) adds a quadratic streak term. Column (8) re-estimates the preferred specification with standard errors clustered by venue. All columns use the full sample unless otherwise noted.