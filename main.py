from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Depends
from database import SessionLocal, get_db
from models import Student, Machine, Appointment
from sqlalchemy import select
from sqlalchemy.orm import Session
from datetime import time, date

app = FastAPI()


class StudentCreate(BaseModel): ## how a student-create object should look like
   name : str
   surname : str
   room_number : str

class StudentResponse(BaseModel):
    student_id: int
    name: str
    surname: str
    room_number: str

    model_config = {
        "from_attributes": True
    }


class MachineCreate(BaseModel):
   machine_number: str
   model : str
   outOfOrder: bool

   model_config = {
           "from_attributes": True
       }

class MachineResponse(BaseModel):
   machine_id : int
   machine_number : str
   model : str
   outOfOrder : bool

class AppointmentCreate(BaseModel):
   student_id : int
   appointment_date : date
   start_time : time
   end_time : time
   machine_count : int

   model_config = {
              "from_attributes": True
          }

class AppointmentResponse(BaseModel):
   appointment_date : date
   start_time : time
   end_time : time
   machine_count : int

   model_config = {
                 "from_attributes": True
             }




@app.get("/machines", response_model=list[MachineResponse])
def get_all_machines(db: Session = Depends(get_db)):

   statement = select(Machine) ## like an sql code, select * from students;

   result = db.execute(statement)

   machines = result.scalars().all()

   return machines

@app.get("/machines/{machine_id}", response_model=MachineResponse)
def get_machine(
   machine_id : int,
   db: Session = Depends(get_db)
   ):

   statement = select(Machine).where(Machine.machine_id == machine_id)

   result = db.execute(statement)

   machine = result.scalar_one_or_none()

   if machine is None:
      
      raise HTTPException(
         status_code=404,
         detail="Machine not found"
      )

   return machine

@app.post("/machines", response_model=MachineResponse) ## create a new machine
def create_machine(
   machine : MachineCreate,
   db: Session = Depends(get_db)
   ):
   
   new_machine = Machine(
      machine_number = machine.machine_number,
      model = machine.model,
      outOfOrder = machine.outOfOrder
   )

   db.add(new_machine)
   db.commit()
   db.refresh(new_machine)

   return new_machine

@app.get("/students", response_model=list[StudentResponse])
def get_all_students(db: Session = Depends(get_db)):

   statement = select(Student) ## like an sql code, select * from students;

   result = db.execute(statement)

   students = result.scalars().all()

   return students

@app.get("/students/{student_id}", response_model=StudentResponse)
def get_student(
   student_id : int,
   db: Session = Depends(get_db)
   ):

   statement = select(Student).where(Student.student_id == student_id)

   result = db.execute(statement)

   student = result.scalar_one_or_none()

   if student is None:
      
      raise HTTPException(
         status_code=404,
         detail="Student not found"
      )

   return student

@app.post("/students", response_model=StudentResponse) ## create a new student
def create_student(
   student : StudentCreate,
   db: Session = Depends(get_db)
   ):
   
   new_student = Student(
      name = student.name,
      surname = student.surname,
      room_number = student.room_number   
   )

   db.add(new_student)
   db.commit()
   db.refresh(new_student)

   return new_student

@app.post("/appointments", response_model=AppointmentResponse)
def create_appointment(
   appointment : AppointmentCreate,
   db : Session = Depends(get_db)
):

   statement = select(Student).where(Student.student_id == appointment.student_id) ## forms a query, stores the quiery in statement
   
   result = db.execute(statement) ## executes the query, stores the result in result
   
   student = result.scalar_one_or_none() ## ORM creates a student object, using the result (data >> backend object)

   if student is None: 
      raise HTTPException(
         status_code=404,
         detail="Student not found"
      )

   statement = select(Machine).where(Machine.outOfOrder == False)

   result = db.execute(statement)

   machines = result.scalars().all()

   available_machines = []

   for machine in machines:

      machine_is_available = True

        # Look at every appointment belonging to this machine
      for existing_appointment in machine.appointments:

            # Check whether the existing appointment is on the
            # same date and overlaps with the requested time
         if (
                existing_appointment.appointment_date
                == appointment.appointment_date
                and
                existing_appointment.start_time
                < appointment.end_time
                and
                existing_appointment.end_time
                > appointment.start_time
            ):
                machine_is_available = False
                break

        # If none of the machine's appointments conflicted,
        # this machine is available
      if machine_is_available:
            available_machines.append(machine)

   print("Available machines:", available_machines)

   if len(available_machines) < appointment.machine_count:
    raise HTTPException(
        status_code=409,
        detail="Not enough machines available for this time"
    )

   selected_machines = available_machines[:appointment.machine_count]

   new_appointment = Appointment(
        student_id=appointment.student_id,
        appointment_date=appointment.appointment_date,
        start_time=appointment.start_time,
        end_time=appointment.end_time,
        machine_count=appointment.machine_count
    )

   new_appointment.machines = selected_machines

   db.add(new_appointment)
   db.commit()
   db.refresh(new_appointment)

   return new_appointment
          
             

   