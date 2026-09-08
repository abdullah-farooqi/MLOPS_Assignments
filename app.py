from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="student-ml-api",
    description="Simple ML inference API",
    version="1.0.0"
)


class PredictionInput(BaseModel):
    value: float


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "application": "student-ml-api",
        "version": "1.0.0"
    }


@app.post("/predict")
def predict(data: PredictionInput):
    prediction = data.value * 2

    return {
        "input": data.value,
        "prediction": prediction
    }
