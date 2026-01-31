# Identification of Acids, Bases, and Neutral Substances

## Input Parameters

- substance_type – Nature of the substance (acid / base / neutral / unknown)
- indicator_type – Type of indicator used (litmus / phenolphthalein / methyl_orange / universal)
- concentration – Concentration of the solution (mol/L)
- temperature – Temperature of the solution (°C)
- volume – Volume of the solution (ml)
- purity – Purity level of the substance (%)
- reaction_time – Time allowed for indicator reaction (s)
- dilution_factor – Factor by which the solution is diluted
- pH_range – Expected pH range (0–14)
- observation_accuracy – Accuracy of observation (low / medium / high)

## Output Parameters

### Final State

- final_pH – Final measured pH value
- substance_nature – Identified nature of substance (acid / base / neutral)
- indicator_color – Observed color of the indicator
- confidence_level – Confidence in identification (0–1)

### Timeline

- t – Time values (s)
- pH – pH variation over time
- color_intensity – Indicator color intensity over time
- reaction_progress – Reaction completion over time

## Frontend Visualization

- Display a beaker or test tube with liquid whose color changes based on indicator output.
- Show a digital pH meter updating in real time.
- Animate gradual color change as the reaction progresses.
- Plot a simple graph of pH versus time beside the experiment view.
