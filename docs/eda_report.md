# Exploratory Data Analysis

## Research question

This project asks whether team winning streaks increase AFL match attendance. The analysis uses a cleaned match-level dataset covering AFL matches from 2000 to 2024. After cleaning and filtering for the key analysis variables, the EDA sample contains 4,643 observations, the same as the original cleaned dataset. This indicates that there is no additional sample loss at the EDA stage from missing values in the main variables of interest.

The purpose of this EDA is not to make a final causal claim. Instead, it is to understand the structure of the cleaned data, identify unusual features, and assess whether a first-order relationship exists between pre-match winning streaks and attendance. This matches the role of EDA in the course: to understand how the data behaves before moving to a formal econometric model.

## 1. Sample overview and variable characteristics

The main variables used in this EDA are attendance, log attendance, maximum pre-match winning streak, winning margin, season, venue, and finals status. These variables are consistent with the research question, as attendance is the outcome of interest and pre-match winning streak is the main explanatory variable.

**Exhibit A** reports the variable overview and missingness. The key takeaway is that the main variables required for the EDA are sufficiently complete to proceed with analysis. In particular, attendance, log attendance, pre-match winning streak, margin, and season are all observed for all 4,643 matches in the EDA sample. This is important because it means the descriptive analysis is not being driven by additional row dropping at this stage.

**Exhibit B** reports summary statistics for the main numeric variables. Attendance averages 34,439.9 spectators, with a standard deviation of 17,813.6, a median of 32,942, and a maximum of 100,024. This confirms that attendance varies substantially across matches. Log attendance has a mean of 10.281 and a standard deviation of 0.667, indicating a much more compressed distribution than attendance in levels. The mean pre-match winning streak is 1.96 matches, with a median of 1, a 75th percentile of 3, and a maximum of 19. This suggests that most observations involve short streaks, while very long streaks are relatively rare. Margin also varies widely, with a mean of 34.37 points and a maximum of 186, which is plausible for AFL matches. The season variable runs from 2000 to 2024, with a mean of 2012.55, showing broad coverage across the modern AFL era.

Overall, the cleaned variables look broadly as expected. The main point of note is that attendance in levels is highly dispersed and likely right-skewed, while winning streaks are discrete and concentrated at relatively low values.

## 2. Distribution of attendance

**Exhibits 1 and 2** show the distribution and box plot of attendance. These exhibits indicate that attendance is not symmetrically distributed. The mean attendance is 34,439.9, while the median is 32,942, and the maximum is 100,024. This gap between the centre of the distribution and the upper tail suggests right-skewness, with most matches drawing moderate crowds and a smaller number of matches attracting extremely large attendances. This is economically plausible, since marquee games, major venues, and finals matches are likely to attract much bigger crowds than typical regular season fixtures.

The box plot also helps identify whether extreme values are likely to be data errors or genuine observations. In this case, the largest attendance values are likely real matches played at major venues like the GF at the MCG rather than coding mistakes. They should therefore not be dropped automatically. However, the skewness does suggest that modelling attendance in levels may overstate the influence of these high-crowd observations.

**Exhibit 3** therefore plots log attendance. The summary statistics support this transformation. The standard deviation falls from 17,813.6 in levels to 0.667 in logs, and the log distribution should appear much more compressed and closer to symmetric. This suggests that a log transformation is appropriate for the formal regression stage. A log specification is useful here because it reduces the influence of extreme attendance values and allows the coefficient on winning streaks to be interpreted in approximate percentage terms rather than raw crowd numbers.

Taken together, these exhibits suggest that attendance in levels is highly skewed, while log attendance is more suitable for regression analysis.

## 3. Distribution of pre-match winning streaks

**Exhibit 4** shows the distribution of pre-match winning streaks. The variable is discrete and concentrated at relatively small values. The mean streak is 1.96 matches, the median is 1, the 25th percentile is 0, and the 75th percentile is 3. The maximum is 19, but this appears to be an extreme tail observation rather than the norm.

This pattern is expected. In a competitive league, most teams frequently move in and out of short streaks, while very long winning streaks are uncommon. This matters because the relationship of interest is identified mostly from variation among shorter streak lengths. If very long streaks occur only rarely, then the estimated relationship at the top end of the streak distribution may be less precise and more sensitive to noise.

