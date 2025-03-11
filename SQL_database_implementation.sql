CREATE DATABASE IF NOT EXISTS student_performance_db;
USE student_performance_db;

-- Drop existing tables to allow recreation
DROP TABLE IF EXISTS Performance;
DROP TABLE IF EXISTS Students;
DROP TABLE IF EXISTS Parental_Education;

-- Create the Parental_Education table
CREATE TABLE Parental_Education (
    Education_ID INT AUTO_INCREMENT PRIMARY KEY,
    Education_Level ENUM('High School', 'Bachelors', 'Masters', 'PhD') NOT NULL
);

-- Insert the defined education levels
INSERT INTO Parental_Education (Education_Level) VALUES
('High School'), ('Bachelors'), ('Masters'), ('PhD');

-- Create the Students table
CREATE TABLE Students (
    Student_ID VARCHAR(10) PRIMARY KEY,
    Gender ENUM('Male', 'Female') NOT NULL,
    Education_ID INT,  -- Matches the Parental_Education table
    Internet_Access_at_Home ENUM('Yes', 'No') NOT NULL,
    Extracurricular_Activities ENUM('Yes', 'No') NOT NULL,  
    FOREIGN KEY (Education_ID) REFERENCES Parental_Education(Education_ID)
);

-- Create the Performance table
CREATE TABLE Performance (
    Performance_ID INT AUTO_INCREMENT PRIMARY KEY,
    Student_ID VARCHAR(10),
    Study_Hours_per_Week FLOAT NOT NULL,
    Attendance_Rate FLOAT NOT NULL,
    Past_Exam_Scores FLOAT NOT NULL,
    Final_Exam_Score FLOAT NOT NULL,
    Pass_Fail ENUM('Pass', 'Fail') NOT NULL,
    FOREIGN KEY (Student_ID) REFERENCES Students(Student_ID)
);


-- Add an index on Student_ID for performance optimization
#CREATE INDEX idx_student_id ON Performance(Student_ID);

-- Stored Procedure: Calculate the average final exam score
DROP PROCEDURE IF EXISTS Calculate_Avg_Final_Score;
DELIMITER //
CREATE PROCEDURE Calculate_Avg_Final_Score()
BEGIN
    SELECT AVG(Final_Exam_Score) AS Average_Final_Score FROM Performance;
END //
DELIMITER ;


-- Drop triggers if they exist
DROP TRIGGER IF EXISTS Set_Pass_Fail_Insert;
DROP TRIGGER IF EXISTS Set_Pass_Fail_Update;

-- Trigger for INSERT
DELIMITER //
CREATE TRIGGER Set_Pass_Fail_Insert
BEFORE INSERT ON Performance
FOR EACH ROW
BEGIN
    IF NEW.Final_Exam_Score >= 60 THEN
        SET NEW.Pass_Fail = 'Pass';
    ELSE
        SET NEW.Pass_Fail = 'Fail';
    END IF;
END //
DELIMITER ;

-- Trigger for UPDATE
DELIMITER //
CREATE TRIGGER Set_Pass_Fail_Update
BEFORE UPDATE ON Performance
FOR EACH ROW
BEGIN
    IF NEW.Final_Exam_Score >= 60 THEN
        SET NEW.Pass_Fail = 'Pass';
    ELSE
        SET NEW.Pass_Fail = 'Fail';
    END IF;
END //
DELIMITER ;

-- View all records in key tables
SELECT * FROM Students;
SELECT * FROM Performance;
SELECT * FROM Parental_Education;
