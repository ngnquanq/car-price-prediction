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
catogrical_encoder=joblib.load(f"{MODEL_PATH}/label_encoders.joblib") # still thinking
model=joblib.load(filename='models/model_xgb.joblib') # still thinking

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
    # Convert input to dataframe
    try:
        test_df = pd.DataFrame([car_data.dict()])
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error converting input to DataFrame: {str(e)}")

    # Preprocess the data
    try:
        # Dropping unwanted columns
        test_df = preprocess.drop_unncessary_columns(df=test_df, cols_to_drop=constants.COLS_TO_DROP)
        print("pass drop")
        
        # Convert categorical columns to category
        test_df = preprocess.cast_to_category(df=test_df, cols_to_cast=constants.CAT_COLS)
        
        # Convert df to DMatrix (assuming this is for XGBoost)
        test_df = preprocess.convert_data_dmatrix(df=test_df)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error during preprocessing: {str(e)}")

    # Make prediction
    try:
        y_pred = model.predict(test_df)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during prediction: {str(e)}")
    
    return {"prediction": float(y_pred[0])}