"""Бизнес-логика домена edtech."""

from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.edtech import exceptions as exc
from src.edtech.models import Course, Student, Teacher


async def get_student(session: AsyncSession, student_id: int) -> Student:
    """Возвращает студента или бросает NotFoundError."""
    student = await session.get(Student, student_id)
    if student is None:
        raise exc.NotFoundError()
    return student


async def get_course(session: AsyncSession, course_id: int) -> Course:
    """Возвращает курс или бросает NotFoundError."""
    course = await session.get(Course, course_id)
    if course is None:
        raise exc.NotFoundError()
    return course


async def get_teacher(session: AsyncSession, teacher_id: int) -> Teacher:
    """Возвращает преподавателя или бросает NotFoundError."""
    teacher = await session.get(Teacher, teacher_id)
    if teacher is None:
        raise exc.NotFoundError()
    return teacher


async def list_students_with_courses(session: AsyncSession) -> list[dict[str, Any]]:
    """Список студентов вместе с их курсами."""
    students = (await session.scalars(select(Student).order_by(Student.id))).all()
    return [
        {
            "id": s.id,
            "name": s.name,
            "age": s.age,
            "courses": [
                {"id": c.id, "name": c.name} for c in sorted(s.courses, key=lambda c: c.id)
            ],
        }
        for s in students
    ]


async def list_courses_with_students(session: AsyncSession) -> list[dict[str, Any]]:
    """Список курсов вместе с подписанными студентами."""
    courses = (await session.scalars(select(Course).order_by(Course.id))).all()
    return [
        {
            "id": c.id,
            "name": c.name,
            "price": float(c.price),
            "duration": c.duration,
            "students": [
                {"id": s.id, "name": s.name} for s in sorted(c.students, key=lambda s: s.id)
            ],
        }
        for c in courses
    ]


async def list_teachers_with_courses(session: AsyncSession) -> list[dict[str, Any]]:
    """Список преподавателей вместе с их курсами."""
    teachers = (await session.scalars(select(Teacher).order_by(Teacher.id))).all()
    return [
        {
            "id": t.id,
            "name": t.name,
            "age": t.age,
            "courses": [
                {"id": c.id, "name": c.name} for c in sorted(t.courses, key=lambda c: c.id)
            ],
        }
        for t in teachers
    ]


async def create_student(session: AsyncSession, data) -> dict[str, Any]:
    """Создаёт студента."""
    student = Student(name=data.name, age=data.age)
    session.add(student)
    await session.flush()
    return {"id": student.id, "name": student.name, "age": student.age, "courses": []}


async def read_student(session: AsyncSession, student_id: int) -> dict[str, Any]:
    """Студент со списком курсов."""
    student = await get_student(session, student_id)
    return {
        "id": student.id,
        "name": student.name,
        "age": student.age,
        "courses": [
            {"id": c.id, "name": c.name} for c in sorted(student.courses, key=lambda c: c.id)
        ],
    }


async def create_course(session: AsyncSession, data) -> dict[str, Any]:
    """Создаёт курс."""
    course = Course(name=data.name, price=data.price, duration=data.duration)
    session.add(course)
    await session.flush()
    return {
        "id": course.id,
        "name": course.name,
        "price": float(course.price),
        "duration": course.duration,
        "students": [],
    }


async def read_course(session: AsyncSession, course_id: int) -> dict[str, Any]:
    """Курс со списком подписанных студентов."""
    course = await get_course(session, course_id)
    return {
        "id": course.id,
        "name": course.name,
        "price": float(course.price),
        "duration": course.duration,
        "students": [
            {"id": s.id, "name": s.name} for s in sorted(course.students, key=lambda s: s.id)
        ],
    }


async def create_teacher(session: AsyncSession, data) -> dict[str, Any]:
    """Создаёт преподавателя."""
    teacher = Teacher(name=data.name, age=data.age)
    session.add(teacher)
    await session.flush()
    return {"id": teacher.id, "name": teacher.name, "age": teacher.age, "courses": []}


async def read_teacher(session: AsyncSession, teacher_id: int) -> dict[str, Any]:
    """Преподаватель со списком его курсов."""
    teacher = await get_teacher(session, teacher_id)
    return {
        "id": teacher.id,
        "name": teacher.name,
        "age": teacher.age,
        "courses": [
            {"id": c.id, "name": c.name} for c in sorted(teacher.courses, key=lambda c: c.id)
        ],
    }


async def update_student(session: AsyncSession, data) -> dict[str, Any]:
    """Обновляет данные студента по id из body."""
    student = await get_student(session, data.id)
    student.name = data.name
    student.age = data.age
    return {"id": student.id, "name": student.name, "age": student.age}


async def delete_student(session: AsyncSession, student_id: int) -> None:
    """Удаляет студента и его подписки на курсы."""
    student = await get_student(session, student_id)
    await session.delete(student)


async def update_course(session: AsyncSession, data) -> dict[str, Any]:
    """Обновляет данные курса по id из body."""
    course = await get_course(session, data.id)
    course.name = data.name
    course.price = data.price
    course.duration = data.duration
    return {
        "id": course.id,
        "name": course.name,
        "price": float(course.price),
        "duration": course.duration,
        "students": [],
    }


async def delete_course(session: AsyncSession, course_id: int) -> None:
    """Удаляет курс и связанные подписки."""
    course = await get_course(session, course_id)
    await session.delete(course)


async def update_teacher(session: AsyncSession, data) -> dict[str, Any]:
    """Обновляет данные преподавателя по id из body."""
    teacher = await get_teacher(session, data.id)
    teacher.name = data.name
    teacher.age = data.age
    return {"id": teacher.id, "name": teacher.name, "age": teacher.age}


async def delete_teacher(session: AsyncSession, teacher_id: int) -> None:
    """Удаляет преподавателя; его курсы остаются без преподавателя."""
    teacher = await get_teacher(session, teacher_id)
    for course in teacher.courses:
        course.teacher_id = None
    await session.delete(teacher)


async def enroll_student(session: AsyncSession, student_id: int, course_id: int) -> None:
    """Подписывает студента на курс; ConflictError при дубликате."""
    student = await get_student(session, student_id)
    course = await get_course(session, course_id)
    if course.id in {c.id for c in student.courses}:
        raise exc.ConflictError()
    student.courses.append(course)


async def unenroll_student(session: AsyncSession, student_id: int, course_id: int) -> None:
    """Снимает студента с курса; NotFoundError если подписки нет."""
    student = await get_student(session, student_id)
    course = await get_course(session, course_id)
    if course.id not in {c.id for c in student.courses}:
        raise exc.NotFoundError()
    student.courses.remove(course)


async def add_teacher_to_course(session: AsyncSession, teacher_id: int, course_id: int) -> Course:
    """Назначает преподавателя на курс; ConflictError при дубликате."""
    course = await get_course(session, course_id)
    if course.teacher_id is not None:
        raise exc.ConflictError()
    teacher = await get_teacher(session, teacher_id)
    course.teacher_id = teacher.id
    return course


async def replace_course_teacher(session: AsyncSession, teacher_id: int, course_id: int) -> Course:
    """Заменяет текущего преподавателя курса."""
    course = await get_course(session, course_id)
    teacher = await get_teacher(session, teacher_id)
    course.teacher_id = teacher.id
    return course
