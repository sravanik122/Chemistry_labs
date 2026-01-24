import random
from typing import List

def set_seed(seed: int | None):
    """
    Set random seed for reproducibility.
    """
    if seed is not None:
        random.seed(seed)

def normalize_input(value: float, min_value: float, max_value: float) -> float:
    """
    Normalize a value to range [0, 1].
    """
    if max_value == min_value:
        return 0.0
    return (value - min_value) / (max_value - min_value)

def clamp(value: float, min_value: float, max_value: float) -> float:
    """
    Clamp value within a specified range.
    """
    return max(min_value, min(value, max_value))

def linear_temperature_change(
    temperature: float,
    rate: float,
    time_step: float
) -> float:
    """
    Compute linear temperature change.
    """
    return temperature + rate * time_step

def energy_loss_factor(energy: float, loss_percent: float) -> float:
    """
    Apply energy loss based on percentage.
    """
    return energy * (1 - loss_percent / 100)

def phase_from_temperature(
    temperature: float,
    freezing_point: float,
    boiling_point: float
) -> str:
    """
    Determine the phase of water based on temperature.
    """
    if temperature < freezing_point:
        return "solid"
    elif temperature < boiling_point:
        return "liquid"
    else:
        return "gas"

def pressure_adjusted_boiling_point(
    boiling_point: float,
    pressure: float,
    factor: float
) -> float:
    """
    Adjust boiling point based on pressure.
    """
    return boiling_point + factor * (pressure - 1.0)

def insulation_effect(
    heating_rate: float,
    insulation_level: str
) -> float:
    """
    Modify heating rate based on insulation.
    """
    insulation_map = {
        "none": 0.8,
        "low": 0.9,
        "medium": 1.0,
        "high": 1.1
    }
    return heating_rate * insulation_map.get(insulation_level, 1.0)

def surface_area_effect(
    rate: float,
    surface_area: float,
    reference_area: float = 100.0
) -> float:
    """
    Adjust heat exchange rate based on exposed surface area.
    """
    return rate * (surface_area / reference_area)

def smooth_series(values: List[float], alpha: float = 0.2) -> List[float]:
    """
    Apply exponential smoothing to time-series data.
    """
    if not values:
        return []

    smoothed = [values[0]]
    for v in values[1:]:
        smoothed.append(alpha * v + (1 - alpha) * smoothed[-1])

    return smoothed
