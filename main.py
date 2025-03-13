from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
from typing import List, Optional

app = FastAPI()

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Marion@2020",
        database="student_performance_db"
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



        
