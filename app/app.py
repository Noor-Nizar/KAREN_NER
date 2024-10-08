from fastapi import FastAPI
from fastapi.responses import JSONResponse
from typing import List, Optional, Dict
from pydantic import BaseModel, Field

app = FastAPI()

# --- Load the model and tokenizer ---
from app.models import get_model, get_tokenizer, get_tuning_tokenizer, get_tuning_model
from app.inference import infer

model_main = get_model()
tokenizer_main = get_tokenizer()

model_tuned = get_tuning_model(path = "models/checkpoint-253-aug")
tokenizer_tuned = get_tuning_tokenizer()

# --- Pydantic Schemas for Request/Response Validation ---
class PredictionRequest(BaseModel):
    """Request body for the /predict endpoint."""
    texts: List[str] = Field(..., description="List of Strings")

class PredictionResponse(BaseModel):
    """Response body for the /predict endpoint."""
    predictions: List[List[Dict]] = Field(..., description="List containing a Lists of predictions for each text, one prediction is a dictionary containing the entity, start_idx, end_idx, and label")


# --- API Endpoints ---
@app.post("/predict", response_model=PredictionResponse)
def predict_endpoint(request: PredictionRequest):
    """Predict the entities in the given text."""
    output = infer(request.texts, model_main, tokenizer_main, model_tuned, tokenizer_tuned)
    return JSONResponse(content=output)

### Training EndPoint ? Decided Against it since I feel thatthe annotation process
### in this task specifically is too tedious to realistically expect a client to add data continously 

# --- Health Check ---
@app.get("/health")
def health_check():
    return {"status": "ok"}
