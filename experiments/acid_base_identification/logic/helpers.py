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

def safe_log(x: float, eps: float = 1e-8) -> float:
    """
    Compute logarithm safely.
    """
    return np.log(max(x, eps))

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
    return max(0.0, 1 - ((temp - optimal) / 30) ** 2)

def dilution_factor_effect(dilution: float) -> float:
    """
    Calculate dilution influence on pH strength.
    """
    return max(0.1, 1.0 / dilution)

def purity_factor(purity: float) -> float:
    """
    Calculate purity influence on reaction.
    """
    return clamp(purity / 100.0, 0.0, 1.0)

def observation_noise_factor(level: str) -> float:
    """
    Map observation accuracy to noise.
    """
    mapping = {
        "low": 0.08,
        "medium": 0.04,
        "high": 0.01
    }

    return mapping.get(level, 0.05)
