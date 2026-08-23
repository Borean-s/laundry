from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Student(BaseModel):
  student_id : int
  name : str
  surname : str
  room_number : str

class StudentCreate(BaseModel):
   student_id : int
   name : str
   surname : str
   room_number : str


class Machine(BaseModel):
   pass

class Appointment(BaseModel):
   pass


students = [
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

@app.post("/students")
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

@app.get("/students")
def get_all_students():
  return students

@app.get("/students/{student_id}")
def get_student(student_id: int):
    for student in students:
        if student.student_id == student_id:
            return student