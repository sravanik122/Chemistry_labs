# Physical and Chemical Changes

## Input Parameters

- substance_type – Type of substance involved (solid / liquid / gas)
- temperature – Temperature of the system (°C)
- pressure – Applied pressure (kPa)
- reaction_time – Duration of the process (s)
- reversibility – Whether the change is reversible (true / false)
- energy_change – Energy absorbed or released (kJ)
- catalyst_presence – Presence of catalyst (true / false)
- physical_state – Initial physical state (solid / liquid / gas)
- mass_change – Change in mass during reaction (g)
- environment – Surrounding condition (open / closed / inert)

## Output Parameters

### Final State

- change_type – Physical or chemical change classification
- reaction_extent – Degree of reaction completion (%)
- final_energy – Final energy level (kJ)
- final_mass – Final mass after change (g)
- stability_index – Stability of final substance (0–1)

### Timeline

- t – Time values (s)
- energy_change – Energy variation over time (kJ)
- mass_change – Mass variation over time (g)
- reaction_extent – Reaction progress over time (%)

## Frontend Visualization

- Display substance state changes using simple color or shape transitions.
- Show temperature and energy changes using line graphs.
- Animate mass variation as gradual increase or decrease.
- Indicate physical or chemical change using labels or icons.
- Plot reaction progress versus time for better understanding.
