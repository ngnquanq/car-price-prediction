from os import error
import pandas as pd
import numpy as np
from xgboost import DMatrix
from typing import List, Optional
def drop_unncessary_columns(df: pd.DataFrame, cols_to_drop: List[str]):
    """Dropping unnecessary columns from the dataframe

    Args:
        df (pd.DataFrame): the dataframe
        cols_to_drop (List[str]): columns to drop
    """
    df = df.drop(columns=cols_to_drop, errors='ignore')
    return df

def cast_to_string(df: pd.DataFrame, cols_to_cast: List[str]):
    """Casting columns to string

    Args:
        df (pd.DataFrame): the dataframe
        cols_to_cast (List[str]): columns to cast
    """
    for col in cols_to_cast:
        df[col] = df[col].astype(str)
    return df

def cast_to_category(df: pd.DataFrame, cols_to_cast: List[str]):
    """Casting columns to string

    Args:
        df (pd.DataFrame): the dataframe
        cols_to_cast (List[str]): columns to cast
    """
    for col in cols_to_cast:
        df[col] = df[col].astype('category')
    return df


def encode_cat_cols(df: pd.DataFrame, label_encoder, cat_cols: List[str]):
    """Encoding categorical columns

    Args:
        df (pd.DataFrame): the dataframe
        label_encoder: the label encoder
        cat_cols (List[str]): categorical columns
    """
    for col in cat_cols:
        df[col] = label_encoder[col].transform(list(df[col].values))
    return df

def convert_data_dmatrix(df: pd.DataFrame):
    """Convert dataframe to DMatrix

    Args:
        df (pd.DataFrame): the dataframe
    """
    return DMatrix(df, enable_categorical=True, missing=np.NAN)
