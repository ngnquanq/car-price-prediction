from json import encoder
from urllib import response
from fastapi.testclient import TestClient
import pandas as pd 
import lightgbm as lgb
from fastapi import FastAPI, HTTPException, Request  # Add Request here
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from regex import R
from api.pydantic_models import CarPriceData
import numpy as np
from loguru import logger
import sys 
import os 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api import constants, preprocess

# Setup some constants
MODEL_PATH="models"

# Initialize the FastAPI app
app = FastAPI()

# Initialize templates
templates = Jinja2Templates(directory="api/templates")

# Mount static files
app.mount("/static", StaticFiles(directory="api/static"), name="static")

# Model LGBM
model_lgbm = lgb.Booster(model_file=f"{MODEL_PATH}/lgbm_model.joblib")

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict_lgbm")
def predict_lgbm(car_data: CarPriceData):
    # Convert input to dataframe
    try:
        test_df = pd.DataFrame([car_data.dict()])
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error converting input to DataFrame: {str(e)}")

    # Preprocess the data
    try:
        # Dropping unwanted columns
        test_df = preprocess.drop_unncessary_columns(df=test_df, cols_to_drop=constants.COLS_TO_DROP)
        
        # Convert categorical columns to category
        test_df = preprocess.cast_to_category(df=test_df, cols_to_cast=constants.CAT_COLS)
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error during preprocessing: {str(e)}")

    # Make prediction
    try:
        y_pred = model_lgbm.predict(test_df)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during prediction: {str(e)}")
    
    return float(y_pred[0])


if __name__ == "__main__":
    pass