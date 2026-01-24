from typing import List, Dict, Optional
from pydantic import BaseModel

class ExperimentInputs(BaseModel):
    initial_state: str
    temperature: float
    pressure: float
    mass_of_water: float
    heating_rate: float
    cooling_rate: float
    heat_supplied: float
    container_material: str
    container_insulation: str
    surface_area_exposed: float
    ambient_conditions: str
    energy_loss: float
    observation_duration: float

    sampling_interval: Optional[float] = None
    seed: Optional[int] = None

class FinalState(BaseModel):
    final_temperature: float
    current_state: str
    energy_absorbed: float
    phase_fraction: float


class Timeline(BaseModel):
    t: List[float]
    temperature: List[float]
    state: List[str]
    energy_absorbed: List[float]

class SimulationResult(BaseModel):
    final_state: FinalState
    timeline: Timeline
    visual: Dict

class TrainingRow(BaseModel):
    inputs: Dict[str, float]
    outputs: Dict[str, float]

class ModelPrediction(BaseModel):
    predicted_params: Dict[str, float]
