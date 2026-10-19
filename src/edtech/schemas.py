"""Pydantic-схемы домена edtech."""

from pydantic import BaseModel, ConfigDict, Field


class StudentCreate(BaseModel):
    """Создание студента (POST /students/)."""

    name: str = Field(min_length=1, max_length=128)
    age: int = Field(ge=0)


class StudentUpdate(StudentCreate):
    """Обновление студента (PUT /students/, id берётся из body)."""

    id: int


class CourseCreate(BaseModel):
    """Создание курса (POST /courses/)."""

    name: str = Field(min_length=1, max_length=128)
    price: float = Field(ge=0)
    duration: int = Field(gt=0)


class CourseUpdate(CourseCreate):
    """Обновление курса (PUT /courses/, id берётся из body)."""

    id: int


class TeacherCreate(BaseModel):
    """Создание преподавателя (POST /teachers/)."""

    name: str = Field(min_length=1, max_length=128)
    age: int = Field(ge=0)


class TeacherUpdate(TeacherCreate):
    """Обновление преподавателя (PUT /teachers/, id берётся из body)."""

    id: int


# --- Ответные модели (ORM -> Pydantic через from_attributes) ---


class CourseBrief(BaseModel):
    """Краткое представление курса во вложенных списках."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class StudentBrief(BaseModel):
    """Краткое представление студента во вложенных списках."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class StudentRead(BaseModel):
    """Студент; вложенный список курсов заполняется на GET /students/."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    age: int
    courses: list[CourseBrief] = []


class CourseRead(BaseModel):
    """Курс; вложенные списки заполняются на соответствующих GET-эндпоинтах."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    price: float
    duration: int
    students: list[StudentBrief] = []


class TeacherRead(BaseModel):
    """Преподаватель; вложенный список курсов заполняется на GET /teachers/."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    age: int
    courses: list[CourseBrief] = []


StudentRead.model_rebuild()
CourseRead.model_rebuild()
TeacherRead.model_rebuild()
