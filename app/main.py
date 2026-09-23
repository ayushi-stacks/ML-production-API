from pathlib import Path

import joblib
import pandas as pd  # type: ignore[reportMissingModuleSource]
from fastapi import FastAPI
from pydantic import BaseModel, Field


# -----------------------------
# Paths
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "model" / "xgboost_pm25_model.pkl"


# -----------------------------
# Load Model
# -----------------------------

model = joblib.load(MODEL_PATH)


# -----------------------------
# FastAPI App
# -----------------------------

app = FastAPI(
    title="Delhi PM2.5 Prediction API",
    description="REST API for predicting next-day PM2.5 concentration.",
    version="1.0.0"
)


# -----------------------------
# Request Schema
# -----------------------------

class PM25Request(BaseModel):
    lag_1: float = Field(ge=0)
    lag_2: float = Field(ge=0)
    lag_3: float = Field(ge=0)
    lag_7: float = Field(ge=0)

    rolling_3: float = Field(ge=0)
    rolling_7: float = Field(ge=0)
    rolling_14: float = Field(ge=0)

    day_of_week: int = Field(ge=0, le=6)
    day_of_year: int = Field(ge=1, le=366)
    week_of_year: int = Field(ge=1, le=53)


# -----------------------------
# Health Check
# -----------------------------

@app.get("/")
def root():
    return {
        "message": "Delhi PM2.5 Prediction API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# -----------------------------
# Prediction Endpoint
# -----------------------------

@app.post("/predict")
def predict(request: PM25Request):

    input_data = pd.DataFrame([{
        "lag_1": request.lag_1,
        "lag_2": request.lag_2,
        "lag_3": request.lag_3,
        "lag_7": request.lag_7,
        "rolling_3": request.rolling_3,
        "rolling_7": request.rolling_7,
        "rolling_14": request.rolling_14,
        "day_of_week": request.day_of_week,
        "day_of_year": request.day_of_year,
        "week_of_year": request.week_of_year
    }])

    prediction = model.predict(input_data)[0]

    prediction = max(0, float(prediction))

    return {
        "predicted_pm25": round(prediction, 2),
        "unit": "µg/m³"
    }