The streak variable therefore looks usable, but it also suggests that the relationship may not be perfectly linear across all streak lengths.

## 4. Attendance over time

**Exhibit 5** reports mean attendance by season. This exhibit is important because it shows whether attendance shifts over time, independent of winning streaks. The season variable spans 2000 to 2024, so there is substantial scope for long-run variation in average attendance due to league expansion, venue changes, scheduling, population growth, and broader shocks affecting live sport attendance.

If mean attendance changes noticeably across seasons, then a simple pooled relationship between streaks and attendance may partly capture year-level differences rather than the within-season effect of interest. The main implication is that the formal model should include season controls, such as season fixed effects or season dummies, to avoid attributing time variation in attendance to winning streaks.

## 5. Finals versus regular season matches

**Exhibit 6** compares attendance by finals status. Finals matches are expected to attract larger crowds than regular season matches, and the exhibit shows a higher centre and upper range for finals games.

This is a major source of heterogeneity in the dataset. Finals status is likely correlated with both attendance and team quality, and stronger teams may also be more likely to arrive with winning streaks. As a result, failing to account for finals matches could overstate the relationship between streaks and attendance if part of the apparent effect is actually being driven by the higher demand for finals football.

This suggests that finals status should be included as a control variable in the next stage of analysis, or that the results should at least be checked separately for finals and non-finals matches.

## 6. Venue heterogeneity

**Exhibit 7** compares attendance across the major venues in the sample. Venue differences are expected to be large because AFL grounds vary in seating capacity, location, and supporter base. A match played at the MCG is not directly comparable to a match played at a smaller regional venue in terms of raw attendance.

The exhibit is therefore useful in showing that venue is a major determinant of crowd size. If stronger or more popular teams on winning streaks are more likely to play at larger venues, then venue could confound the first-order relationship between streaks and attendance.

The implication is that venue controls, or related location/home-ground controls if available, are likely to be important in the formal econometric model.

## 7. Winning streaks and attendance

**Exhibit 8** plots attendance against pre-match winning streak in levels, while **Exhibit 9** plots log attendance against pre-match winning streak. These are the key exhibits for the research question.

**Exhibit C** reports the pairwise correlations between winning streaks and attendance. The Pearson correlation between pre-match winning streak and attendance is 0.170, while the Spearman correlation is 0.154. For log attendance, the Pearson correlation is 0.142 and the Spearman correlation is again 0.154. These values are positive, but modest in size. This suggests that matches involving longer winning streaks do tend to attract larger crowds on average, but the relationship is not especially strong on its own.

The difference between the level-attendance and log-attendance Pearson correlations is also informative. The Pearson correlation is slightly higher in levels (0.170) than in logs (0.142), suggesting that some of the raw linear relationship may be amplified by higher-attendance matches in the upper tail. By contrast, the Spearman correlation is identical for attendance and log attendance at 0.154, implying that the rank-order association is stable across both scales. This is consistent with the idea that the positive relationship is real, but modest, and not purely driven by a handful of outliers.

The main takeaway from these plots and correlations is that there appears to be a positive first-order relationship between winning streaks and attendance, but it is not especially strong. Winning streaks may matter, but they are clearly only one of several drivers of AFL crowd size.

## 8. Mean and median attendance by streak

**Exhibit 10** reports mean and median attendance by winning streak length. This exhibit is useful because it moves beyond the raw scatter and asks whether average attendance tends to rise as streak length increases.

If both the mean and median series trend upward, that supports the positive first-order relationship already suggested by the correlation table. If the mean rises more sharply than the median, that would suggest that the relationship is partly driven by a smaller number of very large-attendance matches. If both move similarly, the relationship is more broadly distributed across the sample.

This exhibit therefore helps assess whether the positive streak-attendance relationship is robust to using a less outlier-sensitive summary measure. In our case we see mean and median rise and fall together with the mean ahead most of the time. However at the 15 streak mark the median jumps ahead and then the two are equal for larger streaks.

## 9. Heterogeneity by finals status

