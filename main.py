from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
import os
from dotenv import load_dotenv
from typing import List, Optional

# Load environment variables
load_dotenv()

app = FastAPI()

# Database connection function using .env variables
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

# Pydantic Models
class Student(BaseModel):
    Student_ID: str
    Gender: str
    Parental_Education_Level: str
    Internet_Access_at_Home: str
    Extracurricular_Activities: str

class Performance(BaseModel):
    Student_ID: str
    Study_Hours_per_Week: float
    Attendance_Rate: float
    Past_Exam_Scores: float
    Final_Exam_Score: float

# CRUD for Students
@app.post("/students/", response_model=dict)
def create_student(student: Student):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Validate Education_ID exists
        if student.Parental_Education_Level is not None:
            cursor.execute("SELECT COUNT(*) FROM Parental_Education WHERE Education_ID = %s", 
                           (student.Parental_Education_Level,))
            if cursor.fetchone()[0] == 0:
                raise HTTPException(status_code=400, detail="Invalid Education_ID")

        cursor.execute(
            "INSERT INTO Students (Student_ID, Gender, Education_ID, Internet_Access_at_Home, Extracurricular_Activities) VALUES (%s, %s, %s, %s, %s)",
            (student.Student_ID, student.Gender, student.Parental_Education_Level, 
             student.Internet_Access_at_Home, student.Extracurricular_Activities)
        )
        conn.commit()
        return {"message": "Student added successfully!"}

    except mysql.connector.Error as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@app.get("/students/{student_id}", response_model=Student)
def read_student(student_id: str):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT Student_ID, Gender, Education_ID as Parental_Education_Level, Internet_Access_at_Home, Extracurricular_Activities FROM Students WHERE Student_ID = %s",
            (student_id,))
        student = cursor.fetchone()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        return student

    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()
        
@app.put("/students/{student_id}", response_model=dict)
def update_student(student_id: str, student: Student):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "UPDATE Students SET Gender=%s, Education_ID=%s, Internet_Access_at_Home=%s, Extracurricular_Activities=%s WHERE Student_ID=%s",
            (student.Gender, student.Parental_Education_Level, student.Internet_Access_at_Home, 
             student.Extracurricular_Activities, student_id)
        )
        conn.commit()
        return {"message": "Student updated successfully!"}

    except mysql.connector.Error as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@app.delete("/students/{student_id}", response_model=dict)
def delete_student(student_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM Students WHERE Student_ID = %s", (student_id,))
        conn.commit()
        return {"message": "Student deleted successfully!"}

    except mysql.connector.Error as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# CRUD for Performance
@app.post("/performance/", response_model=dict)
def create_performance(performance: Performance):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO Performance (Student_ID, Study_Hours_per_Week, Attendance_Rate, Past_Exam_Scores, Final_Exam_Score) VALUES (%s, %s, %s, %s, %s)",
            (performance.Student_ID, performance.Study_Hours_per_Week, performance.Attendance_Rate, 
             performance.Past_Exam_Scores, performance.Final_Exam_Score)
        )
        conn.commit()

        # Retrieve computed Pass_Fail
        cursor.execute("SELECT Pass_Fail FROM Performance WHERE Student_ID = %s", 
                       (performance.Student_ID,))
        pass_fail = cursor.fetchone()[0]

        return {"message": "Performance added successfully!", "Pass_Fail": pass_fail}

    except mysql.connector.Error as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@app.get("/performance/{student_id}")
def read_performance(student_id: str):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM Performance WHERE Student_ID = %s", (student_id,))
        performance = cursor.fetchone()
        if not performance:
            raise HTTPException(status_code=404, detail="Performance record not found")
        return performance

    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@app.put("/performance/{student_id}", response_model=dict)
def update_performance(student_id: str, performance: Performance):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "UPDATE Performance SET Study_Hours_per_Week=%s, Attendance_Rate=%s, Past_Exam_Scores=%s, Final_Exam_Score=%s WHERE Student_ID=%s",
            (performance.Study_Hours_per_Week, performance.Attendance_Rate, performance.Past_Exam_Scores, 
             performance.Final_Exam_Score, student_id)
        )
        conn.commit()

        # Retrieve updated Pass_Fail
        cursor.execute("SELECT Pass_Fail FROM Performance WHERE Student_ID = %s", (student_id,))
        pass_fail = cursor.fetchone()[0]

        return {"message": "Performance record updated successfully!", "Pass_Fail": pass_fail}

    except mysql.connector.Error as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@app.delete("/performance/{student_id}", response_model=dict)
def delete_performance(student_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM Performance WHERE Student_ID = %s", (student_id,))
        conn.commit()
        return {"message": "Performance record deleted successfully!"}

    except mysql.connector.Error as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# API to get average final exam score
@app.get("/performance/average_final_score")
def calculate_average_final_score():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.callproc("Calculate_Avg_Final_Score")
        for result in cursor.stored_results():
            avg_score = result.fetchone()[0]
            return {"Average_Final_Score": avg_score}

    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# Run FastAPI
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
