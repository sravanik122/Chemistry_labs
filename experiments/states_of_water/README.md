# Changes in States of Water

## Input Parameters 

- **temperature** – Initial temperature of water (°C)  
- **pressure** – Ambient pressure acting on water (atm)  
- **heating_rate** – Rate at which heat is supplied (°C/s)  
- **cooling_rate** – Rate at which heat is removed (°C/s)  
- **mass_of_water** – Mass of water used in the experiment (kg)  
- **surface_area_exposed** – Surface area exposed to surroundings (cm²)  
- **heat_supplied** – Total heat energy supplied to water (J)  
- **energy_loss** – Percentage of energy lost to surroundings (%)  
- **container_insulation** – Insulation level of container (none / low / medium / high)  
- **observation_duration** – Total duration of observation (s)  
- **sampling_interval** – Time interval between observations (s)  
- **seed** – Random seed for reproducibility (optional)  

## Output Parameters

### Final State

- **final_temperature** – Temperature at the end of the experiment (°C)  
- **current_state** – Final state of water (solid / liquid / gas)  
- **energy_absorbed** – Total energy absorbed by water (J)  
- **phase_fraction** – Fraction indicating progress toward next phase (0–1)  

### Timeline

- **t** – Time values (s)  
- **temperature** – Temperature variation over time (°C)  
- **state** – State of water at each time step  
- **energy_absorbed** – Energy absorbed over time (J)  

## Frontend Visualization

- Represent water visually as **ice, liquid, or vapor** based on the `state` output.  
- Animate **temperature vs time** using a simple line graph.  
- Show smooth transitions between states using gradual visual changes as `phase_fraction` increases.  
- Display energy absorption using a **progress bar or numeric counter** for better understanding.
