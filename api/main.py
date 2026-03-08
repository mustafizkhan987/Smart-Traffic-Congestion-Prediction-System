from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Smart Traffic Congestion Prediction API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model
model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ml', 'traffic_model.joblib')

try:
    model = joblib.load(model_path)
except FileNotFoundError:
    model = None
    print(f"Warning: Model not found at {model_path}. Please run train_model.py first.")

class TrafficFeatures(BaseModel):
    Time: str
    Day: str
    Road_ID: str
    Weather: str

@app.post("/predict")
def predict_congestion(features: TrafficFeatures):
    if model is None:
        raise HTTPException(status_code=500, detail="Model is not loaded.")
        
    try:
        # Extract Hour and Minute
        time_parts = features.Time.split(':')
        if len(time_parts) != 2:
            raise ValueError("Time must be in HH:MM format.")
            
        hour = int(time_parts[0])
        minute = int(time_parts[1])
        
        # Create DataFrame
        df = pd.DataFrame([{
            'Hour': hour,
            'Minute': minute,
            'Day': features.Day,
            'Road_ID': features.Road_ID,
            'Weather': features.Weather
        }])
        
        # Predict
        prediction = model.predict(df)[0]
        
        return {
            "prediction": prediction,
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "healthy", "model_loaded": model is not None}
