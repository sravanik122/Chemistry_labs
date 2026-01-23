import math
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
    Clamp value within a range.
    """
    return max(min_value, min(value, max_value))

def temperature_factor(
    temperature: float,
    reference_temperature: float,
    sensitivity: float
) -> float:
    """
    Calculate temperature influence on solubility.
    """
    return max(0.0, 1 + sensitivity * (temperature - reference_temperature))

def pressure_factor(pressure: float, reference_pressure: float = 1.0) -> float:
    """
    Calculate pressure influence on solubility.
    """
    return max(0.5, pressure / reference_pressure)

def stirring_factor(stirring_speed: float, max_speed: float = 500.0) -> float:
    """
    Calculate stirring efficiency factor.
    """
    return clamp(stirring_speed / max_speed, 0.0, 1.5)

def particle_size_factor(particle_size: float) -> float:
    """
    Smaller particles dissolve faster.
    """
    if particle_size <= 0:
        return 1.0
    return clamp(1.0 / particle_size, 0.2, 2.0)

def solubility_limit(
    base_limit: float,
    temperature_factor: float,
    pressure_factor: float,
    impurity_level: float
) -> float:
    """
    Compute effective solubility limit.
    """
    impurity_penalty = 1 - impurity_level / 100
    return max(
        0.0,
        base_limit * temperature_factor * pressure_factor * impurity_penalty
    )

def dissolution_rate(
    stirring_factor: float,
    particle_factor: float,
    agitation_efficiency: float
) -> float:
    """
    Calculate dissolution speed multiplier.
    """
    return stirring_factor * particle_factor * agitation_efficiency

def smooth_series(values: List[float], alpha: float = 0.15) -> List[float]:
    """
    Apply exponential smoothing to time-series data.
    """
    if not values:
        return []

    smoothed = [values[0]]
    for v in values[1:]:
        smoothed.append(alpha * v + (1 - alpha) * smoothed[-1])

    return smoothed
