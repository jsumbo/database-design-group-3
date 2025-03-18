import os
import requests
import joblib
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API endpoint to fetch the latest student entry
# API_URL = "https://database-design-group-3.onrender.com/students"

data = requests.get ("https://database-design-group-3.onrender.com/students" verify=false).json()
# API_URL = "https://database-design-group-3.onrender.com/students/latest"

# Fetch the latest student entry
response = requests.get(API_URL)
if response.status_code != 200:
    raise Exception(f"Failed to fetch data: {response.status_code}, {response.text}")

student_data = response.json()

# Convert the student data to a DataFrame
df = pd.DataFrame([student_data])

# Load the trained model
model_path = os.path.join('models', 'model.pkl')
model = joblib.load(model_path)

# Prepare the input data
X = df.drop(['Final_Exam_Score'], axis=1, errors='ignore')

# Make predictions
predictions = model.predict(X)

# Output the predictions
print("Predictions:", predictions)