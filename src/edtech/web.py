"""Веб-страницы для управления сервисом edtech."""

from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.edtech import schemas as sch
from src.edtech import service as edtech_service
from src.edtech.dependencies import DbDep

router = APIRouter(tags=["web"])

TEMPLATE_DIR: Path = Path(__file__).parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))


@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, db: DbDep):
    """Дашборд со статистикой и графиками."""
    raw_students = await edtech_service.list_students_with_courses(db)
    raw_courses = await edtech_service.list_courses_with_students(db)
    raw_teachers = await edtech_service.list_teachers_with_courses(db)

    students = [sch.StudentRead.model_validate(s) for s in raw_students]
    courses = [sch.CourseRead.model_validate(c) for c in raw_courses]
    teachers = [sch.TeacherRead.model_validate(t) for t in raw_teachers]

    revenue: float = sum(c.price * len(c.students) for c in courses)
    enrollments: int = sum(len(c.students) for c in courses)
    course_load = [{"name": c.name, "students": len(c.students)} for c in courses]
    teacher_load = [
        {"name": t.name, "courses": len(t.courses), "price_sum": sum(x.price for x in t.courses)}
        for t in teachers
    ]

    return templates.TemplateResponse(
        request,
        "dashboard.html",
        {
            "students": students,
            "courses": courses,
            "teachers": teachers,
            "revenue": revenue,
            "enrollments": enrollments,
            "course_load": course_load,
            "teacher_load": teacher_load,
        },
    )


@router.get("/students", response_class=HTMLResponse)
async def students_page(request: Request, db: DbDep):
    """Страница управления студентами."""
    raw_students = await edtech_service.list_students_with_courses(db)
    raw_courses = await edtech_service.list_courses_with_students(db)
    students = [sch.StudentRead.model_validate(s) for s in raw_students]
    courses = [sch.CourseRead.model_validate(c) for c in raw_courses]
    enrolled_map: dict[int, list[int]] = {s.id: [c.id for c in s.courses] for s in students}
    return templates.TemplateResponse(
        request,
        "students.html",
        {"students": students, "courses": courses, "enrolled_map": enrolled_map},
    )


@router.get("/courses", response_class=HTMLResponse)
async def courses_page(request: Request, db: DbDep):
    """Страница управления курсами."""
    raw_students = await edtech_service.list_students_with_courses(db)
    raw_courses = await edtech_service.list_courses_with_students(db)
    raw_teachers = await edtech_service.list_teachers_with_courses(db)
    students = [sch.StudentRead.model_validate(s) for s in raw_students]
    courses = [sch.CourseRead.model_validate(c) for c in raw_courses]
    teachers = [sch.TeacherRead.model_validate(t) for t in raw_teachers]
    return templates.TemplateResponse(
        request, "courses.html", {"students": students, "courses": courses, "teachers": teachers}
    )


@router.get("/teachers", response_class=HTMLResponse)
async def teachers_page(request: Request, db: DbDep):
    """Страница управления преподавателями."""
    raw_teachers = await edtech_service.list_teachers_with_courses(db)
    raw_courses = await edtech_service.list_courses_with_students(db)
    teachers = [sch.TeacherRead.model_validate(t) for t in raw_teachers]
    courses = [sch.CourseRead.model_validate(c) for c in raw_courses]
    return templates.TemplateResponse(
        request, "teachers.html", {"teachers": teachers, "courses": courses}
    )
