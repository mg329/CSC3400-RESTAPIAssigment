# Student Record Management REST API

## Overview
A RESTful API built **FastAPI** and **SQLite** for managing student records. This API allows users to create, read, update, delete and filter student data.

## Installation Instructions

### 1. Clone the Repository and Navigate to the Root Directory
`git clone`

`cd student-api`

### 2. Create and Activate Virtual Enviroment
`python -m venv .venv`

`source .venv\Scripts\activate`

### 3. Install Dependencies
`pip install -r requirements.txt`

### 4. Run the Server
`uvicorn main:app --reload`

### 5. Navigate to the Server at:
`http://127.0.0.1:8000`

## API Endpoints:

-GET/students/

-GET/students/{id}

-POST/students

-PUT/students/{id}

-DELETE/students/{id}

-GET/students/by-major

-GET/students/by-gpa

## Testing Instructions:

### 1. Run the Server

### 2. Navigate to:

`http://127.0.0.1:8000/docs`

### 3. Try each endpoint interactively using FastAPI's built in documentation

## Example Requests:

-POST/students

    {
        "name": "Jack Smith",
        "email": "jack@university.edu",
        "major": "Computer Science",
        "gpa": 3.9,
        "enrollment_year": 2025
    }

-PUT/students/1

    {
        "name": "Jack Smith",
        "email": "jack@university.edu",
        "major": "Computer Science",
        "gpa": 4.0,
        "enrollment_year": 2025
    }
    
-GET/students/by-gpa?min_gpa=3.5
