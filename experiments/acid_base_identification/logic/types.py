from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class ExperimentInputs(BaseModel):
    substance_type: str = Field(..., description="Nature of the test substance")
    indicator_type: str = Field(..., description="Indicator used for testing")

    concentration: float = Field(..., ge=0.01, le=5.0, description="Solution concentration (mol/L)")
    temperature: float = Field(..., ge=5, le=80, description="Solution temperature (°C)")
    volume: float = Field(..., ge=1, le=500, description="Solution volume (ml)")
    purity: float = Field(..., ge=0, le=100, description="Purity percentage")

    reaction_time: float = Field(..., ge=1, le=300, description="Reaction time (seconds)")
    dilution_factor: float = Field(..., ge=1, le=10, description="Dilution factor")

    pH_range: float = Field(..., ge=0, le=14, description="Expected pH range")
    observation_accuracy: str = Field(..., description="Observation accuracy level")

    total_time: float = Field(default=60, description="Total simulation time (s)")
    sampling_interval: float = Field(default=1.0, description="Sampling interval (s)")

    seed: Optional[int] = Field(default=None, description="Random seed")

class FinalState(BaseModel):
    final_pH: float
    substance_nature: str
    indicator_color: str
    confidence_level: float

class Timeline(BaseModel):
    t: List[float]

    pH: List[float]
    color_intensity: List[float]
    reaction_progress: List[float]

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
