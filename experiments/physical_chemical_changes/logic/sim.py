import json
import os
import random
import math
from typing import List

from .types import (
    ExperimentInputs,
    FinalState,
    Timeline,
    SimulationResult,
    TrainingRow
)

from .helpers import (
    set_random_seed,
    clamp,
    temperature_factor,
    pressure_factor,
    catalyst_factor,
    environment_factor,
    moving_average
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "../config/sim_config.json")

with open(CONFIG_PATH, "r") as f:
    SIM_CONFIG = json.load(f)

NOISE_SIGMA = SIM_CONFIG["noise_sigma"]
CONSTANTS = SIM_CONFIG["constants"]
VISUAL = SIM_CONFIG["visual"]

PHYSICAL_THRESHOLD = CONSTANTS["physical_change_threshold"]
CHEMICAL_THRESHOLD = CONSTANTS["chemical_change_threshold"]

ENERGY_RELEASE = CONSTANTS["energy_release_factor"]
ENERGY_ABSORB = CONSTANTS["energy_absorption_factor"]

MASS_TOL = CONSTANTS["mass_conservation_tolerance"]
CATALYST_FACTOR = CONSTANTS["catalyst_effect_factor"]

ENV_EFFECT = CONSTANTS["environment_effect"]

def compute_change_score(inputs: ExperimentInputs) -> float:
    """
    Compute score to classify physical vs chemical change.
    """

    temp_eff = temperature_factor(inputs.temperature)
    press_eff = pressure_factor(inputs.pressure)
    cat_eff = catalyst_factor(inputs.catalyst_presence)
    env_eff = environment_factor(inputs.environment)

    energy_eff = abs(inputs.energy_change) / 5000
    mass_eff = abs(inputs.mass_change) / 50

    score = (
        temp_eff * 0.25 +
        press_eff * 0.15 +
        cat_eff * 0.15 +
        energy_eff * 0.25 +
        mass_eff * 0.15 +
        env_eff * 0.05
    )

    return clamp(score, 0.0, 1.0)

def classify_change(score: float) -> str:
    """
    Classify change type.
    """

    if score < PHYSICAL_THRESHOLD:
        return "physical"
    elif score > CHEMICAL_THRESHOLD:
        return "chemical"
    else:
        return "mixed"

def simulate_at_time(inputs: ExperimentInputs, t: float) -> FinalState:
    """
    Compute final state at time t.
    """

    score = compute_change_score(inputs)
    change_type = classify_change(score)

    progress = min(1.0, t / inputs.reaction_time)

    mass_final = inputs.mass_change * progress
    energy_final = inputs.energy_change * progress

    if change_type == "chemical":
        final_state = "new substance formed"
    elif change_type == "physical":
        final_state = "state changed"
    else:
        final_state = "partial transformation"

    confidence = not inputs.reversibility

    return FinalState(
        change_type=change_type,
        final_state=final_state,
        mass_loss_or_gain=mass_final,
        energy_released_or_absorbed=energy_final,
        reversibility_status=inputs.reversibility
    )

def simulate(inputs: ExperimentInputs) -> SimulationResult:
    """
    Run full simulation.
    """

    set_random_seed(inputs.seed)

    total_time = inputs.total_time
    dt = inputs.sampling_interval

    steps = int(total_time / dt) + 1

    t_vals = []
    progress_vals = []
    temp_vals = []
    mass_vals = []
    energy_vals = []

    score = compute_change_score(inputs)

    noise_level = NOISE_SIGMA

    for i in range(steps):

        t = i * dt

        progress = min(1.0, t / inputs.reaction_time)

        # Temperature evolution
        temp = inputs.temperature * (0.8 + 0.2 * progress)

        # Mass change
        mass = inputs.mass_change * progress

        # Energy change
        if inputs.energy_change >= 0:
            energy = inputs.energy_change * ENERGY_RELEASE * progress
        else:
            energy = inputs.energy_change * ENERGY_ABSORB * progress

        # Add noise
        temp += random.gauss(0, noise_level * 10)
        mass += random.gauss(0, noise_level)
        energy += random.gauss(0, noise_level * 50)

        temp = clamp(temp, -100, 400)

        t_vals.append(t)
        progress_vals.append(progress)
        temp_vals.append(temp)
        mass_vals.append(mass)
        energy_vals.append(energy)

    # Smooth curves
    progress_vals = moving_average(progress_vals, 3)
    temp_vals = moving_average(temp_vals, 3)
    mass_vals = moving_average(mass_vals, 3)
    energy_vals = moving_average(energy_vals, 3)

    final_state = simulate_at_time(inputs, total_time)

    timeline = Timeline(
        t=t_vals,
        reaction_progress=progress_vals,
        temperature_change=temp_vals,
        mass_change=mass_vals,
        energy_change=energy_vals
    )

    visual = {
        "show_state_transition": VISUAL["show_state_transition"],
        "show_energy_meter": VISUAL["show_energy_meter"],
        "show_mass_scale": VISUAL["show_mass_scale"],
        "show_change_label": True
    }

    return SimulationResult(
        final_state=final_state,
        timeline=timeline,
        visual=visual
    )

def generate_teacher_dataset(
    inputs_list: List[ExperimentInputs]
) -> List[TrainingRow]:
    """
    Generate dataset for ML training.
    """

    dataset = []

    for inputs in inputs_list:

        result = simulate(inputs)

        input_row = {
            "temperature": inputs.temperature,
            "pressure": inputs.pressure,
            "reaction_time": inputs.reaction_time,
            "energy_change": inputs.energy_change,
            "mass_change": inputs.mass_change,
            "catalyst": int(inputs.catalyst_presence)
        }

        output_row = {
            "progress": result.timeline.reaction_progress[-1],
            "energy": result.final_state.energy_released_or_absorbed,
            "mass": result.final_state.mass_loss_or_gain
        }

        dataset.append(
            TrainingRow(
                inputs=input_row,
                outputs=output_row
            )
        )

    return dataset
