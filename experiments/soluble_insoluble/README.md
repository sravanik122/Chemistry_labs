# Soluble & Insoluble Substances

## Input Parameters
- **solute_type** – Type of solute (sugar / salt / sand / chalk / oil)
- **solvent_type** – Type of solvent (water / alcohol / oil)
- **solute_mass (g)** – Mass of solute added
- **solvent_volume (ml)** – Volume of solvent
- **temperature (°C)** – Temperature of the solvent
- **particle_size (mm)** – Size of solute particles
- **stirring_speed (rpm)** – Speed of stirring
- **time_of_mixing (s)** – Duration of mixing
- **saturation_level (%)** – Maximum allowed saturation
- **impurity_level (%)** – Percentage of impurities
- **pressure (atm)** – Environmental pressure
- **agitation_mode** – Method of agitation (none / manual / magnetic)

## Output Parameters

### Final State
- **dissolved_fraction** – Fraction of solute dissolved
- **undissolved_mass (g)** – Remaining undissolved solute
- **solution_concentration** – Concentration of dissolved solute
- **solution_type** – Unsaturated or saturated solution

### Timeline
- **t (s)** – Time values
- **dissolved_fraction** – Dissolved fraction over time
- **turbidity_level** – Cloudiness of solution over time
- **concentration** – Concentration variation over time

## Frontend Visualization
- Show solute particles **gradually reducing** as they dissolve.
- Display **remaining particles at the bottom** for insoluble substances.
- Use **slight cloudiness** to represent turbidity.
- Plot **dissolved fraction vs time** to show dissolution progress.
- Indicate **saturation state** using a simple label or color change.
