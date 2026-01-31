from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class ExperimentInputs(BaseModel):
    substance_type: str = Field(..., description="Type of substance")

    temperature: float = Field(..., ge=-50, le=300, description="Temperature (°C)")
    pressure: float = Field(..., ge=0.5, le=10, description="Pressure (atm)")
    reaction_time: float = Field(..., ge=1, le=600, description="Reaction duration (s)")

    reversibility: bool = Field(..., description="Whether change is reversible")

    energy_change: float = Field(..., ge=-5000, le=5000, description="Energy change (J)")

    catalyst_presence: bool = Field(..., description="Presence of catalyst")

    physical_state: str = Field(..., description="Initial physical state")

    mass_change: float = Field(..., ge=-50, le=50, description="Mass change (g)")

    environment: str = Field(..., description="Environmental condition")

    total_time: float = Field(default=60, description="Total simulation time (s)")
    sampling_interval: float = Field(default=1.0, description="Sampling interval (s)")

    seed: Optional[int] = Field(default=None, description="Random seed")

class FinalState(BaseModel):
    change_type: str
    final_state: str
    mass_loss_or_gain: float
    energy_released_or_absorbed: float
    reversibility_status: bool

class Timeline(BaseModel):
    t: List[float]

    reaction_progress: List[float]
    temperature_change: List[float]
    mass_change: List[float]
    energy_change: List[float]

class SimulationResult(BaseModel):
    final_state: FinalState
    timeline: Timeline
    visual: Dict

class TrainingRow(BaseModel):
    inputs: Dict[str, float]
    outputs: Dict[str, float]

class ModelPrediction(BaseModel):
    predicted_params: Dict[str, float]
    timeline: Timeline
