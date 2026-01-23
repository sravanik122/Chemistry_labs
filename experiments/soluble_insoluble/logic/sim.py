import json
import random
from pathlib import Path
from typing import List

from .types import (
    ExperimentInputs,
    FinalState,
    Timeline,
    SimulationResult,
    TrainingRow
)
from .helpers import (
    set_seed,
    temperature_factor,
    pressure_factor,
    stirring_factor,
    particle_size_factor,
    solubility_limit,
    dissolution_rate,
    smooth_series,
    clamp
)

CONFIG_PATH = Path(__file__).parents[1] / "config" / "sim_config.json"

with open(CONFIG_PATH, "r") as f:
    CONFIG = json.load(f)

def simulate(inputs: ExperimentInputs) -> SimulationResult:
    """
    Run deterministic simulation for soluble & insoluble substances.
    """

    set_seed(inputs.seed)

    sampling_interval = (
        inputs.sampling_interval
        if inputs.sampling_interval is not None
        else CONFIG["default_sampling_interval"]
    )

    total_time = inputs.time_of_mixing
    noise_sigma = CONFIG["noise_sigma"]

    base_solubility = CONFIG["constants"]["solubility_limits"].get(
        inputs.solute_type, 0.0
    )

    temp_factor = temperature_factor(
        inputs.temperature,
        CONFIG["constants"]["reference_temperature"],
        CONFIG["constants"]["temperature_solubility_factor"].get(
            inputs.solute_type, 0.0
        )
    )

    press_factor = pressure_factor(inputs.pressure)

    effective_solubility = solubility_limit(
        base_solubility,
        temp_factor,
        press_factor,
        inputs.impurity_level
    )

    agitation_efficiency = CONFIG["constants"]["stirring_efficiency"][
        inputs.agitation_mode
    ]

    stir_factor = stirring_factor(inputs.stirring_speed)
    particle_factor = particle_size_factor(inputs.particle_size)

    rate_constant = dissolution_rate(
        stir_factor,
        particle_factor,
        agitation_efficiency
    )

    max_dissolvable_mass = min(
        inputs.solute_mass,
        effective_solubility * inputs.solvent_volume
    )

    A = max_dissolvable_mass / inputs.solute_mass if inputs.solute_mass > 0 else 0.0
    k = rate_constant

    times = []
    dissolved_fractions = []
    turbidity_levels = []
    concentrations = []

    t = 0.0
    while t <= total_time:
        dissolved_fraction = A * (1 - pow(2.71828, -k * t))

        dissolved_fraction = clamp(dissolved_fraction, 0.0, 1.0)

        dissolved_fraction += random.gauss(0, noise_sigma)
        dissolved_fraction = clamp(dissolved_fraction, 0.0, 1.0)

        dissolved_mass = dissolved_fraction * inputs.solute_mass
        concentration = dissolved_mass / inputs.solvent_volume

        turbidity = clamp(
            1.0 - dissolved_fraction + inputs.impurity_level / 100,
            0.0,
            1.0
        )

        times.append(t)
        dissolved_fractions.append(dissolved_fraction)
        turbidity_levels.append(turbidity)
        concentrations.append(concentration)

        t += sampling_interval

    dissolved_fractions = smooth_series(dissolved_fractions)
    turbidity_levels = smooth_series(turbidity_levels)
    concentrations = smooth_series(concentrations)

    final_dissolved_fraction = dissolved_fractions[-1]
    dissolved_mass = final_dissolved_fraction * inputs.solute_mass
    undissolved_mass = inputs.solute_mass - dissolved_mass

    solution_type = (
        "unsaturated"
        if dissolved_mass < max_dissolvable_mass
        else "saturated"
    )

    final_state = FinalState(
        dissolved_fraction=final_dissolved_fraction,
        undissolved_mass=undissolved_mass,
        solution_concentration=concentrations[-1],
        solution_type=solution_type
    )

    timeline = Timeline(
        t=times,
        dissolved_fraction=dissolved_fractions,
        turbidity_level=turbidity_levels,
        concentration=concentrations
    )

    return SimulationResult(
        final_state=final_state,
        timeline=timeline,
        visual=CONFIG["visual"]
    )

def simulate_at_time(inputs: ExperimentInputs, t: float) -> FinalState:
    """
    Compute solution state at a specific time.
    """

    base_solubility = CONFIG["constants"]["solubility_limits"].get(
        inputs.solute_type, 0.0
    )

    temp_factor_val = temperature_factor(
        inputs.temperature,
        CONFIG["constants"]["reference_temperature"],
        CONFIG["constants"]["temperature_solubility_factor"].get(
            inputs.solute_type, 0.0
        )
    )

    press_factor_val = pressure_factor(inputs.pressure)

    effective_solubility = solubility_limit(
        base_solubility,
        temp_factor_val,
        press_factor_val,
        inputs.impurity_level
    )

    max_dissolvable_mass = min(
        inputs.solute_mass,
        effective_solubility * inputs.solvent_volume
    )

    stir_factor = stirring_factor(inputs.stirring_speed)
    particle_factor = particle_size_factor(inputs.particle_size)

    agitation_efficiency = CONFIG["constants"]["stirring_efficiency"][
        inputs.agitation_mode
    ]

    k = dissolution_rate(stir_factor, particle_factor, agitation_efficiency)
    A = max_dissolvable_mass / inputs.solute_mass if inputs.solute_mass > 0 else 0.0

    dissolved_fraction = clamp(
        A * (1 - pow(2.71828, -k * t)),
        0.0,
        1.0
    )

    dissolved_mass = dissolved_fraction * inputs.solute_mass
    undissolved_mass = inputs.solute_mass - dissolved_mass

    concentration = dissolved_mass / inputs.solvent_volume

    solution_type = (
        "unsaturated"
        if dissolved_mass < max_dissolvable_mass
        else "saturated"
    )

    return FinalState(
        dissolved_fraction=dissolved_fraction,
        undissolved_mass=undissolved_mass,
        solution_concentration=concentration,
        solution_type=solution_type
    )

def generate_teacher_dataset(
    inputs_list: List[ExperimentInputs]
) -> List[TrainingRow]:
    """
    Generate supervised learning dataset from simulation.
    """

    dataset = []

    for inputs in inputs_list:
        result = simulate(inputs)

        dataset.append(
            TrainingRow(
                inputs={
                    "solute_mass": inputs.solute_mass,
                    "temperature": inputs.temperature,
                    "stirring_speed": inputs.stirring_speed,
                    "particle_size": inputs.particle_size,
                    "impurity_level": inputs.impurity_level
                },
                outputs={
                    "dissolved_fraction": result.final_state.dissolved_fraction,
                    "solution_concentration": result.final_state.solution_concentration
                }
            )
        )

    return dataset
