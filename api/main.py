from urllib import response
import joblib
import pandas as pd 
from regex import R
import requests
from api.pydantic_models import CarPriceData
from fastapi import FastAPI, HTTPException
from loguru import logger
import sys 
import os 
sys.path.append(os.path.dirname(os.path.dirname((os.path.abspath(__file__)))))
from api import constants, preprocess

# Setup some constants
MODEL_PATH="models"
EXTERNAL_API="https://localhost:8081/retrieve_data" #can connect to database or other external resources

# Initialize the FastAPI app
app = FastAPI()

# load the model
encoder=... # still thinking
model=... # still thinking

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/retrieve_data")
def retrieve_data(id: int):
    # Make call from external resources to retrieve data
    logger.info(f"Retrieving data for id {id}")
    return constants.SAMPLE_DATA

@app.post("/predict")
def predict(car_data: CarPriceData):
    # convert input to dataframe
    test_df = pd.DataFrame([car_data.dict()])
    # preprocess the data
    
    # Make prediction
    try:
        y_pred = model.predict(test_df)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return{"prediction": y_pred[0]}