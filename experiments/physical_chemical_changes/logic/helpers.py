import random
import numpy as np
from typing import List

def set_random_seed(seed: int | None = None):
    """
    Set random seed for reproducibility.
    """
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

def normalize_input(value: float, min_value: float, max_value: float) -> float:
    """
    Normalize value to range [0, 1].
    """
    if max_value == min_value:
        return 0.0

    return (value - min_value) / (max_value - min_value)

def denormalize_value(norm_value: float, min_value: float, max_value: float) -> float:
    """
    Convert normalized value back to original scale.
    """
    return norm_value * (max_value - min_value) + min_value

def clamp(value: float, min_val: float, max_val: float) -> float:
    """
    Restrict value within given bounds.
    """
    return max(min_val, min(value, max_val))

def safe_exp(x: float, limit: float = 50) -> float:
    """
    Compute exponential safely.
    """
    return np.exp(min(x, limit))

def moving_average(data: List[float], window: int = 3) -> List[float]:
    """
    Smooth data using moving average.
    """
    if window <= 1:
        return data

    smoothed = []

    for i in range(len(data)):
        start = max(0, i - window + 1)
        subset = data[start:i + 1]

        smoothed.append(sum(subset) / len(subset))

    return smoothed

def linear_interpolate(start: float, end: float, steps: int) -> List[float]:
    """
    Generate linearly interpolated values.
    """
    if steps <= 1:
        return [start]

    return list(np.linspace(start, end, steps))

def temperature_factor(temp: float, optimal: float = 25.0) -> float:
    """
    Calculate temperature influence on reaction rate.
    """
    return max(0.0, 1 - ((temp - optimal) / 50) ** 2)

def pressure_factor(pressure: float, standard: float = 1.0) -> float:
    """
    Calculate pressure influence.
    """
    return clamp(pressure / standard, 0.5, 2.0)

def catalyst_factor(present: bool) -> float:
    """
    Calculate catalyst influence.
    """
    return 1.5 if present else 1.0

def environment_factor(env: str) -> float:
    """
    Calculate environment influence.
    """
    mapping = {
        "open": 0.9,
        "closed": 1.0,
        "controlled": 1.1
    }

    return mapping.get(env, 1.0)
