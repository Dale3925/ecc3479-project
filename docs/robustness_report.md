# Robustness Analysis

## Main result being tested

The main result from the Primary Econometric Analysis is that the preferred descriptive specification of log attendance on `max_pre_streak`, with controls for finals status, match margin, season fixed effects, and venue fixed effects, produces a coefficient of approximately **0.027**. This implies that each additional game in the match’s maximum pre-match winning streak is associated with roughly a **2.7 per cent higher attendance**, conditional on the included controls.

## Declared ambition

This robustness analysis is **descriptive rather than causal**. It tests whether the association between pre-match winning streaks and attendance is stable under alternative model choices, sample restrictions, functional forms, and inference methods. The aim is to assess the credibility of the descriptive finding, not to claim a causal effect.

## Robustness strategy

The robustness strategy reports the preferred model alongside seven alternative robustness checks:

1. The main preferred specification with HC3 robust standard errors.
2. A simple model with no controls.
3. A model with season controls only.
4. The main specification restricted to regular-season matches.
5. The main specification excluding COVID-disrupted seasons 2020 and 2021.
6. A levels-outcome specification using raw attendance instead of log attendance.
7. A quadratic specification that adds `max_pre_streak_sq` to the preferred model.
8. The preferred specification again with standard errors clustered by venue.

These checks are designed to test whether the coefficient on `max_pre_streak` is broadly stable to control inclusion, sample definition, functional form, and inference method.

## Robustness table

The full table of results is saved in `outputs/robustness/robustness_table.md` and `outputs/robustness/robustness_table.csv`.

Key results for `max_pre_streak` are:

- Main spec: 0.027 (SE 0.002)
- No controls: 0.040 (SE 0.004)
- Season only: 0.028 (SE 0.003)
- Regular season: 0.028 (SE 0.002)
- Exclude COVID: 0.024 (SE 0.002)
- Levels: 875.990 (SE 77.919)
- Quadratic: 0.042 (SE 0.005), with a negative quadratic term of -0.002 (SE 0.000)
- Clustered: 0.027 (SE 0.003)

## Interpretation of checks

The no-controls model produces a larger association, which is expected because it omits finals status, margin, and season and venue effects. The preferred coefficient attenuates when controls are added, suggesting that part of the raw relationship reflects broader match context rather than winning streaks alone.

The season-controls-only model is very close to the main result at **0.028**, suggesting that most of the attenuation from the no-controls model is already captured once finals status, margin, and season effects are included. Adding venue fixed effects improves fit substantially, but changes the `max_pre_streak` coefficient only slightly.

Restricting to regular-season matches leaves the coefficient essentially unchanged at **0.028**. This indicates that the descriptive association is not driven solely by finals matches.

Excluding the COVID-disrupted 2020 and 2021 seasons lowers the coefficient slightly to **0.024**, but the sign and statistical precision remain intact. This suggests that the association is not solely driven by those unusual seasons, although the exact magnitude is somewhat sensitive to that time window.

The levels-outcome model is not directly comparable in percentage terms, but it confirms the positive relationship in raw attendance units: each additional streak game is associated with around **876 more spectators** in the full sample. This supports the direction of the result while showing that the scale of interpretation depends on functional form.

The quadratic specification finds a positive linear term and a small negative squared term, consistent with a slightly concave relationship. This suggests that the attendance benefit associated with longer streaks may increase at a diminishing rate. Importantly, the main positive association remains present even when the model allows curvature.

The venue-clustered inference check also supports the result. The coefficient remains **0.027** and statistically significant, with a slightly larger standard error of **0.003** compared with the HC3 estimate. This indicates that the main finding is not an artefact of the inference method used in the preferred model.

## What the robustness analysis implies

Overall, the main descriptive finding is stable. The preferred coefficient remains positive and statistically significant across the primary sample, the regular-season-only subsample, the sample excluding COVID seasons, and under clustered inference. The estimate attenuates modestly with controls and sample restrictions, which is consistent with a conditional association rather than a raw bivariate relationship.

The only meaningful change is in scale when the outcome is measured in levels rather than log attendance; that model is consistent with a positive association, but it should not be interpreted using the same percentage logic as the log specification. The quadratic model also suggests that the exact shape of the relationship may not be perfectly linear, although this does not overturn the substantive finding.

Taken together, the robustness checks increase confidence that the positive association between winning streaks and attendance is a stable feature of the data rather than a fragile artefact of one particular modelling choice.

## Conclusion

The robustness analysis supports the descriptive conclusion that longer pre-match winning streaks are associated with higher AFL match attendance. The result is not fragile within the set of checks considered: it survives added controls, alternative sample definitions, a quadratic functional form, and venue-clustered standard errors. However, this remains a descriptive association, and the analysis does not claim a causal effect.