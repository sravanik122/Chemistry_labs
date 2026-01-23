from fastapi import FastAPI
from typing import List, Dict

from .logic.types import ExperimentInputs, SimulationResult, TrainingRow
from .logic.sim import simulate, generate_teacher_dataset
from .logic.ai import train_model, load_model, predict

app = FastAPI(
    title="Soluble & Insoluble Substances",
    description="Simulation and ML API for solubility experiments",
    version="1.0.0"
)

MODEL_PATH = "./logs/soluble_insoluble_model/model.keras"

@app.post("/simulate", response_model=SimulationResult)
def run_simulation(inputs: ExperimentInputs):
    """
    Run deterministic solubility simulation.
    """
    return simulate(inputs)

@app.post("/train")
def train_ml_model(
    inputs_list: List[ExperimentInputs],
    input_keys: List[str],
    output_keys: List[str]
):
    """
    Train regression ML model using simulation-generated data.
    """
    dataset = generate_teacher_dataset(inputs_list)

    history = train_model(
        training_data=dataset,
        input_keys=input_keys,
        output_keys=output_keys
    )

    return {
        "status": "training_completed",
        "history": history
    }

@app.post("/predict")
def predict_outcome(
    input_data: Dict[str, float],
    input_keys: List[str],
    output_keys: List[str]
):
    """
    Predict dissolution parameters using trained model.
    """
    model = load_model(MODEL_PATH)

    prediction = predict(
        model=model,
        input_data=input_data,
        input_keys=input_keys,
        output_keys=output_keys
    )

    return prediction
