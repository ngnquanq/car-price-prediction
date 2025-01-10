from calendar import c
from json import encoder
import os
import pandas as pd
import sys
import numpy as np
from unittest.mock import MagicMock, patch
#from conftest import create_model, sample_inference_1, sample_inference_2, sample_inference_3
from test.conftest import sample_inference_1, sample_inference_2, sample_inference_3

from fastapi.testclient import TestClient
import pytest

# Add the root directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api.main import predict 
from api.main import app
from api import constants, preprocess
import xgboost as xgb


client = TestClient(app)

from fastapi.middleware.cors import CORSMiddleware

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Adjust allowed origins for your use case
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


def test_model_inference_1(create_model, create_encoder, sample_inference_1):
    """Test model inference using a fixture."""
    model = create_model  # Load the model from the fixture
    encoder = create_encoder
    # Actual value for sample_inference_1
    actual_value = 1239000000.0

    # Tolerance for 5% interval
    tolerance = 0.05

    # Preprocess the sample data
    data_df = pd.DataFrame([sample_inference_1])
    data_df = preprocess.drop_unncessary_columns(data_df, constants.COLS_TO_DROP)
    data_df = preprocess.cast_to_category(data_df, constants.CAT_COLS)
    data_df = preprocess.encode_cat_cols(data_df, encoder, constants.CAT_COLS)
    # Convert to DMatrix
   #dtest = preprocess.convert_data_dmatrix(df=data_df)

    # Make prediction
    prediction = model.predict(data_df)
    predicted_value = float(prediction[0])

    # Calculate bounds
    lower_bound = actual_value * (1 - tolerance)
    upper_bound = actual_value * (1 + tolerance)

    # Assertion: Check if the predicted value is within the interval
    assert lower_bound <= predicted_value <= upper_bound, (
        f"Predicted value {predicted_value} is not within 5% of the actual value {actual_value}."
    )

    print(f"Test passed: Predicted value {predicted_value} is within 5% of the actual value {actual_value}.")


def test_model_inference_2(create_model, create_encoder, sample_inference_2):
    """Test model inference using a fixture."""
    model = create_model  # Load the model from the fixture
    encoder = create_encoder
    # Actual value for sample_inference_1
    actual_value = 494000000.0

    # Tolerance for 5% interval
    tolerance = 0.05

    # Preprocess the sample data
    data_df = pd.DataFrame([sample_inference_2])
    data_df = preprocess.drop_unncessary_columns(data_df, constants.COLS_TO_DROP)
    data_df = preprocess.cast_to_category(data_df, constants.CAT_COLS)
    data_df = preprocess.encode_cat_cols(data_df, encoder, constants.CAT_COLS)
    # Convert to DMatrix
    #dtest = preprocess.convert_data_dmatrix(df=data_df)

    # Make prediction
    prediction = model.predict(data_df)
    predicted_value = float(prediction[0])

    # Calculate bounds
    lower_bound = actual_value * (1 - tolerance)
    upper_bound = actual_value * (1 + tolerance)

    # Assertion: Check if the predicted value is within the interval
    assert lower_bound <= predicted_value <= upper_bound, (
        f"Predicted value {predicted_value} is not within 5% of the actual value {actual_value}."
    )

    print(f"Test passed: Predicted value {predicted_value} is within 5% of the actual value {actual_value}.")

def test_model_inference_3(create_model, create_encoder, sample_inference_3):
    """Test model inference using a fixture."""
    model = create_model  # Load the model from the fixture
    encoder = create_encoder
    # Actual value for sample_inference_1
    actual_value = 368000000.0

    # Tolerance for 5% interval
    tolerance = 0.05

    # Preprocess the sample data
    data_df = pd.DataFrame([sample_inference_3])
    data_df = preprocess.drop_unncessary_columns(data_df, constants.COLS_TO_DROP)
    data_df = preprocess.cast_to_category(data_df, constants.CAT_COLS)
    data_df = preprocess.encode_cat_cols(data_df, encoder, constants.CAT_COLS)

    # Make prediction
    prediction = model.predict(data_df)
    predicted_value = float(prediction[0])

    # Calculate bounds
    lower_bound = actual_value * (1 - tolerance)
    upper_bound = actual_value * (1 + tolerance)

    # Assertion: Check if the predicted value is within the interval
    assert lower_bound <= predicted_value <= upper_bound, (
        f"Predicted value {predicted_value} is not within 5% of the actual value {actual_value}."
    )

    print(f"Test passed: Predicted value {predicted_value} is within 5% of the actual value {actual_value}.")

# @pytest.mark.parametrize("sample_inference, actual_value", [
#     ("sample_inference_1", 1239000000.0),  # Reference fixture by name
#     ("sample_inference_2", 368000000.0),
#     ("sample_inference_3", 368000000.0)
# ], indirect=["sample_inference"])  # Use indirect parameterization for the fixture
# def test_correct_inference(sample_inference, actual_value):
#     predicted_value = client.post("/predict", json=sample_inference).json()  # Ensure it returns the predicted value
#     tolerance = 0.1  # 10% tolerance
#     lower_bound = actual_value * (1 - tolerance)
#     upper_bound = actual_value * (1 + tolerance)
#     assert lower_bound <= predicted_value <= upper_bound, f"Predicted value {predicted_value} is not within {tolerance*100}% of actual value {actual_value}"


# def test_inference_case_1(sample_inference_1, create_model):
#     actual_value = 1239000000.0
#     tolerance = 0.1  # 10% tolerance
#     model = create_model
#     # Simulate API request (replace client.post with actual logic)
#     predicted_value = client.post("/predict", json=sample_inference_1).json()

#     # Calculate bounds
#     lower_bound = actual_value * (1 - tolerance)
#     upper_bound = actual_value * (1 + tolerance)

#     # Assertion
#     assert lower_bound <= predicted_value <= upper_bound, f"Predicted value {predicted_value} is not within 10% of actual value {actual_value}"


# def test_inference_case_2(sample_inference_2):
#     actual_value = 368000000.0
#     tolerance = 0.1  # 10% tolerance

#     # Simulate API request (replace client.post with actual logic)
#     predicted_value = client.post("/predict", json=sample_inference_2).json()

#     # Calculate bounds
#     lower_bound = actual_value * (1 - tolerance)
#     upper_bound = actual_value * (1 + tolerance)

#     # Assertion
#     assert lower_bound <= predicted_value <= upper_bound, f"Predicted value {predicted_value} is not within 10% of actual value {actual_value}"


# def test_inference_case_3(sample_inference_3):
#     actual_value = 368000000.0
#     tolerance = 0.1  # 10% tolerance
#     print(sample_inference_3)
#     # Simulate API request and get the predicted value as a float
#     response = client.post("/predict", json=sample_inference_3)
#     assert response.status_code == 200, f"API request failed with status code {response.status_code} and detail {response.json()}"
#     predicted_value = float(response.json())  # Ensure the predicted value is converted to float

#     # Calculate bounds
#     lower_bound = actual_value * (1 - tolerance)
#     upper_bound = actual_value * (1 + tolerance)

#     # Assertion
#     assert lower_bound <= predicted_value <= upper_bound, (
#         f"Predicted value {predicted_value} is not within 10% of actual value {actual_value}"
#     )
