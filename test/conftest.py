import pandas as pd
import lightgbm as lgb
import pytest
import random
import pandas as pd
import random
import joblib
from api.constants import CAT_COLS, COLS_TO_DROP
from api.preprocess import convert_data_dmatrix, drop_unncessary_columns, cast_to_category, encode_cat_cols
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api.main import MODEL_PATH

# @pytest.fixture()
# def create_model_xgboost():
#     model = catboost.CatBoostRegressor()
#     model.load_model(f"{MODEL_PATH}/catboost_model.cbm")
#     return model


# @pytest.fixture()
# def create_model_catboost():
#     model = catboost.CatBoostRegressor()
#     model.load_model(f"{MODEL_PATH}/catboost_model_autoencode.cbm")
#     return model

@pytest.fixture()
def create_model_lgbm():
    model = lgb.Booster(model_file=f"{MODEL_PATH}/lgbm_model.joblib")
    return model

# @pytest.fixture()
# def create_encoder():
#     encoder = joblib.load(f"{MODEL_PATH}/label_encoders.joblib")
#     return encoder

@pytest.fixture()
def sample_inference_1():
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
        "gearbox": "AT",
        "fuel": "petrol",
        "color": "white",
        "mileage_v2": 30000,
        "condition": "used"
    }

@pytest.fixture()
def sample_inference_2():
    return {
        "id": 149990878,
        "list_id": 109913621,
        "list_time": 1694606265000,
        "manufacture_date": 2020,
        "brand": "Hyundai",
        "model": "Tucson",
        "origin": "Việt Nam",
        "type": "SUV / Cross over",
        "seats": 5.0,
        "gearbox": "AT",
        "fuel": "petrol",
        "color": "white",
        "mileage_v2": 20000,
        "condition": "used"
    }

@pytest.fixture()
def sample_inference_3():
    return {
        "id": 149990878,
        "list_id": 109913621,
        "list_time": 1694606265000,
        "manufacture_date": 2011,
        "brand": "Chevrolet",
        "model": "Cruze",
        "origin": "Mỹ",
        "type": "Sedan",
        "seats": 5.0,
        "gearbox": "MT",
        "fuel": "petrol",
        "color": "gold",
        "mileage_v2": 95000,
        "condition": "used"
    }