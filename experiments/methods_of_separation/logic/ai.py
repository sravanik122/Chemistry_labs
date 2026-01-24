import json
from pathlib import Path
from typing import List, Dict

import numpy as np
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import TensorBoard

from .types import TrainingRow, ModelPrediction

CONFIG_PATH = Path(__file__).parents[1] / "config" / "model_config.json"

with open(CONFIG_PATH, "r") as f:
    MODEL_CONFIG = json.load(f)

def build_model(input_dim: int, output_dim: int) -> tf.keras.Model:
    """
    Build regression MLP model.
    """
    model = Sequential()

    for i, units in enumerate(MODEL_CONFIG["model_layers"]):
        if i == 0:
            model.add(Dense(units, activation="relu", input_shape=(input_dim,)))
        else:
            model.add(Dense(units, activation="relu"))

    model.add(Dense(output_dim, activation="linear"))

    optimizer = Adam(learning_rate=MODEL_CONFIG["learning_rate"])

    model.compile(
        optimizer=optimizer,
        loss=MODEL_CONFIG["loss"],
        metrics=MODEL_CONFIG["metrics"]
    )

    return model

def train_model(
    training_data: List[TrainingRow],
    input_keys: List[str],
    output_keys: List[str]
) -> Dict:
    """
    Train ML model using simulation-generated data.
    """

    X = []
    y = []

    for row in training_data:
        X.append([float(row.inputs[k]) for k in input_keys])
        y.append([float(row.outputs[k]) for k in output_keys])

    X = np.array(X, dtype=np.float32)
    y = np.array(y, dtype=np.float32)

    model = build_model(X.shape[1], y.shape[1])

    tensorboard = TensorBoard(
        log_dir=MODEL_CONFIG["tensorboard_logdir"],
        histogram_freq=0
    )

    history = model.fit(
        X,
        y,
        epochs=MODEL_CONFIG["epochs"],
        batch_size=MODEL_CONFIG["batch_size"],
        validation_split=MODEL_CONFIG["validation_split"],
        callbacks=[tensorboard],
        verbose=0
    )

    model.save(
        Path(MODEL_CONFIG["tensorboard_logdir"]) / "model.keras"
    )

    return history.history

def load_model(model_path: str) -> tf.keras.Model:
    """
    Load trained Keras model.
    """
    return tf.keras.models.load_model(model_path)

def predict(
    model: tf.keras.Model,
    input_data: Dict[str, float],
    input_keys: List[str],
    output_keys: List[str]
) -> ModelPrediction:
    """
    Predict compact physical parameters.
    """

    X = np.array([[input_data[k] for k in input_keys]], dtype=np.float32)
    y_pred = model.predict(X, verbose=0)[0]

    return ModelPrediction(
        predicted_params=dict(zip(output_keys, map(float, y_pred)))
    )

def params_to_timeline(
    predicted_params: Dict[str, float],
    total_time: float,
    sampling_interval: float
) -> Dict[str, List[float]]:
    """
    Reconstruct separation timeline from predicted parameters.
    """

    A = predicted_params.get("purity_level", 0.0) / 100.0
    k = predicted_params.get("separated_mass", 0.05)

    times = []
    efficiencies = []

    t = 0.0
    while t <= total_time:
        efficiency = A * (1 - np.exp(-k * t))
        times.append(t)
        efficiencies.append(float(efficiency))
        t += sampling_interval

    return {
        "t": times,
        "separation_efficiency": efficiencies
    }
