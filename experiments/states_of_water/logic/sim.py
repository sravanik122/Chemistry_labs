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
    phase_from_temperature,
    pressure_adjusted_boiling_point,
    insulation_effect,
    surface_area_effect,
    linear_temperature_change,
    energy_loss_factor,
    smooth_series
)

CONFIG_PATH = Path(__file__).parents[1] / "config" / "sim_config.json"

with open(CONFIG_PATH, "r") as f:
    CONFIG = json.load(f)

def simulate(inputs: ExperimentInputs) -> SimulationResult:
    """
    Deterministic simulation for changes in states of water.
    """

    set_seed(inputs.seed)

    sampling_interval = (
        inputs.sampling_interval
        if inputs.sampling_interval is not None
        else CONFIG["default_sampling_interval"]
    )

    total_time = inputs.observation_duration
    noise_sigma = CONFIG["noise_sigma"]

    freezing_point = CONFIG["constants"]["freezing_point"]
    boiling_point = CONFIG["constants"]["boiling_point"]
    pressure_factor = CONFIG["constants"]["pressure_effect_factor"]

    adjusted_boiling = pressure_adjusted_boiling_point(
        boiling_point,
        inputs.pressure,
        pressure_factor
    )

    temperature = inputs.temperature
    energy_absorbed = 0.0

    heating_rate = insulation_effect(
        inputs.heating_rate,
        inputs.container_insulation
    )

    heating_rate = surface_area_effect(
        heating_rate,
        inputs.surface_area_exposed
    )

    cooling_rate = inputs.cooling_rate

    A = (adjusted_boiling - freezing_point) / (
        CONFIG["default_input_ranges"]["temperature"][1] - freezing_point
    )

    k = clamp(heating_rate - cooling_rate, 0.01, 5.0)

    times = []
    temperatures = []
    states = []
    energies = []

    t = 0.0
    while t <= total_time:

        delta_temp = linear_temperature_change(
            0.0,
            k,
            sampling_interval
        )

        temperature += delta_temp
        temperature -= cooling_rate * sampling_interval

        # Noise
        temperature += random.gauss(0, noise_sigma)

        temperature = clamp(
            temperature,
            CONFIG["default_input_ranges"]["temperature"][0],
            CONFIG["default_input_ranges"]["temperature"][1]
        )

        # Energy absorbed
        energy_absorbed += inputs.heat_supplied * sampling_interval / total_time
        energy_absorbed = energy_loss_factor(
            energy_absorbed,
            inputs.energy_loss
        )

        current_state = phase_from_temperature(
            temperature,
            freezing_point,
            adjusted_boiling
        )

        times.append(t)
        temperatures.append(temperature)
        states.append(current_state)
        energies.append(energy_absorbed)

        t += sampling_interval

    # Smooth curves for frontend
    temperatures = smooth_series(temperatures)
    energies = smooth_series(energies)

    final_temperature = temperatures[-1]
    final_state_name = states[-1]

    phase_fraction = clamp(
        (final_temperature - freezing_point) /
        (adjusted_boiling - freezing_point),
        0.0,
        1.0
    )

    final_state = FinalState(
        final_temperature=final_temperature,
        current_state=final_state_name,
        energy_absorbed=energies[-1],
        phase_fraction=phase_fraction
    )

    timeline = Timeline(
        t=times,
        temperature=temperatures,
        state=states,
        energy_absorbed=energies
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
        int(t / (inputs.sampling_interval or CONFIG["default_sampling_interval"])),
        len(result.timeline.t) - 1
    )

    return FinalState(
        final_temperature=result.timeline.temperature[index],
        current_state=result.timeline.state[index],
        energy_absorbed=result.timeline.energy_absorbed[index],
        phase_fraction=clamp(
            (result.timeline.temperature[index] -
             CONFIG["constants"]["freezing_point"]) /
            (CONFIG["constants"]["boiling_point"] -
             CONFIG["constants"]["freezing_point"]),
            0.0,
            1.0
        )
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
                    "temperature": inputs.temperature,
                    "pressure": inputs.pressure,
                    "heating_rate": inputs.heating_rate,
                    "cooling_rate": inputs.cooling_rate,
                    "mass_of_water": inputs.mass_of_water
                },
                outputs={
                    "final_temperature": result.final_state.final_temperature,
                    "energy_absorbed": result.final_state.energy_absorbed
                }
            )
        )

    return dataset
