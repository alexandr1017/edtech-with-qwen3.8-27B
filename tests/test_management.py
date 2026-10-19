"""Тесты management-эндпоинтов."""


async def _seed(client):
    student = await client.post("/students/", json={"name": "Alice", "age": 20})
    course = await client.post("/courses/", json={"name": "SQL", "price": 100, "duration": 5})
    teacher = await client.post("/teachers/", json={"name": "Ivan", "age": 35})
    return (
        student.json()["id"],
        course.json()["id"],
        teacher.json()["id"],
    )


async def test_enroll_and_unenroll(client):
    student_id, course_id, _teacher_id = await _seed(client)

    resp = await client.post(f"/management/?studentId={student_id}&courseId={course_id}")
    assert resp.status_code == 200

    # Дублирующая подписка — конфликт.
    resp = await client.post(f"/management/?studentId={student_id}&courseId={course_id}")
    assert resp.status_code == 409
    assert resp.json()["error"] == "CONFLICT"

    resp = await client.delete(f"/management?studentId={student_id}&courseId={course_id}")
    assert resp.status_code == 200

    # Повторное снятие — нет такой подписки.
    resp = await client.delete(f"/management?studentId={student_id}&courseId={course_id}")
    assert resp.status_code == 404


async def test_enroll_not_found(client):
    student_id, _course_id, _teacher_id = await _seed(client)

    resp = await client.post(f"/management/?studentId={student_id}&courseId=999")
    assert resp.status_code == 404


async def test_add_and_replace_teacher(client):
    _student_id, course_id, teacher_id = await _seed(client)

    resp = await client.put(f"/management/?teacherId={teacher_id}&courseId={course_id}&action=add")
    assert resp.status_code == 200

    # Уже назначен — конфликт.
    resp = await client.put(f"/management/?teacherId={teacher_id}&courseId={course_id}&action=add")
    assert resp.status_code == 409

    teacher2 = await client.post("/teachers/", json={"name": "Petr", "age": 30})
    teacher2_id = teacher2.json()["id"]

    resp = await client.put(
        f"/management/?teacherId={teacher2_id}&courseId={course_id}&action=replace"
    )
    assert resp.status_code == 200

    # Курс после замены преподавателя доступен.
    resp = await client.get(f"/courses/{course_id}")
    assert resp.status_code == 200

    teachers = await client.get("/teachers/")
    for t in teachers.json():
        if t["id"] == teacher2_id:
            assert [c["id"] for c in t["courses"]] == [course_id]


async def test_add_teacher_not_found(client):
    _student_id, course_id, _teacher_id = await _seed(client)

    resp = await client.put(f"/management/?teacherId=999&courseId={course_id}&action=add")
    assert resp.status_code == 404


async def test_bad_action_value(client):
    _student_id, course_id, teacher_id = await _seed(client)

    # Неизвестное действие — ошибка валидации FastAPI.
    resp = await client.put(
        f"/management/?teacherId={teacher_id}&courseId={course_id}&action=unknown"
    )
    assert resp.status_code == 422
