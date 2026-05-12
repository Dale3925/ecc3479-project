# Robustness Checks

## Research Question
This project asks whether AFL team winning streaks are associated with higher match attendance.

## Main Result
In the preferred specification, `max_pre_streak` is positively associated with log attendance after controlling for finals status, match margin, season fixed effects, and venue fixed effects. The coefficient of approximately 0.027 suggests that each additional game in the maximum pre-match winning streak is associated with roughly a 2.7 per cent higher attendance, conditional on the included controls.

## Claim Type
This is a descriptive analysis, not a causal design. The estimates should be interpreted as conditional correlations, not proof that winning streaks cause higher attendance. Teams on winning streaks may differ in unobserved ways such as fan base size, team quality, opponent quality, media attention, or fixture attractiveness, which could confound the relationship.

## Robustness Strategy
The robustness checks stress-test whether the positive association between winning streaks and attendance depends on choices of controls, sample restrictions, functional form, or standard error estimation method. Eight alternative specifications are estimated to assess the stability of the main finding.

## Robustness Table

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

## Interpretation by Check Group

### Alternative Controls
Comparing the no-controls model (column 2) to the season-only (column 3) and main/preferred (column 1) models shows that the coefficient on `max_pre_streak` attenuates from 0.040 to around 0.027-0.028 as controls are added. This suggests that part of the raw association between winning streaks and attendance is explained by observable differences in finals status, match margin, season, and venue. However, the coefficient remains positive and statistically significant even after including these controls, indicating that winning streaks have an independent association with attendance beyond these factors.

### Alternative Samples
Restricting the sample to regular-season matches only (column 4) produces a coefficient of 0.028, nearly identical to the main specification. This shows the result is not driven solely by finals matches. Excluding the COVID-disrupted seasons 2020 and 2021 (column 5) reduces the coefficient to 0.024, suggesting some sensitivity to those unusual years. However, the positive association persists, indicating the finding is not entirely dependent on the pandemic period.

### Alternative Functional Form
The levels specification (column 6) uses raw attendance instead of log attendance, resulting in a large coefficient of 875.990. This is expected because levels coefficients are in attendance-count units, not percentages, so they are not directly comparable to the log models. The quadratic specification (column 7) includes a squared term for `max_pre_streak`, yielding a positive linear coefficient of 0.042 and a negative squared coefficient of -0.002. This suggests diminishing returns to very long winning streaks, where the attendance boost tapers off at higher streak lengths.

### Alternative Inference
Re-estimating the preferred specification with standard errors clustered by venue (column 8) produces a coefficient of 0.027 with a slightly larger standard error of 0.003. Clustering accounts for potential correlation in errors within venues but does not change the sign or significance of the result.

## Overall Conclusion
The main finding survives the robustness checks: longer pre-match winning streaks are consistently associated with higher AFL match attendance across a range of model specifications, samples, and estimation methods. The coefficient remains positive and statistically significant in all eight checks, with magnitudes ranging from 0.024 to 0.042 in the log models. However, because this is a descriptive analysis, the result should be presented as a robust conditional association rather than a causal effect. The coefficient is smaller after including controls and when excluding COVID seasons, so the magnitude should be interpreted cautiously.