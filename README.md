# Student Performance Prediction and Management System

## Overview

This project implements a web-based system for managing student data and predicting their final exam scores. It leverages a FastAPI backend, a MySQL database for persistent storage, and a machine learning model for making predictions. The system allows for CRUD (Create, Read, Update, Delete) operations on student and performance data and uses a pre-trained model to predict final exam scores based on several factors.

## Features

*   **Student Management:**
    *   Add new student records to the system.
    *   Retrieve details of specific students.
    *   Update existing student information.
    *   Delete student records.
*   **Performance Tracking:**
    *   Record student academic performance data (study hours, attendance, past scores, final score).
    *   Retrieve a student's performance details.
    *   Update existing performance records.
    *   Delete performance records.
    * Calculate the Pass_Fail value for each Performance.
*   **Prediction:**
    *   Fetch data for a student using the API.
    *   Load a pre-trained machine learning model.
    *   Prepare data for prediction.
    *   Predict the student's final exam score.
*   **Database:** Uses a MySQL database for persistent data storage.
*   **API:** Implemented using FastAPI, providing a RESTful API.
* **Model training:** includes a `train_model.py` to train the model, and save it.
* **API connection:** there is a script to fetch data from the api.
* **Deployed API:** the api is deployed on render.
* **Dataset:** includes a `student_performance_dataset.csv` that you can use to train the model, and populate the DB.

## Prerequisites

*   **Python 3.8+**
*   **MySQL Database** (with appropriate credentials)
*   **Python Packages:** Install the required packages using:

    ```bash
    pip install fastapi uvicorn mysql-connector-python pandas scikit-learn joblib python-dotenv requests
    ```

## Setup and Installation

1.  **Clone the Repository:**

    ```bash
    git clone <your_repository_url>
    cd database-design-group-3
    ```

2.  **Database Setup:**
    *   Create a MySQL database (if it doesn't exist).
    *   Update the `.env` file with your database credentials:

        ```
        DB_HOST=your_db_host
        DB_USER=your_db_user
        DB_PASSWORD=your_db_password
        DB_NAME=your_db_name
        ```

    *   Run `insert_data_sql_db.py` to populate the database with initial data (this will need to be adapted if your database has different table names/columns).
        ```bash
        python insert_data_sql_db.py
        ```
3. **Create the directories:**
    * Run this commands to create the required directories:
    ```bash
    mkdir data
    mkdir model_training
    mkdir models
    ```

4.  **Data setup**
    * Move the `student_performance_dataset.csv` file into `data` directory.

5.  **Train the Model:**
    *   Run the model training script:

        ```bash
        python model_training/train_model.py
        ```
    * This will create the `model.pkl` file on `models/` directory.

6.  **Run the FastAPI Application:**

    ```bash
    uvicorn main:app --reload
    ```
    The API will be available at `http://localhost:8000`.

7. **Test with the API:**
    * Post new data using: `http://localhost:8000/performance/` or `http://localhost:8000/students/`
    * Test the other endpoints.

## Code Overview

*   **`main.py`:** Contains the FastAPI application. Defines API endpoints for student and performance management.
*   **`insert_data_sql_db.py`:**  Populates the database with data from the `student_performance_dataset.csv` file.
*   **`fetch_and_predict.py`:** Fetches student data, loads the machine learning model, prepares data, and makes predictions.
*   **`model_training/train_model.py`:** Trains the machine learning model, preprocesses data, and saves the model as `model.pkl` in the `models/` directory.

## Model Details

*   **Model:** Linear Regression.
*   **Features:**  Study_Hours_per_Week, Attendance_Rate, Past_Exam_Scores and others.
*   **Target:** Final_Exam_Score.
*   **Preprocessing:** The data is preprocessed using `StandardScaler` for numeric columns and `OneHotEncoder` for categorical columns.

## API Endpoints
*   **Student Management:**
*   **`POST /students/`:** Create a new student.
*   **`GET /students/{student_id}`:** Get a student's details.
*   **`PUT /students/{student_id}`:** Update a student's information.
*   **`DELETE /students/{student_id}`:** Delete a student.

*   **Performance Tracking:**
*   **`POST /performance/`:** Create a new performance record.
*   **`GET /performance/{student_id}`:** Get a performance record.
*   **`PUT /performance/{student_id}`:** Update a performance record.
*   **`DELETE /performance/{student_id}`:** Delete a performance record.
*   **`GET /students/latest`:** returns the latest student.

## Deployment

* The Api is deployed on render, you can access it through this link: `https://database-design-group-3.onrender.com/`

## License

This project is licensed under the MIT License
