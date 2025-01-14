from json import encoder
from urllib import response
import catboost
from fastapi.testclient import TestClient
import joblib
import pytest
import pandas as pd 
import xgboost as xgb
from fastapi import FastAPI, HTTPException, Request  # Add Request here
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from regex import R
import requests
from api.pydantic_models import CarPriceData
import numpy as np
from loguru import logger
import sys 
import os 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api import constants, preprocess

# Setup some constants
MODEL_PATH="models"
PARAMS = {
    'objective': 'reg:squarederror', 
    'max_depth': 20,
    'eta': 0.5,
    'enable_categorical': True
    }

# Initialize the FastAPI app
app = FastAPI()

# Initialize templates
templates = Jinja2Templates(directory="api/templates")

# Mount static files
app.mount("/static", StaticFiles(directory="api/static"), name="static")


# Load the encoder
encoder = joblib.load(f"{MODEL_PATH}/label_encoders.joblib")
# load the model
model = catboost.CatBoostRegressor()
model.load_model(f"{MODEL_PATH}/catboost_model.cbm")

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


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
        
        # # Convert categorical columns to category
        test_df = preprocess.cast_to_category(df=test_df, cols_to_cast=constants.CAT_COLS)
        
        # # Convert with the label encoder
        test_df = preprocess.encode_cat_cols(df=test_df, label_encoder=encoder, cat_cols=constants.CAT_COLS)
        
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error during preprocessing: {str(e)}")

    # Make prediction
    try:
        y_pred = model.predict(test_df)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during prediction: {str(e)}")
    
    return float(y_pred[0])

if __name__ == "__main__":
    # The following code is for fast prototype
    xgb_params = {
    'objective': 'reg:squarederror', 
    'max_depth': 20,
    'eta': 0.5,
    'enable_categorical': True
    }   
    #model = xgb.Booster(params=xgb_params, model_file=f"{MODEL_PATH}/xgb_model.json")
    encoder = joblib.load(f"{MODEL_PATH}/label_encoders.joblib")
    model = catboost.CatBoostRegressor()
    model.load_model(f"{MODEL_PATH}/catboost_model.cbm")
    sample_data = constants.SAMPLE_DATA
    data_df = pd.DataFrame(sample_data, index=[0])
    data_df = data_df.drop(columns='price')
    data_df = preprocess.drop_unncessary_columns(df=data_df, cols_to_drop=constants.COLS_TO_DROP)
    data_df = preprocess.cast_to_category(df=data_df, cols_to_cast=constants.CAT_COLS)
    data_df = preprocess.encode_cat_cols(df=data_df, label_encoder=encoder, cat_cols=constants.CAT_COLS)
    #data_numpy = data_df.to_numpy()
    # # Convert the sample input to DMatrix for prediction
    #dtest_sample = xgb.DMatrix(data_df, enable_categorical=True, missing=np.NAN)

    # Predict the price using the trained model
    predicted_price = model.predict(data_df)

    # Print the predicted price
    print(f"Predicted price: {predicted_price[0]}")