import os
import pandas as pd
import mysql.connector

# Database credentials
DB_HOST = "localhost"  
DB_USER = "root"      
DB_PASSWORD = "password"  
DB_NAME = "student_db"    

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
        INSERT INTO Performance (Student_ID, Study_Hours_per_Week, Attendance_Rate, Past_Exam_Scores, Final_Exam_Score, Pass_Fail)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (
            row["Student_ID"],
            row["Study_Hours_per_Week"],
            row["Attendance_Rate"],
            row["Past_Exam_Scores"],
            row["Final_Exam_Score"],
            row["Pass_Fail"]
        )
    )

db.commit()

# Close connection
cursor.close()
db.close()

print("Data inserted successfully!")