# Car Price Prediction

This project is a FastAPI application for predicting car prices at vucar.

## Report

The latest report can be found here: [link](https://docs.google.com/document/d/19Z7UBl4Te8HHzwaOXbRzGcpIlKpdOoEZ-TlovbhqSX4/edit?usp=sharing)

- Fast recap:
    - Model: LGBM (best baseline)
    - MAE: 40mil vnd
    - R-squared: approx 93%
    - Test case: pass 3/3 w fault tolerance = 5% (pass if predicted value is within 10% interval of the actual value).
    - Monotonic constraint to avoid weird situation.
    - Many room to improve later on (cross val with hyper tune (bayesian approach)).

## Requirements

All the requirements are in the requirements.txt.

Also, my python version is 3.9. I use with conda. 


## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/ngnquanq/car-price-prediction.git
    cd car-price-prediction
    ```

2. Create and activate a virtual environment:
I use conda, so that i will just:
    ```bash
    conda create -n car-price-prediction python=3.9
    conda activate car-price-prediction
    ```
If you dont have conda, use venv (built-in w/ Python)
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:

    ```bash
    python -m pip install -r requirements.txt
    ```
4. (Skip the above if already did it) (Crucial to run application) Weight for lgbm (101MB -> rejected by gh (file too large)).

You can download the weight in the [link](https://drive.google.com/file/d/1W2J11QF6wms18m_6UUy7egOVx2XdBUPL/view?usp=sharing). Then, unzip and put it under the models/

## Running the Application

1. Start the FastAPI server:

    ```bash
    uvicorn api.main:app --reload
    ```

2. Open your browser and navigate to `http://127.0.0.1:8000/docs` to access the interactive API documentation.

## Project Structure

- `api`
    - `main.py`: The main entry point of the FastAPI application.
    - `constants.py`: Use in the main, mainly dealwith preprocessing.
    - `preprocess.py`: Preprocessing function. 
    - `pydantic_models.py`: check for data schema
- `models/`: Directory containing the machine learning models (weights, etc).
- `data/`: Directory containing the dataset.
  - `raw/`: Directory containing the raw dataset.
  - `processed/`: Directory containing the processed dataset.
- `requirements.txt`: File listing all the dependencies.
- `test/`: Directory containing test cases for the application.
  - `test_model/`: Directory containing tests for the model.
- `config/models/xgboost_search_space.json`: File containing the search space configuration for XGBoost model tuning.
- `demo.ipynb`: EDA, preprocessing, training, experiment, etc

## Endpoints

- `GET /`: Root endpoint to check if the API is running.
- `POST /predict`: Endpoint to predict car prices. Expects a JSON payload with car features.

## Test
In order to run test code:

```bash
pytest test
```

The objective of the test is to see whether the predicted values lay within the 5% range of the actual value




