import os
import pandas as pd
import mysql.connector
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get database credentials
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# Connect to MySQL database
try:
    db = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = db.cursor()
    print("Connected to MySQL successfully!")
except mysql.connector.Error as err:
    print(f"Database connection error: {err}")
    exit(1)

# Load CSV
df = pd.read_csv("student_performance_dataset.csv")

# Expected columns
expected_columns = {
    "Student_ID", "Gender", "Parental_Education_Level", "Internet_Access_at_Home",
    "Extracurricular_Activities", "Study_Hours_per_Week", "Attendance_Rate",
    "Past_Exam_Scores", "Final_Exam_Score", "Pass_Fail"
}

if not expected_columns.issubset(df.columns):
    raise ValueError(f"Missing columns! Expected: {expected_columns}")

# Insert Data
for _, row in df.iterrows():
    cursor.execute(
        """
        INSERT INTO Students (Student_ID, Gender, Internet_Access_at_Home, Extracurricular_Activities)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE Gender=VALUES(Gender),
                                Internet_Access_at_Home=VALUES(Internet_Access_at_Home),
                                Extracurricular_Activities=VALUES(Extracurricular_Activities)
        """,
        (
            row["Student_ID"],
            row["Gender"],
            row["Internet_Access_at_Home"],
            row["Extracurricular_Activities"]
        )
    )
db.commit()

# Close connection
cursor.close()
db.close()

print("Data inserted successfully!")
