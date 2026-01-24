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
    Clamp a value between minimum and maximum limits.
    """
    return max(min_value, min(value, max_value))

def linear_decay(initial: float, rate: float, time_step: float) -> float:
    """
    Compute linear decay over a time step.
    """
    return max(0.0, initial - rate * time_step)


def exponential_decay(initial: float, rate: float, time_step: float) -> float:
    """
    Compute exponential decay over a time step.
    """
    return initial * (1 - rate * time_step)

def filtration_factor(particle_size: float, threshold: float = 300.0) -> float:
    """
    Estimate filtration effectiveness based on particle size.
    """
    return clamp(1 - (particle_size / threshold), 0.0, 1.0)

def sedimentation_factor(density_difference: float, max_density: float = 5000.0) -> float:
    """
    Estimate sedimentation efficiency from density difference.
    """
    return clamp(density_difference / max_density, 0.0, 1.0)

def evaporation_factor(temperature: float, reference_temp: float = 100.0) -> float:
    """
    Estimate evaporation effectiveness based on temperature.
    """
    return clamp(temperature / reference_temp, 0.0, 1.0)

def magnetic_factor(property_type: str) -> float:
    """
    Magnetic separation effectiveness.
    """
    return 1.0 if property_type == "magnetic" else 0.0

def manual_efficiency_factor(level: str) -> float:
    """
    Human handling efficiency.
    """
    mapping = {
        "low": 0.6,
        "medium": 0.8,
        "high": 0.95
    }
    return mapping.get(level, 0.8)

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
