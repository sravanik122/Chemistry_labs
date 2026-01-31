import json
import os
import math
import random
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
    dilution_factor_effect,
    purity_factor,
    observation_noise_factor,
    moving_average
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "../config/sim_config.json")

with open(CONFIG_PATH, "r") as f:
    SIM_CONFIG = json.load(f)

NOISE_SIGMA = SIM_CONFIG["noise_sigma"]
CONSTANTS = SIM_CONFIG["constants"]
VISUAL = SIM_CONFIG["visual"]

NEUTRAL_PH = CONSTANTS["neutral_pH"]
TEMP_FACTOR = CONSTANTS["temperature_effect_factor"]
DILUTION_FACTOR = CONSTANTS["dilution_effect_factor"]
PURITY_FACTOR = CONSTANTS["purity_effect_factor"]
COLOR_MAP = CONSTANTS["indicator_color_map"]

def compute_base_ph(inputs: ExperimentInputs) -> float:
    """
    Compute base pH based on substance type and concentration.
    """

    if inputs.substance_type == "acid":
        base = 7.0 - math.log10(inputs.concentration + 1)

    elif inputs.substance_type == "base":
        base = 7.0 + math.log10(inputs.concentration + 1)

    elif inputs.substance_type == "neutral":
        base = 7.0

    else:
        base = random.uniform(4.5, 9.5)

    return clamp(base, 0.0, 14.0)

def compute_indicator_color(pH: float, indicator: str) -> str:
    """
    Get indicator color from pH value.
    """

    if pH < 6.5:
        state = "acid"
    elif pH > 7.5:
        state = "base"
    else:
        state = "neutral"

    return COLOR_MAP[indicator][state]

def simulate_at_time(inputs: ExperimentInputs, t: float) -> FinalState:
    """
    Compute final state at given time t.
    """

    base_ph = compute_base_ph(inputs)

    temp_eff = temperature_factor(inputs.temperature)
    dil_eff = dilution_factor_effect(inputs.dilution_factor)
    pur_eff = purity_factor(inputs.purity)

    reaction_progress = min(1.0, t / inputs.reaction_time)

    ph_shift = (
        base_ph
        * temp_eff
        * dil_eff
        * pur_eff
        * reaction_progress
    )

    final_ph = clamp(ph_shift, 0.0, 14.0)

    color = compute_indicator_color(final_ph, inputs.indicator_type)

    confidence = clamp(
        pur_eff * (1 - observation_noise_factor(inputs.observation_accuracy)),
        0.0,
        1.0
    )

    if final_ph < 6.5:
        nature = "acid"
    elif final_ph > 7.5:
        nature = "base"
    else:
        nature = "neutral"

    return FinalState(
        final_pH=final_ph,
        substance_nature=nature,
        indicator_color=color,
        confidence_level=confidence
    )

def simulate(inputs: ExperimentInputs) -> SimulationResult:
    """
    Run full simulation and generate timeline.
    """

    set_random_seed(inputs.seed)

    total_time = inputs.total_time
    dt = inputs.sampling_interval

    steps = int(total_time / dt) + 1

    t_values = []
    ph_values = []
    color_values = []
    progress_values = []

    base_ph = compute_base_ph(inputs)

    temp_eff = temperature_factor(inputs.temperature)
    dil_eff = dilution_factor_effect(inputs.dilution_factor)
    pur_eff = purity_factor(inputs.purity)

    noise_level = observation_noise_factor(inputs.observation_accuracy)

    for i in range(steps):
        t = i * dt

        progress = min(1.0, t / inputs.reaction_time)

        ph = (
            base_ph
            * temp_eff
            * dil_eff
            * pur_eff
            * progress
        )

        noise = random.gauss(0, NOISE_SIGMA + noise_level)
        ph += noise

        ph = clamp(ph, 0.0, 14.0)

        t_values.append(t)
        ph_values.append(ph)
        progress_values.append(progress)

        color_values.append(ph / 14.0)

    # Smooth curves
    ph_values = moving_average(ph_values, 3)
    progress_values = moving_average(progress_values, 3)

    final_state = simulate_at_time(inputs, total_time)

    timeline = Timeline(
        t=t_values,
        pH=ph_values,
        color_intensity=color_values,
        reaction_progress=progress_values
    )

    visual = {
        "show_ph_meter": VISUAL["show_ph_meter"],
        "show_color_transition": VISUAL["show_color_transition"],
        "show_reaction_progress": VISUAL["show_reaction_progress"],
        "color_scale": "0-14"
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
    Generate training dataset for ML.
    """

    dataset = []

    for inputs in inputs_list:

        result = simulate(inputs)

        input_row = {
            "concentration": inputs.concentration,
            "temperature": inputs.temperature,
            "volume": inputs.volume,
            "purity": inputs.purity,
            "reaction_time": inputs.reaction_time,
            "dilution_factor": inputs.dilution_factor
        }

        output_row = {
            "final_pH": result.final_state.final_pH,
            "confidence": result.final_state.confidence_level
        }

        dataset.append(
            TrainingRow(
                inputs=input_row,
                outputs=output_row
            )
        )

    return dataset