**Exhibit 11** splits the attendance-streak relationship by finals status. This is important because it checks whether the pooled relationship is masking subgroup differences. A positive pooled association does not necessarily mean the same pattern holds within both finals and regular season matches.

If the relationship differs across finals and non-finals games, that would be a sign of heterogeneity and possibly a composition effect. For example, winning streaks may matter more for regular season matches, while finals attendance may already be high regardless of streak length. Alternatively, the stronger pooled relationship could simply reflect the fact that finals games are both more highly attended and more likely to involve stronger teams.

This exhibit therefore provides an informal check against subgroup composition effects and helps identify whether the pooled relationship should be interpreted cautiously.

## 10. Within-season partial relationship

**Exhibit 12** presents a regression of log attendance on pre-match winning streak with season fixed effects. This is not yet the final econometric model, but it is a useful bridge between pure EDA and formal analysis because it asks whether the streak relationship remains once season-level differences are partialled out.

The coefficient on `max_pre_streak` is **0.0365** with a standard error of **0.0035** and a p-value effectively equal to zero. Because the dependent variable is log attendance, this can be interpreted as a semi-elasticity: one additional pre-match win is associated with approximately a **3.6% increase in attendance**, holding season constant. This suggests that the positive relationship between winning streaks and attendance is not purely an artefact of cross-season differences.

The season coefficients are also informative. In particular, the coefficients for **2020 (-1.999)** and **2021 (-0.461)** are strongly negative, which is consistent with the large disruption to AFL crowd attendance during the COVID-19 period. This reinforces the importance of including season controls in the formal regression stage, since attendance clearly varies over time for reasons unrelated to team winning streaks.

This exhibit should still be interpreted cautiously. It does not establish causality, and it does not yet control for other important factors such as finals status, venue, or team-specific popularity. However, it provides strong descriptive evidence that the positive association between winning streaks and attendance survives a basic within-season comparison.

## 11. What the EDA implies for modelling

Several conclusions emerge from the EDA.

First, attendance is strongly right-skewed, and log attendance appears more appropriate than attendance in levels for regression analysis. The large gap between the minimum and maximum attendance values, together with the smaller dispersion in log attendance, supports using log attendance as the dependent variable.

Second, there is a positive but modest first-order relationship between pre-match winning streaks and attendance. The pairwise correlations are positive in both levels and logs, but they are all relatively small, ranging from **0.142 to 0.170**. This supports the project hypothesis at a descriptive level, but it also shows that winning streaks alone explain only a limited share of crowd variation.

Third, once season effects are included, the relationship remains clearly positive. The within-season regression coefficient of **0.0365** implies that each additional pre-match win is associated with about a **3.6% increase in attendance**, even after accounting for season-level shifts. This is an important result because it shows the streak relationship is not just being driven by broad attendance differences across years.

Fourth, there is substantial heterogeneity across seasons, finals status, and venues. These factors are all plausible confounders because they affect attendance and may also be related to team success or streak length. This means the next stage of analysis should control for these variables where possible.

Fifth, the discrete and uneven distribution of winning streaks suggests caution in assuming a perfectly linear effect across all streak lengths. Since the median streak is only **1** match and the 75th percentile is **3**, the relationship is identified mostly from short streak variation. It may therefore be useful to test whether the effect is nonlinear or whether very long streaks behave differently from short ones.

Overall, the EDA suggests that winning streaks have a positive association with attendance, and this association remains economically meaningful once season effects are included. However, the size and interpretation of this effect still depend on accounting for other important determinants of crowd size in the formal regression stage.

## Conclusion

The EDA shows that the cleaned AFL attendance dataset is suitable for further analysis and contains meaningful variation in both attendance and winning streaks. Attendance is highly dispersed and right-skewed in levels, making log attendance the more appropriate modelling choice. There is preliminary evidence of a positive association between winning streaks and attendance, and this relationship remains present after controlling for season effects. In particular, the within-season regression suggests that each additional pre-match win is associated with roughly a **3.6% increase in attendance**.

These findings do not establish a causal effect. Instead, they provide a clear descriptive foundation for the next stage of the project and help justify the modelling decisions that follow, especially the use of log attendance and the inclusion of controls for season, finals status, and venue-related factors.