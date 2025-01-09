# Car Price Prediction

This project is a FastAPI application for predicting car prices at vucar.

## Requirements

- Python 3.9+
- FastAPI
- Uvicorn
- scikit-learn
- pandas

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/car-price-prediction.git
    cd car-price-prediction
    ```

2. Create and activate a virtual environment:

If you dont have conda, use venv (built-in w/ Python)
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

1. Start the FastAPI server:

    ```bash
    uvicorn main:app --reload
    ```

2. Open your browser and navigate to `http://127.0.0.1:8000/docs` to access the interactive API documentation.

## Project Structure

- `main.py`: The main entry point of the FastAPI application.
- `models/`: Directory containing the machine learning models.
- `data/`: Directory containing the dataset and data processing scripts.
- `requirements.txt`: File listing all the dependencies.

## Endpoints

- `GET /`: Root endpoint to check if the API is running.
- `POST /predict`: Endpoint to predict car prices. Expects a JSON payload with car features.

## Example Request

```json
{
    "make": "Toyota",
    "model": "Corolla",
    "year": 2020,
    "mileage": 15000,
    "condition": "Excellent"
}
```

## License

This project is licensed under the MIT License.

## Contact

For any questions or suggestions, please open an issue or contact the repository owner.
