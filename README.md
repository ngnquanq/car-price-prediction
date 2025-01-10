# Car Price Prediction

This project is a FastAPI application for predicting car prices at vucar.

## Requirements

All the requirements are in the requirements.txt.

Also, my python version is 3.9. I use with conda. 


## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/car-price-prediction.git
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




