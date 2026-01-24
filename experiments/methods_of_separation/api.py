from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict

from .logic.types import (
    ExperimentInputs,
    SimulationResult,
    TrainingRow,
    ModelPrediction
)
from .logic.sim import simulate, generate_teacher_dataset
from .logic.ai import train_model, load_model, predict


app = FastAPI(
    title="Methods of Separation of Substances API",
    version="1.0.0"
)

class TrainRequest(BaseModel):
    inputs_list: List[ExperimentInputs]
    input_keys: List[str]
    output_keys: List[str]

class PredictRequest(BaseModel):
    model_path: str
    input_data: Dict[str, float]
    input_keys: List[str]
    output_keys: List[str]

@app.post("/simulate", response_model=SimulationResult)
def simulate_experiment(inputs: ExperimentInputs):
    """
    Run deterministic simulation for separation of substances.
    """
    return simulate(inputs)

@app.post("/train")
def train_experiment(request: TrainRequest):
    """
    Train ML model using simulation-generated dataset.
    """
    dataset = generate_teacher_dataset(request.inputs_list)

    history = train_model(
        training_data=dataset,
        input_keys=request.input_keys,
        output_keys=request.output_keys
    )

    return {
        "status": "training_completed",
        "history": history
    }

@app.post("/predict", response_model=ModelPrediction)
def predict_experiment(request: PredictRequest):
    """
    Predict compact separation parameters using trained model.
    """
    model = load_model(request.model_path)

    prediction = predict(
        model=model,
        input_data=request.input_data,
        input_keys=request.input_keys,
        output_keys=request.output_keys
    )

    return prediction
