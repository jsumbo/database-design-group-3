import requests
import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

def fetch_latest_data(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")

def load_model(model_path):
    return joblib.load(model_path)

def prepare_data(data):
    # Assuming the data is in a format that can be directly used by the model
    # Convert data to DataFrame if necessary
    df = pd.DataFrame([data])
    return df

def make_prediction(model, data):
    prediction = model.predict(data)
    return prediction[0]

if __name__ == "__main__":
    api_url = "http://localhost:8000/performance/latest"  # Replace with the actual endpoint for the latest entry
    model_path = "path_to_your_model.pkl"  # Replace with the path to your trained model

    try:
        latest_data = fetch_latest_data(api_url)
        model = load_model(model_path)
        prepared_data = prepare_data(latest_data)
        prediction = make_prediction(model, prepared_data)
        print(f"Predicted Final Exam Score: {prediction}")
    except Exception as e:
        print(e)