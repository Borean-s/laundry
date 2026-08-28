from datetime import date, time

from database import SessionLocal
from models import Student, Machine, Appointment


db = SessionLocal()

student = db.get(Student, 1)

machine1 = db.get(Machine, 1)
machine2 = db.get(Machine, 2)

appointment = Appointment(
    student=student,
    appointment_date=date(2026, 7, 15),
    start_time=time(13, 0),
    end_time=time(14, 0),
    machine_count=2
)

appointment.machines = [machine1, machine2]

db.add(appointment)
db.commit()

db.close()