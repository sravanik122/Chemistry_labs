import json
import os
import numpy as np
import tensorflow as tf
from typing import List, Dict

from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import TensorBoard, EarlyStopping, ModelCheckpoint

from .types import TrainingRow, Timeline
from .helpers import clamp

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "../config/model_config.json")

with open(CONFIG_PATH, "r") as f:
    MODEL_CONFIG = json.load(f)

EPOCHS = MODEL_CONFIG["epochs"]
BATCH_SIZE = MODEL_CONFIG["batch_size"]
LEARNING_RATE = MODEL_CONFIG["learning_rate"]
VAL_SPLIT = MODEL_CONFIG["validation_split"]

LAYERS = MODEL_CONFIG["model_layers"]
DROPOUT = MODEL_CONFIG["dropout_rate"]

LOSS = MODEL_CONFIG["loss"]
METRICS = MODEL_CONFIG["metrics"]

LOG_DIR = MODEL_CONFIG["tensorboard_logdir"]
MODEL_PATH = MODEL_CONFIG["model_checkpoint_path"]

EARLY_STOP = MODEL_CONFIG["early_stopping"]

def build_model(input_dim: int, output_dim: int) -> tf.keras.Model:
    """
    Build regression MLP model.
    """

    model = Sequential()

    # Input layer
    model.add(Dense(LAYERS[0], activation="relu", input_shape=(input_dim,)))

    # Hidden layers
    for units in LAYERS[1:]:
        model.add(Dense(units, activation="relu"))
        model.add(Dropout(DROPOUT))

    # Output layer
    model.add(Dense(output_dim, activation="linear"))

    optimizer = Adam(learning_rate=LEARNING_RATE)

    model.compile(
        optimizer=optimizer,
        loss=LOSS,
        metrics=METRICS
    )

    return model

def train_model(
    training_data: List[TrainingRow],
    input_keys: List[str],
    output_keys: List[str]
) -> Dict:
    """
    Train ML model.
    """
    # Prepare dataset
    X = []
    y = []

    for row in training_data:

        X.append([float(row.inputs[k]) for k in input_keys])
        y.append([float(row.outputs[k]) for k in output_keys])

    X = np.array(X, dtype=np.float32)
    y = np.array(y, dtype=np.float32)

    # Build model
    model = build_model(X.shape[1], y.shape[1])

    # Callbacks
    callbacks = []

    callbacks.append(
        TensorBoard(log_dir=LOG_DIR)
    )

    callbacks.append(
        EarlyStopping(
            monitor=EARLY_STOP["monitor"],
            patience=EARLY_STOP["patience"],
            restore_best_weights=EARLY_STOP["restore_best_weights"]
        )
    )

    callbacks.append(
        ModelCheckpoint(
            MODEL_PATH,
            monitor="val_loss",
            save_best_only=True
        )
    )

    # Train
    history = model.fit(
        X,
        y,
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        validation_split=VAL_SPLIT,
        callbacks=callbacks,
        verbose=1
    )

    # Save model
    model.save(MODEL_PATH)

    return history.history

def load_trained_model() -> tf.keras.Model:
    """
    Load saved model.
    """

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("Trained model not found")

    return load_model(MODEL_PATH)

def predict(
    model: tf.keras.Model,
    inputs: Dict[str, float],
    input_keys: List[str]
) -> Dict[str, float]:
    """
    Predict output parameters.
    """

    X = np.array(
        [[float(inputs[k]) for k in input_keys]],
        dtype=np.float32
    )

    preds = model.predict(X)[0]

    return {
        f"param_{i}": float(p)
        for i, p in enumerate(preds)
    }

def params_to_timeline(
    predicted_params: Dict[str, float],
    total_time: float,
    sampling_interval: float
) -> Timeline:
    """
    Convert predicted parameters to timeline.
    """

    A = predicted_params.get("param_0", 7.0)
    k = predicted_params.get("param_1", 0.05)

    steps = int(total_time / sampling_interval) + 1

    t_vals = []
    ph_vals = []
    color_vals = []
    progress_vals = []

    for i in range(steps):

        t = i * sampling_interval

        ph = A * (1 - np.exp(-k * t))
        ph = clamp(ph, 0.0, 14.0)

        progress = min(1.0, t / total_time)

        t_vals.append(t)
        ph_vals.append(ph)
        color_vals.append(ph / 14.0)
        progress_vals.append(progress)

    return Timeline(
        t=t_vals,
        pH=ph_vals,
        color_intensity=color_vals,
        reaction_progress=progress_vals
    )
