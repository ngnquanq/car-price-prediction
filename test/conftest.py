import pandas as pd
import xgboost as xgb
import pytest
import random
import pandas as pd
import pytest
import random
import joblib
import catboost
from api.constants import CAT_COLS, COLS_TO_DROP
from api.preprocess import convert_data_dmatrix, drop_unncessary_columns, cast_to_category, encode_cat_cols
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api.main import PARAMS, MODEL_PATH

@pytest.fixture()
def create_model():
    model = catboost.CatBoostRegressor()
    model.load_model(f"{MODEL_PATH}/catboost_model.cbm")
    return model

@pytest.fixture()
def create_encoder():
    encoder = joblib.load(f"{MODEL_PATH}/label_encoders.joblib")
    return encoder

@pytest.fixture()
def sample_inference_1():
    return {
    "id": 149990878,
    "list_id": 109913621,
    "list_time": 1694606265000,
    "manufacture_date": 2020,
    "brand": "Mercedes Benz",
    "model": "GLC Class",
    "origin": "Việt Nam",
    "type": "SUV / Cross over",
    "seats": 5.0,
    "gearbox": "AT",
    "fuel": "petrol",
    "color": "black",
    "mileage_v2": 71000,
    "condition": "used"
    }
@pytest.fixture()
def sample_inference_2():
    return {
        "id": 149990878,
        "list_id": 109913621,
        "list_time": 1694606265000,
        "manufacture_date": 2017,
        "brand": "Honda",
        "model": "Civic",
        "origin": "Thái Lan",
        "type": "Sedan",
        "seats": 5.0,
        "gearbox": "AT",
        "fuel": "petrol",
        "color": "black",
        "mileage_v2": 68500,
        "condition": "used"
    }

# The actual value for this is 368000000
@pytest.fixture()
def sample_inference_3():
        return {
        "id": 149990878,
        "list_id": 109913621,
        "list_time": 1694606265000,
        "manufacture_date": 2020,
        "brand": "Toyota",
        "model": "Vios",
        "origin": "Việt Nam",
        "type": "Sedan",
        "seats": 5.0,
        "gearbox": "MT",
        "fuel": "petrol",
        "color": "white",
        "mileage_v2": 99999,
        "condition": "used"
        }
