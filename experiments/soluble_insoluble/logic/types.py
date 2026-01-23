from typing import List, Dict, Optional
from pydantic import BaseModel

class ExperimentInputs(BaseModel):
    solute_type: str
    solvent_type: str
    solute_mass: float
    solvent_volume: float
    temperature: float
    particle_size: float
    stirring_speed: float
    time_of_mixing: float
    saturation_level: float
    impurity_level: float
    pressure: float
    agitation_mode: str

    sampling_interval: Optional[float] = None
    seed: Optional[int] = None

class FinalState(BaseModel):
    dissolved_fraction: float
    undissolved_mass: float
    solution_concentration: float
    solution_type: str

class Timeline(BaseModel):
    t: List[float]
    dissolved_fraction: List[float]
    turbidity_level: List[float]
    concentration: List[float]

class SimulationResult(BaseModel):
    final_state: FinalState
    timeline: Timeline
    visual: Dict

class TrainingRow(BaseModel):
    inputs: Dict[str, float]
    outputs: Dict[str, float]

class ModelPrediction(BaseModel):
    predicted_params: Dict[str, float]
