"""Тесты веб-страниц."""


async def test_dashboard_renders(client):
    await client.post("/students/", json={"name": "Alice", "age": 20})

    resp = await client.get("/")
    assert resp.status_code == 200
    assert "Дашборд" in resp.text
    assert "Alice" in resp.text


async def test_students_page_renders(client):
    await client.post("/students/", json={"name": "Bob", "age": 21})

    resp = await client.get("/students")
    assert resp.status_code == 200
    assert "Bob" in resp.text


async def test_courses_page_renders(client):
    await client.post("/courses/", json={"name": "SQL", "price": 1, "duration": 1})

    resp = await client.get("/courses")
    assert resp.status_code == 200
    assert "SQL" in resp.text


async def test_teachers_page_renders(client):
    await client.post("/teachers/", json={"name": "Ivan", "age": 35})

    resp = await client.get("/teachers")
    assert resp.status_code == 200
    assert "Ivan" in resp.text


async def test_static_css_served(client):
    resp = await client.get("/static/style.css")
    assert resp.status_code == 200


async def test_health(client):
    resp = await client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}
