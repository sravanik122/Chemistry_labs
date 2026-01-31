from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict

from .logic.types import ExperimentInputs
from .logic.sim import (
    simulate,
    generate_teacher_dataset
)
from .logic.ai import (
    train_model,
    load_trained_model,
    predict
)

app = FastAPI(
    title="Physical and Chemical Changes API",
    version="1.0.0"
)

class TrainRequest(BaseModel):
    samples: List[ExperimentInputs]
    input_keys: List[str]
    output_keys: List[str]

class PredictRequest(BaseModel):
    inputs: Dict[str, float]
    input_keys: List[str]

@app.post("/simulate")
def run_simulation(inputs: ExperimentInputs):
    """
    Run scientific simulation
    """

    try:
        result = simulate(inputs)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/train")
def train_ai_model(request: TrainRequest):
    """
    Train ML model
    """

    try:
        dataset = generate_teacher_dataset(request.samples)

        history = train_model(
            training_data=dataset,
            input_keys=request.input_keys,
            output_keys=request.output_keys
        )

        return {
            "status": "success",
            "training_history": history
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict")
def run_prediction(request: PredictRequest):
    """
    Predict using trained model
    """

    try:
        model = load_trained_model()

        prediction = predict(
            model=model,
            inputs=request.inputs,
            input_keys=request.input_keys
        )

        return {
            "status": "success",
            "prediction": prediction
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
