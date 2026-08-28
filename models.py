from sqlalchemy import String, Time, Date, ForeignKey, Table, Column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import time, date

class Base(DeclarativeBase):
  pass


appointment_machines = Table(
"appointment_machines",
Base.metadata,
Column(
    "appointment_id",
    ForeignKey("appointments.appointment_id"),
    primary_key=True
),
Column(
  "machine_id",
  ForeignKey("machines.machine_id"),
  primary_key=True
)
)


class Student(Base): ## creating the empty table in the database, to be filled with students
  __tablename__ = "students"

  student_id: Mapped[int] = mapped_column(primary_key=True)
  name: Mapped[str] = mapped_column(String(20))
  surname: Mapped[str] = mapped_column(String(20))
  room_number: Mapped[str] = mapped_column(String(4))

  appointments = relationship("Appointment", back_populates="student")


class Machine(Base):
  __tablename__ = "machines"

  machine_id: Mapped[int] = mapped_column(primary_key=True)
  machine_number: Mapped[str] = mapped_column(String(3))
  model: Mapped[str] = mapped_column(String(50))
  outOfOrder: Mapped[bool] = mapped_column(default=False)

  appointments = relationship(
    "Appointment",
    secondary=appointment_machines,
    back_populates="machines"
  )

class Appointment(Base):
  __tablename__ = "appointments"

  appointment_id: Mapped[int] = mapped_column(primary_key=True)
  student_id : Mapped[int] = mapped_column(
    ForeignKey("students.student_id")
    )
  appointment_date: Mapped[date] = mapped_column(Date)
  start_time: Mapped[time] = mapped_column(Time)  
  end_time: Mapped[time] = mapped_column(Time)
  machine_count: Mapped[int] = mapped_column()

  student = relationship("Student", back_populates="appointments") 

  machines = relationship(
    "Machine",
    secondary=appointment_machines,
    back_populates="appointments"
  )

