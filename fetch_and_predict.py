import os
import requests
import joblib
import pandas as pd

# API endpoints
CREATE_API_URL = "https://database-design-group-3.onrender.com/performance/"
FETCH_API_URL = "https://database-design-group-3.onrender.com/performance/{student_id}"

# Create performance record
student_id = "S001"  
performance_data = {
    "Student_ID": student_id,
    "Study_Hours_per_Week": 15,
    "Attendance_Rate": 85,
    "Past_Exam_Scores": 78,
    "Final_Exam_Score": 0  # Placeholder for prediction
}

# POST request to create performance data
response = requests.post(CREATE_API_URL, json=performance_data)
if response.status_code != 200:
    raise Exception(f"Failed to create performance data: {response.status_code}, {response.text}")

print("Created Performance Data:", response.json())

# Fetch the created performance record
response = requests.get(FETCH_API_URL.format(student_id=student_id))
if response.status_code != 200:
    raise Exception(f"Failed to fetch data: {response.status_code}, {response.text}")

# Parse the response JSON
performance_data = response.json()
print("Fetched Performance Data:", performance_data)

# Convert the performance data to a DataFrame
df = pd.DataFrame([performance_data])

# Load the trained model
model_path = os.path.join('models', 'model.pkl')  # Ensure the model.pkl file exists in the 'models' directory
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Trained model not found at {model_path}")

model = joblib.load(model_path)

# Prepare the input data for prediction
# Drop columns that are not used by the model (e.g., 'Final_Exam_Score', 'Pass_Fail', etc.)
X = df.drop(['Final_Exam_Score', 'Pass_Fail'], axis=1, errors='ignore')

# Make predictions
predictions = model.predict(X)

# utput the predictions
print("Predicted Final Exam Score:", predictions[0])