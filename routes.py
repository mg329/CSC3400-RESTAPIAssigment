from fastapi import APIRouter, HTTPException, Body
from models import Student
from database import get_connection

router = APIRouter()

@router.get("/students")
def get_all_students():
    
    #Opens the connection to the students database
    conn = get_connection()
    
    #Creates an executor to run SQL commands
    cursor = conn.cursor()

    #Retrieves every column from the students database
    cursor.execute("SELECT * FROM students")
    
    #Returns a list of the rows from the students database
    rows = cursor.fetchall()

    #Converts the rows to dictionaries so the FastAPI can handle them
    students = [dict(row) for row in rows]

    #Closes the connection with the students database
    conn.close()

    #Returns all student records in the appropriate format
    return {"students": students, "count": len(students)}

@router.get("/students/by-major")
def get_students_by_major(major: str):
    
    #Opens the connection to the students database
    conn = get_connection()

    #Creates an executor to run SQL commands
    cursor = conn.cursor()

    #Retrieves every column from the students database with the chosen major
    cursor.execute("SELECT * FROM students WHERE major=?", (major,))

    #Returns a list of the rows from the students database by the chosen major
    rows = cursor.fetchall()

    #Converts the rows to dictionaries so the FastAPI can handle them
    students = [dict(row) for row in rows]

    #Closes the connection with the students database
    conn.close()

    #Returns all student records for that major in the appropriate format
    return {"students": students, "count": len(students), "major": major}

@router.get("/students/by-gpa") # TODO: Replace ??? with correct endpoint path
def get_students_by_gpa(min_gpa: float):
    
    #Validation Error
    if min_gpa < 0.0 or min_gpa > 4.0:
        raise HTTPException(status_code=400, detail="GPA must be between 0.0 and 4.0")

    #Opens the connection to the students database
    conn = get_connection()

    #Creates an executor to run SQL commands
    cursor = conn.cursor()

    #Retrieves every column from the students database with the minimum gpa
    cursor.execute("SELECT * FROM students WHERE gpa >= ?", (min_gpa,))

    #Returns a list of the rows from the students database with the minimum gpa
    rows = cursor.fetchall()

    #Converts the rows to dictionaries so the FastAPI can handle them
    students = [dict(row) for row in rows]

    #Closes the connection with the students database
    conn.close()

    #Returns all student records with that minimum gpa in the appropriate format
    return {"students": students, "count": len(students), "min_gpa": min_gpa}

@router.get("/students/{student_id}")
def get_student(student_id: int):

    #Opens the connection to the students database
    conn = get_connection()

    #Creates an executor to run SQL commands
    cursor = conn.cursor()

    #Retrieves the column from the students database with the student id
    cursor.execute("SELECT * FROM students WHERE id=?", (student_id,))

    #Returns a list of the row from the students database with the student id
    row = cursor.fetchone()

    #Closes the connection with the students database
    conn.close()

    #Validation Error
    if not row:
        raise HTTPException(status_code=404, detail=f"Student with ID {student_id} not found")

    #Returns the student record with that student id in the appropriate format
    return dict(row)

@router.post("/students", status_code=201)
def create_student(student: Student):

    #Validation Error
    if not student.name.strip():
        raise HTTPException(status_code=400, detail="Name connot be empty")

    #Validation Error
    if not student.major.strip():
        raise HTTPException(status_code=400, detail="Major cannot be empty")

    #Validation Error
    if student.gpa < 0.0 or student.gpa > 4.0:
        raise HTTPException(status_code=400, detail="GPA must be between 0.0 and 4.0")

    #Opens the connection to the students database
    conn = get_connection()

    #Creates an executor to run SQL commands
    cursor = conn.cursor()

    #Inserts a new student record into the student database
    cursor.execute("""INSERT INTO students (name, email, major, gpa, enrollment_year) VALUES (?, ?, ?, ?, ?)""", (student.name, student.email, student.major, student.gpa, student.enrollment_year))

    #Saves changes to the database
    conn.commit()

    #Gets the id of the student that was just inserted
    new_id = cursor.lastrowid

    #Retrieves the column from the students database with the new student id
    cursor.execute("SELECT * FROM students WHERE id=?", (new_id,))

    #Returns a list of the row from the students database with the new student id
    row = cursor.fetchone()

    #Closes the connection with the students database
    conn.close()

    #Returns the student record with that new student id in the appropriate format
    return dict(row)

@router.put("/students/{student_id}") # TODO:
def update_student(student_id: int, student: Student):

    #Validation Error
    if not student.name.strip():
        raise HTTPException(status_code=400, detail="Name cannot be empty")

    #Validation Error
    if not student.major.strip():
        raise HTTPException(status_code=400, detail="Major cannot be empty")

    #Validation Error
    if student.gpa < 0.0 or student.gpa > 4.0:
        raise HTTPException(status_code=400, detail="GPA must be between 0.0 and 4.0")

    #Opens the connection to the students database
    conn = get_connection()

    #Creates an executor to run SQL commands
    cursor = conn.cursor()

    #Retrieves the column from the students database with the student id
    cursor.execute("SELECT * FROM students WHERE id=?", (student_id,))

    #Checks if the student id was found in the students database
    if not cursor.fetchone():

        #If the student id wasn't found, the connection with the database is closed
        conn.close()

        #Validation Error
        raise HTTPException(status_code=404, detail=f"Student with ID {student_id} not found")

    #Updates the found student record with the new data
    cursor.execute("""UPDATE students SET name=?, email=?, major=?, gpa=?, enrollment_year=? WHERE id=?""", (student.name, student.email, student.major, student.gpa, student.enrollment_year, student_id))

    #Saves changes to the database
    conn.commit()
    
    #Retrieves the column from the students database with the student id
    cursor.execute("SELECT * FROM students WHERE id=?", (student_id,))    
    
    #Returns a list of the row from the students database with the student id
    row = cursor.fetchone()

    #Closes the connection with the students database
    conn.close()

    #Returns the student record with that new student id in the appropriate format
    return dict(row)

@router.delete("/students/{student_id}")
def delete_student(student_id: int):

    #Opens the connection to the students database
    conn = get_connection()

    #Creates an executor to run SQL commands
    cursor = conn.cursor()

    #Retrieves the column from the students database with the student id
    cursor.execute("SELECT * FROM students WHERE id=?", (student_id,))

    #Checks if the student id was found in the students database
    if not cursor.fetchone():

        #If the student id wasn't found, the connection with the database is closed
        conn.close()

        #Validation Error
        raise HTTPException(status_code=404, detail=f"Student with ID {student_id} not found")

    #Deletes the student with the associated student id from the students database
    cursor.execute("DELETE FROM students WHERE id=?", (student_id,))

    #Saves changes to the database
    conn.commit()

    #Closes the connection with the students database
    conn.close()

    #Returns the appropriate message to alert that the student was sucessfully defeated
    return {"message": "Student deleted successfully"}
