from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException

app = FastAPI()

class Student(BaseModel): ## how a student object should look like
  student_id : int
  name : str
  surname : str
  room_number : str

class StudentCreate(BaseModel): ## how a student-create object should look like
   student_id : int
   name : str
   surname : str
   room_number : str


class Machine(BaseModel):
   pass

class Appointment(BaseModel):
   pass


students = [  ## creating student objects to test
    Student(
        student_id=1,
        name="Ali",
        surname="Yilmaz",
        room_number="B101"
    ),
    Student(
        student_id=2,
        name="Mehmet",
        surname="Kaya",
        room_number="C204"
    )
]


@app.get("/")
def home():
  return {"hello" : "world!"}

@app.post("/students", response_model=Student) ## create a new student
def create_stduent(student : StudentCreate):

   new_id = len(students) + 1
   
   new_student = Student(
      student_id = new_id,
      name = student.name,
      surname = student.surname,
      room_number = student.room_number   
   )

   students.append(new_student)

   return new_student

@app.get("/students", response_model=list[Student]) ## get a list of all existing students
def get_all_students():
  return students

@app.get("/students/{student_id}", response_model=Student) ## get an existing student
def get_student(student_id: int):
    for student in students:
        if student.student_id == student_id:
            return student


    raise HTTPException(
       status_code=404,
       detail="Student not found"
    )