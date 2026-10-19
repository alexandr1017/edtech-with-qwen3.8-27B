"""REST-эндпоинты домена edtech (спецификация edTechREST)."""

from typing import Annotated, Literal

from fastapi import APIRouter, Query, status

from src.edtech import schemas as sch
from src.edtech import service as edtech_service
from src.edtech.dependencies import DbDep

router = APIRouter(tags=["edtech"])


@router.get("/students/{student_id}", response_model=sch.StudentRead)
async def get_student(student_id: int, db: DbDep):
    """Получить студента по id."""
    return await edtech_service.read_student(db, student_id)


@router.get("/courses/{course_id}", response_model=sch.CourseRead)
async def get_course(course_id: int, db: DbDep):
    """Получить курс по id."""
    return await edtech_service.read_course(db, course_id)


@router.get("/teachers/{teacher_id}", response_model=sch.TeacherRead)
async def get_teacher(teacher_id: int, db: DbDep):
    """Получить преподавателя по id."""
    return await edtech_service.read_teacher(db, teacher_id)


@router.get("/students/", response_model=list[sch.StudentRead])
async def list_students(db: DbDep):
    """Список всех студентов со списком курсов каждого студента."""
    return await edtech_service.list_students_with_courses(db)


@router.get("/courses/", response_model=list[sch.CourseRead])
async def list_courses(db: DbDep):
    """Список всех курсов со списком студентов, подписанных на каждый курс."""
    return await edtech_service.list_courses_with_students(db)


@router.get("/teachers/", response_model=list[sch.TeacherRead])
async def list_teachers(db: DbDep):
    """Список всех преподавателей со списком их курсов."""
    return await edtech_service.list_teachers_with_courses(db)


@router.post(
    "/students/",
    response_model=sch.StudentRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_student(data: sch.StudentCreate, db: DbDep):
    """Добавить студента."""
    return await edtech_service.create_student(db, data)


@router.post(
    "/courses/",
    response_model=sch.CourseRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_course(data: sch.CourseCreate, db: DbDep):
    """Добавить курс."""
    return await edtech_service.create_course(db, data)


@router.post(
    "/teachers/",
    response_model=sch.TeacherRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_teacher(data: sch.TeacherCreate, db: DbDep):
    """Добавить преподавателя."""
    return await edtech_service.create_teacher(db, data)


@router.put("/students/", response_model=sch.StudentRead)
async def update_student(data: sch.StudentUpdate, db: DbDep):
    """Обновить данные студента по id из body."""
    return await edtech_service.update_student(db, data)


@router.put("/courses/", response_model=sch.CourseRead)
async def update_course(data: sch.CourseUpdate, db: DbDep):
    """Обновить данные курса по id из body."""
    return await edtech_service.update_course(db, data)


@router.put("/teachers/", response_model=sch.TeacherRead)
async def update_teacher(data: sch.TeacherUpdate, db: DbDep):
    """Обновить данные преподавателя по id из body."""
    return await edtech_service.update_teacher(db, data)


@router.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(student_id: int, db: DbDep):
    """Удалить студента по id."""
    await edtech_service.delete_student(db, student_id)


@router.delete("/courses/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(course_id: int, db: DbDep):
    """Удалить курс по id."""
    await edtech_service.delete_course(db, course_id)


@router.post("/management/")
async def enroll_student(
    studentId: Annotated[int, Query(...)],  # noqa: N803
    courseId: Annotated[int, Query(...)],  # noqa: N803
    db: DbDep,
) -> dict[str, str]:
    """Подписать студента на курс."""
    await edtech_service.enroll_student(db, studentId, courseId)
    return {"detail": f"Student {studentId} enrolled into course {courseId}"}


@router.post("/management")  # noqa: D103
async def enroll_student_no_slash(
    studentId: Annotated[int, Query(...)],  # noqa: N803
    courseId: Annotated[int, Query(...)],  # noqa: N803
    db: DbDep,
) -> dict[str, str]:
    """Подписать студента на курс (URL без завершающего слеша)."""
    return await enroll_student(studentId, courseId, db)


@router.put("/management/")
async def manage_course_teacher(
    teacherId: Annotated[int, Query(...)],  # noqa: N803
    courseId: Annotated[int, Query(...)],  # noqa: N803
    action: Literal["add", "replace"],
    db: DbDep,
) -> dict[str, str]:
    """Добавить (action=add) или заменить (action=replace) преподавателя курса."""
    if action == "add":
        await edtech_service.add_teacher_to_course(db, teacherId, courseId)
    else:
        await edtech_service.replace_course_teacher(db, teacherId, courseId)
    return {"detail": f"Course {courseId} now taught by teacher {teacherId}"}


@router.put("/management")  # noqa: D103
async def manage_course_teacher_no_slash(
    teacherId: Annotated[int, Query(...)],  # noqa: N803
    courseId: Annotated[int, Query(...)],  # noqa: N803
    action: Literal["add", "replace"],
    db: DbDep,
) -> dict[str, str]:
    """Добавить или заменить преподавателя курса (URL без завершающего слеша)."""
    return await manage_course_teacher(teacherId, courseId, action, db)


@router.delete("/management/")
async def unenroll_student(
    studentId: Annotated[int, Query(...)],  # noqa: N803
    courseId: Annotated[int, Query(...)],  # noqa: N803
    db: DbDep,
) -> dict[str, str]:
    """Снять студента с курса."""
    await edtech_service.unenroll_student(db, studentId, courseId)
    return {"detail": f"Student {studentId} removed from course {courseId}"}


@router.delete("/management")  # noqa: D103
async def unenroll_student_no_slash(
    studentId: Annotated[int, Query(...)],  # noqa: N803
    courseId: Annotated[int, Query(...)],  # noqa: N803
    db: DbDep,
) -> dict[str, str]:
    """Снять студента с курса (URL без завершающего слеша)."""
    return await unenroll_student(studentId, courseId, db)
