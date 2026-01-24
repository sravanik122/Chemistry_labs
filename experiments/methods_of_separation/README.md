# Methods of Separation of Substances

## Input Parameters

- **mixture_type** – Type of mixture (solid–solid / solid–liquid)  
- **particle_size** – Average particle size in the mixture (µm)  
- **solubility** – Solubility of the solid component (g/100 ml)  
- **density_difference** – Density difference between components (kg/m³)  
- **magnetic_property** – Magnetic or non-magnetic nature of the substance  
- **filtration_medium** – Medium used for filtration (cloth / filter paper / sieve)  
- **evaporation_temperature** – Temperature used for evaporation (°C)  
- **solvent_volume** – Volume of solvent present (ml)  
- **impurity_percentage** – Initial impurity percentage (%)  
- **manual_efficiency** – Human handling efficiency (low / medium / high)  
- **separation_time** – Total time allowed for separation (s)  

## Output Parameters

### Final State

- **separated_mass** – Mass of substance successfully separated (kg)  
- **purity_level** – Purity of the final substance (%)  
- **remaining_impurity** – Impurity remaining after separation (%)  
- **method_used** – Most effective separation method applied  

### Timeline

- **t** – Time values (s)  
- **separation_efficiency** – Separation efficiency over time  
- **remaining_impurity** – Impurity percentage over time  
- **separated_mass** – Separated mass over time  

## Frontend Visualization

- Show a **beaker or container** with particles gradually separating over time.  
- Highlight the **active separation method** (filter, magnet, evaporation dish).  
- Reduce visible particles as `remaining_impurity` decreases.  
- Use a simple **progress bar or line graph** to show separation efficiency vs time.
