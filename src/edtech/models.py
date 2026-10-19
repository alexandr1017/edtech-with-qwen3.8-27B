"""ORM-модели домена edtech."""

from sqlalchemy import (
    ForeignKey,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base, TimestampMixin


class Teacher(Base, TimestampMixin):
    """Преподаватель."""

    __tablename__ = "teacher"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)

    courses: Mapped[list["Course"]] = relationship(back_populates="teacher", lazy="selectin")


class Course(Base, TimestampMixin):
    """Курс."""

    __tablename__ = "course"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    duration: Mapped[int] = mapped_column(Integer, nullable=False)

    teacher_id: Mapped[int | None] = mapped_column(ForeignKey("teacher.id"), nullable=True)

    teacher: Mapped["Teacher | None"] = relationship(back_populates="courses")

    students: Mapped[list["Student"]] = relationship(
        secondary="student_course", back_populates="courses", lazy="selectin"
    )


class Student(Base, TimestampMixin):
    """Студент."""

    __tablename__ = "student"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)

    courses: Mapped[list["Course"]] = relationship(
        secondary="student_course", back_populates="students", lazy="selectin"
    )


class StudentCourse(Base):
    """Связь студент-курс."""

    __tablename__ = "student_course"
    __table_args__: tuple = (UniqueConstraint("student_id", "course_id", name="uq_student_course"),)

    student_id: Mapped[int] = mapped_column(ForeignKey("student.id"), primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("course.id"), primary_key=True)


Base.registry.configure()
