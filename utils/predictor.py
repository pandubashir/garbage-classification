"""
predictor.py
------------
Handles model loading and image inference.

Model is loaded once at module import time so it is shared across
all requests without reloading on every call.
"""

import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# ── Constants ────────────────────────────────────────────────────────────────

CLASS_NAMES = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']
INPUT_SIZE   = (224, 224)
MODEL_PATH   = os.path.join(os.path.dirname(__file__), '..', 'model', 'garbage_cnn.h5')

# ── Model Loading ─────────────────────────────────────────────────────────────
# Loaded once when the module is first imported.
# If the model file is missing, we raise immediately with a clear message
# instead of a cryptic crash on the first request.

try:
    _model = load_model(os.path.normpath(MODEL_PATH))
except Exception as e:
    raise RuntimeError(
        f"Failed to load model from '{MODEL_PATH}'. "
        f"Make sure 'model/garbage_cnn.h5' exists. Original error: {e}"
    )

# ── Public API ────────────────────────────────────────────────────────────────

def predict(img_path: str) -> dict:
    """
    Run inference on a single image file.

    Parameters
    ----------
    img_path : str
        Absolute or relative path to the image file.

    Returns
    -------
    dict with keys:
        top_class   : str   — predicted class name
        confidence  : float — confidence percentage (0–100)
        top3        : list  — [{'class': str, 'confidence': float}, ...]
    """
    img_array = _preprocess(img_path)
    probabilities = _model.predict(img_array, verbose=0)[0]  # shape: (6,)

    # Top-1
    top_index = int(np.argmax(probabilities))
    top_class  = CLASS_NAMES[top_index]
    confidence = float(probabilities[top_index]) * 100

    # Top-3 — sorted by probability descending
    top3_indices = np.argsort(probabilities)[::-1][:3]
    top3 = [
        {
            'class':      CLASS_NAMES[i],
            'confidence': round(float(probabilities[i]) * 100, 2),
        }
        for i in top3_indices
    ]

    return {
        'top_class':  top_class,
        'confidence': round(confidence, 2),
        'top3':       top3,
    }


# ── Internal Helpers ─────────────────────────────────────────────────────────

def _preprocess(img_path: str) -> np.ndarray:
    """
    Load an image from disk and prepare it for ResNet50 inference.

    Mirrors exactly what was used during training:
        ImageDataGenerator(preprocessing_function=
            tf.keras.applications.resnet50.preprocess_input)
    """
    img       = image.load_img(img_path, target_size=INPUT_SIZE)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = tf.keras.applications.resnet50.preprocess_input(img_array)
    return img_array
