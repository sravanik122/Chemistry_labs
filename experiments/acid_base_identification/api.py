from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict

from .logic.types import ExperimentInputs, SimulationResult, TrainingRow
from .logic.sim import simulate, generate_teacher_dataset
from .logic.ai import train_model, load_trained_model, predict, params_to_timeline

app = FastAPI(
    title="Identification of Acids, Bases and Neutral Substances",
    description="API for Identification of Acids, Bases, and Neutral Substances",
    version="1.0.0"
)

class TrainRequest(BaseModel):
    inputs_list: List[ExperimentInputs]
    input_keys: List[str]
    output_keys: List[str]

class PredictRequest(BaseModel):
    inputs: Dict[str, float]
    input_keys: List[str]
    total_time: float = 60
    sampling_interval: float = 1.0

@app.post("/simulate", response_model=SimulationResult)
def run_simulation(inputs: ExperimentInputs):
    """
    Run scientific simulation.
    """
    return simulate(inputs)

@app.post("/train")
def train(request: TrainRequest):
    """
    Train ML model using generated dataset.
    """

    dataset = generate_teacher_dataset(request.inputs_list)

    history = train_model(
        training_data=dataset,
        input_keys=request.input_keys,
        output_keys=request.output_keys
    )

    return {
        "status": "success",
        "message": "Model trained successfully",
        "history": history
    }

@app.post("/predict")
def run_prediction(request: PredictRequest):
    """
    Predict using trained ML model and generate timeline.
    """

    model = load_trained_model()

    predicted_params = predict(
        model=model,
        inputs=request.inputs,
        input_keys=request.input_keys
    )

    timeline = params_to_timeline(
        predicted_params=predicted_params,
        total_time=request.total_time,
        sampling_interval=request.sampling_interval
    )

    return {
        "status": "success",
        "predicted_params": predicted_params,
        "timeline": timeline
    }

@app.get("/")
def root():
    return {
        "message": "Acid-Base Identification API is running"
    }
