import pandas as pd
import mysql.connector

# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Marion@2020",
    database="student_performance_db"
)
cursor = db.cursor()

# Load CSV file
df = pd.read_csv("student_performance_dataset.csv")

# Expected column names
expected_columns = {
    "Student_ID", "Gender", "Parental_Education_Level", "Internet_Access_at_Home",
    "Extracurricular_Activities", "Study_Hours_per_Week", "Attendance_Rate",
    "Past_Exam_Scores", "Final_Exam_Score", "Pass_Fail"
}

if not expected_columns.issubset(df.columns):
    raise ValueError(f"Column names do not match expected names: {expected_columns}")

# Fixed mapping for education levels
fixed_edu_map = {
    "High School": 1,
    "Bachelors": 2,
    "Masters": 3,
    "PhD": 4
}

# Insert into Parental_Education table with explicit IDs
for level, edu_id in fixed_edu_map.items():
    cursor.execute(
        """
        INSERT INTO Parental_Education (Education_ID, Education_Level)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE Education_Level=VALUES(Education_Level)
        """,
        (edu_id, level)
    )
db.commit()

# Fetch education level IDs for mapping
cursor.execute("SELECT Education_ID, Education_Level FROM Parental_Education")
edu_map = {row[1]: row[0] for row in cursor.fetchall()}


# Insert data into Students table (handling duplicates)
for _, row in df.iterrows():
    education_id = edu_map.get(row["Parental_Education_Level"])

    if education_id is None:
        print(f"Warning: Education level '{row['Parental_Education_Level']}' not found. Skipping student {row['Student_ID']}.")
        continue

    try:
        cursor.execute(
            """
            INSERT INTO Students (Student_ID, Gender, Education_ID, Internet_Access_at_Home, Extracurricular_Activities)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE Gender=VALUES(Gender),
                                    Education_ID=VALUES(Education_ID),
                                    Internet_Access_at_Home=VALUES(Internet_Access_at_Home),
                                    Extracurricular_Activities=VALUES(Extracurricular_Activities)
            """,
            (
                row["Student_ID"],
                row["Gender"],
                education_id,
                row["Internet_Access_at_Home"],
                row["Extracurricular_Activities"]
            )
        )
    except KeyError as e:
        print(f"Skipping student {row['Student_ID']} due to missing key: {e}")
db.commit()

# Insert data into Performance table (handling duplicates)
for _, row in df.iterrows():
    try:
        pass_fail_value = str(row["Pass_Fail"]).strip().capitalize() if isinstance(row["Pass_Fail"], str) else 'Fail'
        
        cursor.execute(
            """
            INSERT INTO Performance (Student_ID, Study_Hours_per_Week, Attendance_Rate, Past_Exam_Scores, Final_Exam_Score, Pass_Fail)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE Study_Hours_per_Week=VALUES(Study_Hours_per_Week),
                                    Attendance_Rate=VALUES(Attendance_Rate),
                                    Past_Exam_Scores=VALUES(Past_Exam_Scores),
                                    Final_Exam_Score=VALUES(Final_Exam_Score),
                                    Pass_Fail=VALUES(Pass_Fail)
            """,
            (
                row["Student_ID"],
                row["Study_Hours_per_Week"],
                row["Attendance_Rate"],
                row["Past_Exam_Scores"],
                row["Final_Exam_Score"],
                pass_fail_value
            )
        )
    except KeyError as e:
        print(f"Skipping student {row['Student_ID']} due to missing key: {e}")
db.commit()

# Close connection
cursor.close()
db.close()

print("Data inserted successfully!")
