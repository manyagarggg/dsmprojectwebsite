# Guide to figures in sangam_ganga_figures
## construction_mining_analysis.ipynb
fig_temporal_surge.png
What it shows: Bar chart of annual illegal sand mining incidents (2010–2025), split blue (pre-PMAY) vs red (post-PMAY). A dashed vertical line marks 2015 (PMAY-U launch). Dotted horizontal lines show the group means. The right panel shows year-on-year growth rates post-2015.

How to read it: Blue bars are the pre-policy baseline. Red bars are post-launch. The further the red bars extend above the blue mean line, the bigger the post-PMAY surge.

Key finding: Mining jumps from 13 incidents/year on average pre-2015 to 191/year post-2015 — a 14.7× increase. Mann-Whitney confirms this is statistically significant (p=0.001). The sharpest single-year spike is 2022–2023 (549 incidents), coinciding with PMAY construction completion pressure.

## fig_event_study.png
What it shows: Event study coefficients — the estimated effect of being a "high-PMAY allocation" state in each year relative to 2014 (the omitted baseline year). Each dot is a DiD coefficient; bars are 95% CIs. The red dashed line marks the PMAY launch. Green shading = pre-period; red shading = post-period.

How to read it: Dots to the left of the red line (pre-period) should be near zero if the parallel-trends assumption holds — meaning high and low PMAY states were trending similarly before the policy. Dots to the right show whether high-PMAY states diverged after launch.

Key finding: Pre-trend F-test gives p=0.805 — the pre-period coefficients are jointly indistinguishable from zero. This validates the DiD design. Post-2015, coefficients rise sharply and stay positive, confirming high-PMAY states experienced significantly more mining after the scheme launched.

## fig_synthetic_control.png
What it shows: Left panel — actual UP mining trajectory (red) vs a synthetic counterfactual UP (blue dashed) constructed as a weighted average of donor states that best matched UP's pre-2015 mining pattern. Right panel — the year-by-year gap (actual minus synthetic).

How to read it: The synthetic UP represents "what would have happened to UP's mining if PMAY had not launched." The red shaded area between the curves (post-2015) is the estimated causal effect. A pre-period RMSE of 0.12 means the synthetic control fit the pre-treatment period well.

Key finding: UP's actual mining is +158% above its synthetic counterfactual post-2015 (ATT = +0.948 log-units). The gap opens immediately in 2015 and grows through 2023 before falling back. This corroborates the DiD result using a completely different identification strategy.

## fig_ols_coefficients.png
What it shows: Horizontal bar chart of OLS regression coefficients (with 95% CIs as error bars) for predictors of log(mining incidents), using heteroskedasticity-robust (HC3) standard errors. Variables are centred so coefficients are comparable. Stars mark significance.

How to read it: Red bars point right (positive effect on mining), blue bars point left (negative). Error bars crossing the zero dashed line mean the variable is not statistically significant. The longer the bar, the stronger the effect.

Key finding: log(PMAY) is the only significant predictor (β=+0.593, p<0.001; R²=0.576). Once construction scale is controlled for, poverty (% BPL), literacy, urbanisation, and completion rate all become non-significant — their apparent bivariate correlations with mining are largely explained by PMAY allocation.

## fig_spatial_clusters.png
What it shows: Side-by-side India choropleth maps. Left: PMAY houses sanctioned per state (Blues gradient). Right: mining incident counts per state (YlOrRd gradient). The bivariate Moran's I statistic is shown in the right title.

How to read it: If construction demand and mining supply were spatially co-located, both maps would show the same dark-state pattern. Visual divergence suggests spatial decoupling.

Key finding: Bivariate Moran's I = 0.033, p=0.42 — no significant spatial co-clustering at the state level. Andhra Pradesh and UP have the most PMAY houses but moderate mining; Madhya Pradesh has the most mining but not the most PMAY. This means mining doesn't happen in the highest-construction states — it happens in economically vulnerable states that supply sand to distant construction markets. Mining and construction are spatially decoupled across state borders.

## fig_rf_importance.png
What it shows: Permutation feature importance from a Random Forest regressor predicting state-level mining counts. Each bar shows how much the model's R² drops when that variable's values are randomly shuffled (larger drop = more important). Error bars are standard deviations across 100 permutation repeats.

How to read it: Bars extending right mean the variable genuinely predicts mining. A bar near zero means the model barely uses that feature. OOB R² of 0.354 means the RF predicts ~35% of variance on held-out states.

Key finding: Central government assistance (₹Cr) and total PMAY sanctioned are the top two predictors, ahead of all economic variables. This supports the causal story — it's the scale of government-mandated construction (measured by both houses and rupees) that best explains mining intensity, not background socioeconomic conditions alone.

