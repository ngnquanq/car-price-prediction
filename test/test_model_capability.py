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
#from api.main import predict_lgbm 
#from api.main import app
from api import constants, preprocess


#client = TestClient(app)

from fastapi.middleware.cors import CORSMiddleware


@pytest.mark.parametrize("sample_data,actual_value", [
    ("sample_inference_1", 451500000.0),
    ("sample_inference_2", 729666666.0), 
    ("sample_inference_3", 222500000.0)
])
def test_model_inference_lgbm(create_model_lgbm, request, sample_data, actual_value):
    """Test LGBM model inference using parametrized fixtures."""
    model = create_model_lgbm
    # request is a built-in pytest fixture that provides access to test context
    # It allows retrieving other fixtures dynamically using getfixturevalue()
    sample = request.getfixturevalue(sample_data)
    
    # Tolerance for 5% interval
    tolerance = 0.05

    # Preprocess the sample data
    data_df = pd.DataFrame([sample])
    data_df = preprocess.drop_unncessary_columns(data_df, constants.COLS_TO_DROP)
    data_df = preprocess.cast_to_category(data_df, constants.CAT_COLS)

    # Make prediction
    prediction = model.predict(data_df)
    predicted_value = float(prediction[0])

    # Calculate bounds
    lower_bound = actual_value * (1 - tolerance)
    upper_bound = actual_value * (1 + tolerance)

    # Assertion: Check if the predicted value is within the interval
    assert lower_bound <= predicted_value <= upper_bound, (
        f"Predicted value {predicted_value} is not within {tolerance*100}% of the actual value {actual_value}."
    )

    print(f"Test passed: Predicted value {predicted_value} is within {tolerance*100}% of the actual value {actual_value}.")