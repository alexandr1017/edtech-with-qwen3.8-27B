"""Тесты CRUD-эндпоинтов студентов, курсов и преподавателей."""


async def test_create_and_get_student(client):
    resp = await client.post("/students/", json={"name": "Alice", "age": 20})
    assert resp.status_code == 201
    student_id = resp.json()["id"]

    resp = await client.get(f"/students/{student_id}")
    assert resp.status_code == 200
    body = resp.json()
    assert body["name"] == "Alice"
    assert body["age"] == 20
    assert body["courses"] == []


async def test_create_student_validation_error(client):
    resp = await client.post("/students/", json={"name": "", "age": -1})
    assert resp.status_code == 422


async def test_update_student(client):
    created = await client.post("/students/", json={"name": "Alice", "age": 20})
    student_id = created.json()["id"]

    resp = await client.put("/students/", json={"id": student_id, "name": "Bob", "age": 21})
    assert resp.status_code == 200
    body = resp.json()
    assert body["name"] == "Bob"
    assert body["age"] == 21


async def test_update_student_not_found(client):
    resp = await client.put("/students/", json={"id": 999, "name": "X", "age": 1})
    assert resp.status_code == 404
    assert resp.json()["error"] == "NOT_FOUND"


async def test_delete_student(client):
    created = await client.post("/students/", json={"name": "Alice", "age": 20})
    student_id = created.json()["id"]

    resp = await client.delete(f"/students/{student_id}")
    assert resp.status_code == 204

    resp = await client.get(f"/students/{student_id}")
    assert resp.status_code == 404


async def test_list_students_with_courses(client):
    student1 = (await client.post("/students/", json={"name": "S1", "age": 18})).json()
    course_resp = await client.post("/courses/", json={"name": "SQL", "price": 100, "duration": 5})
    course1 = course_resp.json()

    await client.post(f"/management/?studentId={student1['id']}&courseId={course1['id']}")

    resp = await client.get("/students/")
    assert resp.status_code == 200
    body = resp.json()
    assert len(body) == 1
    assert [c["name"] for c in body[0]["courses"]] == ["SQL"]


async def test_course_crud(client):
    created = await client.post(
        "/courses/", json={"name": "Portuguese", "price": 500, "duration": 10}
    )
    assert created.status_code == 201
    course_id = created.json()["id"]

    resp = await client.get(f"/courses/{course_id}")
    assert resp.status_code == 200
    body = resp.json()
    assert body["name"] == "Portuguese"
    assert body["students"] == []

    resp = await client.put(
        "/courses/", json={"id": course_id, "name": "Spanish", "price": 600, "duration": 12}
    )
    assert resp.status_code == 200
    assert resp.json()["name"] == "Spanish"

    resp = await client.delete(f"/courses/{course_id}")
    assert resp.status_code == 204

    resp = await client.get(f"/courses/{course_id}")
    assert resp.status_code == 404


async def test_list_courses_with_students(client):
    student1 = (await client.post("/students/", json={"name": "S1", "age": 18})).json()
    course_resp = await client.post("/courses/", json={"name": "SQL", "price": 100, "duration": 5})
    course1 = course_resp.json()

    await client.post(f"/management/?studentId={student1['id']}&courseId={course1['id']}")

    resp = await client.get("/courses/")
    assert resp.status_code == 200
    body = resp.json()
    assert [s["name"] for s in body[0]["students"]] == ["S1"]


async def test_teacher_crud(client):
    created = await client.post("/teachers/", json={"name": "Ivan", "age": 35})
    assert created.status_code == 201
    teacher_id = created.json()["id"]

    resp = await client.get(f"/teachers/{teacher_id}")
    assert resp.status_code == 200
    assert resp.json()["courses"] == []

    course_resp = await client.post("/courses/", json={"name": "SQL", "price": 10, "duration": 1})
    course1 = course_resp.json()
    await client.put(f"/management/?teacherId={teacher_id}&courseId={course1['id']}&action=add")

    resp = await client.get("/teachers/")
    assert resp.status_code == 200
    body = resp.json()
    assert [c["name"] for c in body[0]["courses"]] == ["SQL"]

    resp = await client.put("/teachers/", json={"id": teacher_id, "name": "Ivan P.", "age": 36})
    assert resp.status_code == 200
    assert resp.json()["name"] == "Ivan P."
