from pydantic import BaseModel
from typing import List, Dict

class ExperimentInputs(BaseModel):
    mixture_type: str
    particle_size: float
    solubility: float
    density_difference: float
    magnetic_property: str
    filtration_medium: str
    evaporation_temperature: float
    solvent_volume: float
    impurity_percentage: float
    manual_efficiency: str
    separation_time: float

    seed: int | None = None

class FinalState(BaseModel):
    separated_mass: float
    purity_level: float
    remaining_impurity: float
    method_used: str

class Timeline(BaseModel):
    t: List[float]
    separation_efficiency: List[float]
    remaining_impurity: List[float]
    separated_mass: List[float]

class SimulationResult(BaseModel):
    final_state: FinalState
    timeline: Timeline
    visual: Dict

class TrainingRow(BaseModel):
    inputs: Dict[str, float]
    outputs: Dict[str, float]

class ModelPrediction(BaseModel):
    predicted_params: Dict[str, float]
