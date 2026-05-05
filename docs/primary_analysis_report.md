# Primary Econometric Analysis

## Research question
Do team winning streaks increase AFL match attendance?

## Declared ambition
This analysis is descriptive rather than causal. It estimates conditional associations between pre-match winning streaks and AFL match attendance.

## Econometric specification
The analysis estimates three ordinary least squares (OLS) models using heteroskedasticity-robust HC3 standard errors. The dependent variable is the natural logarithm of match attendance, which accounts for the right-skewed distribution of attendance figures and allows coefficients to be interpreted in approximate percentage terms.

The estimated specifications are:

**Model 1**

`log(attendance_i) = β0 + β1 · max_pre_streak_i + ε_i`

**Model 2**

`log(attendance_i) = β0 + β1 · max_pre_streak_i + β2 · is_finals_i + β3 · margin_i + γ_s + ε_i`

**Model 3**

`log(attendance_i) = β0 + β1 · max_pre_streak_i + β2 · is_finals_i + β3 · margin_i + γ_s + δ_v + ε_i`

where `γ_s` denotes season fixed effects and `δ_v` denotes venue fixed effects.

The key independent variable is `max_pre_streak`, defined as the maximum pre-match winning streak in the match. Model 1 estimates the raw association between winning streaks and attendance. Model 2 adds controls for finals status, match margin, and season effects. Model 3 further includes venue fixed effects and is the preferred descriptive specification.

## Sample
The regression sample consists of 4,643 AFL matches from the 2000 to 2024 seasons. All models are estimated on the same sample after excluding matches with missing values for the required variables. The sample covers a broad range of seasons, venues, and match types, providing a comprehensive view of AFL attendance patterns.

## Main results
Table 1 reports the main regression results. Robust HC3 standard errors are reported in parentheses.

```
Variable          Model 1          Model 2          Model 3
---------------  ---------------  ---------------  -------------
max_pre_streak   0.040 (0.004)    0.028 (0.003)    0.027 (0.002)
is_finals        —                0.610 (0.035)    0.392 (0.025)
margin           —                -0.001 (0.000)  -0.001 (0.000)
N                4643             4643             4643
R-squared        0.02             0.346            0.734
Season_FE        No               Yes              Yes
Venue_FE         No               No               Yes
```

The coefficient on `max_pre_streak` is positive and statistically significant across all models, though it attenuates as additional controls are included. The explanatory power of the models increases substantially with the addition of season and venue fixed effects.

## Interpretation
The Model 3 coefficient on `max_pre_streak` is 0.027 (standard error 0.002). This suggests that, holding finals status, match margin, season, and venue constant, each additional game in the match’s maximum pre-match winning streak is associated with approximately a 2.7 per cent higher match attendance (calculated as 100 × 0.027). This semi-elasticity interpretation reflects the log-linear specification of the model.

## Threats and limitations
As a descriptive analysis, this study estimates conditional associations rather than causal effects. The main limitation is omitted confounding. Team popularity or club size, rivalry intensity, match timing and scheduling, ladder position, finals race importance, and home-team effects may all be correlated with both winning streaks and attendance. If stronger and more popular teams are more likely to generate longer winning streaks and also attract larger crowds, the estimated coefficient on `max_pre_streak` may be upward biased relative to the independent association of streaks alone.

There may also be sample composition, capacity, and measurement limitations. Venue capacity can constrain observed attendance, and the streak variable may not capture all aspects of team quality or match attractiveness. For these reasons, the results should not be interpreted as evidence of a causal relationship between winning streaks and attendance.

## Conclusion
The analysis finds a positive association between pre-match winning streaks and AFL match attendance. In the preferred specification, each additional game in the match’s maximum pre-match winning streak is associated with approximately a 2.7 per cent increase in attendance, holding finals status, match margin, season, and venue constant. The coefficient remains statistically precise after the inclusion of substantial controls, although it attenuates relative to the simple bivariate model.

However, this is a descriptive rather than causal result. The findings are best interpreted as evidence that stronger recent team form is associated with higher attendance, not that winning streaks themselves necessarily cause crowd sizes to rise.