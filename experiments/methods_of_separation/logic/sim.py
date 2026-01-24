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
    clamp,
    filtration_factor,
    sedimentation_factor,
    evaporation_factor,
    magnetic_factor,
    manual_efficiency_factor,
    smooth_series
)

CONFIG_PATH = Path(__file__).parents[1] / "config" / "sim_config.json"

with open(CONFIG_PATH, "r") as f:
    CONFIG = json.load(f)

def simulate(inputs: ExperimentInputs) -> SimulationResult:
    """
    Deterministic simulation for separation of substances.
    """

    set_seed(inputs.seed)

    sampling_interval = CONFIG["default_sampling_interval"]
    total_time = inputs.separation_time
    noise_sigma = CONFIG["noise_sigma"]

    scores = {
        "filtration": filtration_factor(inputs.particle_size),
        "sedimentation": sedimentation_factor(inputs.density_difference),
        "evaporation": evaporation_factor(inputs.evaporation_temperature),
        "magnetic": magnetic_factor(inputs.magnetic_property)
    }

    method_used = max(scores, key=scores.get)
    base_efficiency = scores[method_used]

    manual_eff = manual_efficiency_factor(inputs.manual_efficiency)

    A = clamp(
        base_efficiency * manual_eff,
        0.0,
        1.0
    )

    k = clamp(
        A * 0.8,
        0.05,
        1.0
    )

    t = 0.0
    times = []
    efficiencies = []
    impurities = []
    separated_mass = []

    initial_impurity = inputs.impurity_percentage
    total_mass = inputs.solvent_volume * 0.001  # simple mass proxy (kg)

    while t <= total_time:

        efficiency = A * (1 - pow(2.718, -k * t))
        efficiency += random.gauss(0, noise_sigma)

        efficiency = clamp(efficiency, 0.0, 1.0)

        remaining_impurity = initial_impurity * (1 - efficiency)
        separated = total_mass * efficiency

        times.append(t)
        efficiencies.append(efficiency)
        impurities.append(remaining_impurity)
        separated_mass.append(separated)

        t += sampling_interval

    # Smooth curves for frontend
    efficiencies = smooth_series(efficiencies)
    impurities = smooth_series(impurities)
    separated_mass = smooth_series(separated_mass)

    final_state = FinalState(
        separated_mass=separated_mass[-1],
        purity_level=100 - impurities[-1],
        remaining_impurity=impurities[-1],
        method_used=method_used
    )

    timeline = Timeline(
        t=times,
        separation_efficiency=efficiencies,
        remaining_impurity=impurities,
        separated_mass=separated_mass
    )

    return SimulationResult(
        final_state=final_state,
        timeline=timeline,
        visual=CONFIG["visual"]
    )

def simulate_at_time(inputs: ExperimentInputs, t: float) -> FinalState:
    """
    Compute state at a specific time instant.
    """
    result = simulate(inputs)

    index = min(
        int(t / CONFIG["default_sampling_interval"]),
        len(result.timeline.t) - 1
    )

    return FinalState(
        separated_mass=result.timeline.separated_mass[index],
        purity_level=100 - result.timeline.remaining_impurity[index],
        remaining_impurity=result.timeline.remaining_impurity[index],
        method_used=result.final_state.method_used
    )

def generate_teacher_dataset(
    inputs_list: List[ExperimentInputs]
) -> List[TrainingRow]:
    """
    Generate supervised dataset for ML training.
    """

    dataset = []

    for inputs in inputs_list:
        result = simulate(inputs)

        dataset.append(
            TrainingRow(
                inputs={
                    "particle_size": inputs.particle_size,
                    "density_difference": inputs.density_difference,
                    "solubility": inputs.solubility,
                    "evaporation_temperature": inputs.evaporation_temperature,
                    "impurity_percentage": inputs.impurity_percentage
                },
                outputs={
                    "purity_level": result.final_state.purity_level,
                    "separated_mass": result.final_state.separated_mass
                }
            )
        )

    return dataset
