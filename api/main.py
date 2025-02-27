# For logging purposes
import os
from loguru import logger
os.makedirs("/var/log/myapp", exist_ok=True)

# Configure Loguru to log to /var/log/myapp/app.log
logger.add("/var/log/myapp/app.log", rotation="10 MB", retention="10 days", level="INFO")

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
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api import constants, preprocess

# Log initial message 
logger.info("Starting the ML application ...")

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
    logger.info("Serving index page")
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict_lgbm")
def predict_lgbm(car_data: CarPriceData):
    logger.info("Received LGBM prediction request")
    try:
        test_df = pd.DataFrame([car_data.dict()])
    except Exception as e:
        logger.error("DataFrame conversion error: {}", e)
        raise HTTPException(status_code=400, detail=f"Error converting input to DataFrame: {str(e)}")
    
    try:
        test_df = preprocess.drop_unncessary_columns(df=test_df, cols_to_drop=constants.COLS_TO_DROP)
        test_df = preprocess.cast_to_category(df=test_df, cols_to_cast=constants.CAT_COLS)
    except Exception as e:
        logger.error("Preprocessing error: {}", e)
        raise HTTPException(status_code=400, detail=f"Error during preprocessing: {str(e)}")

    try:
        y_pred = model_lgbm.predict(test_df)
    except Exception as e:
        logger.error("Prediction error: {}", e)
        raise HTTPException(status_code=500, detail=f"Error during prediction: {str(e)}")
    
    logger.info("Prediction completed successfully")
    return float(y_pred[0])


if __name__ == "__main__":
    pass