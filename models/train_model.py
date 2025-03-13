import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
import joblib
import os

# Construct the full path to the CSV file
csv_file_path = 'student_performance_dataset.csv'

# Load dataset
df = pd.read_csv(csv_file_path)

# Preprocess data
X = df.drop(['Final_Exam_Score'], axis=1)
y = df['Final_Exam_Score']

# Identify categorical and numeric columns
categorical_cols = X.select_dtypes(include=['object', 'category']).columns
numeric_cols = X.select_dtypes(include=['int64', 'float64']).columns

# Create preprocessing pipelines for both numeric and categorical data
numeric_transformer = Pipeline(steps=[
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

# Combine preprocessing steps
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_cols),
        ('cat', categorical_transformer, categorical_cols)
    ])

# Create a complete pipeline
clf = Pipeline(steps=[('preprocessor', preprocessor),
                      ('regressor', LinearRegression())])

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
clf.fit(X_train, y_train)

# Create the models directory if it does not exist
models_dir = 'models'
if not os.path.exists(models_dir):
    os.makedirs(models_dir)

# Save the model and the preprocessor
model_path = os.path.join(models_dir, 'model.pkl')
joblib.dump(clf, model_path)