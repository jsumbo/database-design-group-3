import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

def create_connection():
    """ create a database connection to a MySQL database """
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except Error as e:
        print(e)

def create_db():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE DATABASE IF NOT EXISTS StudentPerformanceDB;
        USE StudentPerformanceDB;

        CREATE TABLE IF NOT EXISTS Students (
            Student_ID VARCHAR(10) PRIMARY KEY,
            Gender ENUM('Male', 'Female') NOT NULL,
            Parental_Education_Level INT,
            Internet_Access_at_Home ENUM('Yes', 'No') NOT NULL,
            Extracurricular_Activities ENUM('Yes', 'No') NOT NULL
        );

        CREATE TABLE IF NOT EXISTS ParentalEducation (
            Education_ID INT PRIMARY KEY,
            Education_Level VARCHAR(50) NOT NULL
        );

        CREATE TABLE IF NOT EXISTS Performance (
            Performance_ID INT PRIMARY KEY,
            Student_ID VARCHAR(10),
            Study_Hours_per_Week INT NOT NULL,
            Attendance_Rate FLOAT NOT NULL,
            Past_Exam_Scores INT NOT NULL,
            Final_Exam_Score INT NOT NULL,
            Pass_Fail ENUM('Pass', 'Fail'),
            FOREIGN KEY (Student_ID) REFERENCES Students(Student_ID)
        );
    """)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_db()