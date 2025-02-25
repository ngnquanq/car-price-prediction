import pandas as pd
import numpy as np
import os
import joblib
from api.constants import CAT_COLS
from api.preprocess import cast_to_category, encode_cat_cols
from lightgbm import LGBMRegressor
import lightgbm as lgb


DATA_PATH = 'data'
MODEL_PATH = 'models'

if not os.path.exists(MODEL_PATH):
    os.makedirs(MODEL_PATH)

monotonic_constraints = [1, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0]

lgbm_params = {
    'objective': 'regression',
    'metric': 'mae',
    'boosting_type': 'gbdt',
    'monotone_constraints':monotonic_constraints,
    'monotone_constraints_method':'advanced',
    'num_leaves': 31,
    'learning_rate': 0.1,
    'feature_fraction': 0.9
}


X_train = pd.read_csv(f"{DATA_PATH}/processed/X_train_monotonic.csv")
y_train = pd.read_csv(f"{DATA_PATH}/processed/y_train_monotonic.csv")
X_test = pd.read_csv(f"{DATA_PATH}/processed/X_test_monotonic.csv") 
y_test = pd.read_csv(f"{DATA_PATH}/processed/y_test_monotonic.csv")
X_val = pd.read_csv(f"{DATA_PATH}/processed/X_val_monotonic.csv")
y_val = pd.read_csv(f"{DATA_PATH}/processed/y_val_monotonic.csv")

# Create encoded versions for LightGBM
X_train_encoded = X_train.copy()
X_test_encoded = X_test.copy()
y_train_encoded = y_train.copy()
y_test_encoded = y_test.copy()
X_val_encoded = X_val.copy()
y_val_encoded = y_val.copy()

X_train_encoded = cast_to_category(X_train_encoded, CAT_COLS)
X_test_encoded = cast_to_category(X_test_encoded, CAT_COLS)
X_val_encoded = cast_to_category(X_val_encoded, CAT_COLS)

# Create LightGBM dataset
train_data = lgb.Dataset(X_train_encoded, 
                         label=y_train_encoded,
                         categorical_feature='auto')
val_data = lgb.Dataset(X_val_encoded, 
                        label=y_val_encoded, 
                        reference=train_data,
                        categorical_feature='auto')
test_data = lgb.Dataset(X_test_encoded,
                        label=y_test_encoded,
                        categorical_feature='auto',
                        reference=train_data)

lgbm_model = lgb.train(lgbm_params, train_data, num_boost_round=40000, valid_sets=[train_data, test_data])
lgbm_model.save_model(f'{MODEL_PATH}/lgbm_model.joblib') #the file is heavy tho

    