spatial_analysis.ipynb — Section 11 (Ganga/Sangam)
## fig_ganga_sangam_timeseries.png
What it shows: Three-panel time series (Jan 2019 – Feb 2020) for both sensors. Top: WQI (higher = worse). Middle: Conductivity (µS/cm). Bottom: Dissolved Oxygen (mg/L). Blue = Ganga sensor; orange = Sangam sensor. Purple shading marks the Kumbh Mela window; faint red shading marks dry-season months.

How to read it: WQI and conductivity spiking together = worse water quality. DO dropping = ecosystem stress. Recurrent seasonal patterns are the main signal.

Key finding: Conductivity rises sharply from May 2019 onward, peaking in Nov 2019 – Feb 2020 (dry season), which is exactly when river levels fall and sand mining peaks nationally. The two sensors track each other closely, confirming this is a river-wide phenomenon.

## fig_ganga_seasonal.png
What it shows: Monthly bar + line charts for both sensors. Red bars = dry-season months (Nov–Mar); blue bars = wet-season months. Bars show mean WQI; black line shows mean conductivity.

How to read it: You're looking for the red bars to have higher conductivity (black line) than blue bars. The taller the conductivity line in red-bar months, the stronger the dry-season signal.

Key finding: The conductivity line is systematically higher in red months for both sensors. Ganga conductivity peaks at ~542 µS/cm in Jan 2020 vs a low of ~5 µS/cm in May 2019. Crucially, WQI does not show the same clean seasonal pattern — conductivity is a better proxy for physical riverbed disturbance (like mining) than the composite WQI index.

## fig_kumbh_mela_effect.png
What it shows: Daily WQI time series for both sensors with the Kumbh Mela period highlighted in red, and horizontal dashed lines for Kumbh vs non-Kumbh mean WQI.

How to read it: The gap between the two dashed lines shows the Kumbh "pollution premium." Note: the sensor had a data gap through most of Feb–Mar 2019, so only the very beginning of the Kumbh window (Jan 12–14) has readings.

Key finding: The pre-Kumbh baseline (Jan 12, 3 days before the event) already shows WQI ≈ 48 ("Very Poor") — the Ganga at Prayagraj was heavily polluted before the mass gathering. This implicates year-round upstream industrial and urban discharge, not just festival activity.

## fig_sensor_correlation.png
What it shows: Left panel — scatter of Ganga vs Sangam daily conductivity with an OLS trend line and a colour gradient showing time (Jan 2019 = dark, Feb 2020 = light). Right panel — Ganga daily conductivity over time with red dots marking statistical anomalies (|z-score| > 2).

How to read it: Left: points tightly along the diagonal = sensors agree. Colour gradient shows whether agreement is consistent across the monitoring period. Right: red dots flag days where conductivity or WQI was unusually high or low.

Key finding: WQI, DO, pH and temperature are all strongly correlated (r > 0.89) between sensors. Conductivity correlation is weaker (r=0.37, ns), reflecting that the Sangam sees Yamuna inputs that the Ganga-only sensor doesn't capture. Three anomaly days were detected: Jul 22–23 (WQI spike — possibly a monsoon flush event) and Dec 31 (conductivity spike — possibly year-end industrial discharge or new-year crowd activity at the ghats).

## fig_conductivity_mining_seasonal.png
What it shows: Dual-axis monthly chart. Bars show mean Ganga conductivity by month (red = dry-season months, blue = wet); the black line with markers shows total national mining incidents by month from the no_mobs dataset.

How to read it: This is the central "demand meets supply" visual for water quality. If conductivity and mining incidents both peak in the same months, the bars and the line should be highest at the same positions on the x-axis.

Key finding: Both conductivity and mining incidents peak in the Nov–Feb window and are lowest in May–Jun (pre-monsoon transition). Monthly Spearman ρ = 0.54 (p=0.089 — marginal). The alignment is directionally clear even if not formally significant at the 5% level given only 12 monthly data points.

## fig_ganga_decomposition.png
What it shows: Four-panel seasonal decomposition (additive model, 30-day period) of Ganga daily conductivity. Panels from top: observed, trend, seasonal cycle, residual.

How to read it: The trend panel shows the slow drift over the year, stripping out the recurring monthly cycle. The seasonal panel isolates the repeating 30-day pattern. The residual shows what's left after both are removed — unexplained spikes.

Key finding: The trend rises steeply from Jan 2019 (Kumbh dilution effect) through late 2019, then stabilises into the Feb 2020 dry-season peak (+1.37 µS/cm/day average). The seasonal component shows a consistent monthly oscillation — higher conductivity in the latter half of each month (possibly tied to upstream agricultural or industrial discharge cycles). The largest residuals coincide with the Jul 2019 WQI anomaly and the Dec 31 spike.