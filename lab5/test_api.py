"""ЛР5: автотесты REST API (requests + pytest), повторяют логику тестов из Postman."""
import re

import pytest
import requests

BASE_URL = "https://jsonplaceholder.typicode.com"
USER_ID = 1
HEADERS = {"Content-Type": "application/json; charset=UTF-8"}
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@pytest.fixture(scope="module")
def session():
    s = requests.Session()
    s.headers.update(HEADERS)
    yield s
    s.close()


class TestGetUser:
    @pytest.fixture(scope="class")
    def response(self, session):
        return session.get(f"{BASE_URL}/users/{USER_ID}", timeout=10)

    def test_status_code(self, response):
        assert response.status_code == 200

    def test_content_type(self, response):
        assert "application/json" in response.headers["Content-Type"]

    def test_response_time(self, response):
        assert response.elapsed.total_seconds() < 2

    def test_json_structure(self, response):
        user = response.json()
        assert set(user) == {"id", "name", "username", "email", "address", "phone", "website", "company"}
        assert {"street", "city", "zipcode", "geo"} <= set(user["address"])
        assert "name" in user["company"]

    def test_field_types(self, response):
        user = response.json()
        assert isinstance(user["id"], int)
        assert isinstance(user["name"], str)
        assert isinstance(user["email"], str)

    def test_field_values(self, response):
        user = response.json()
        assert user["id"] == USER_ID
        assert user["name"] == "Leanne Graham"
        assert user["username"] == "Bret"
        assert EMAIL_RE.match(user["email"])


class TestCreateUser:
    PAYLOAD = {"name": "Maria Tumanova", "username": "mtumanova",
               "email": "maria@example.com", "job": "QA engineer"}

    @pytest.fixture(scope="class")
    def response(self, session):
        return session.post(f"{BASE_URL}/users", json=self.PAYLOAD, timeout=10)

    def test_status_code(self, response):
        assert response.status_code == 201

    def test_json_structure(self, response):
        assert set(response.json()) == {"id", "name", "username", "email", "job"}

    def test_new_id(self, response):
        body = response.json()
        assert isinstance(body["id"], int)
        assert body["id"] == 11

    def test_values_match_request(self, response):
        body = response.json()
        for key, value in self.PAYLOAD.items():
            assert body[key] == value


class TestUpdateUser:
    PAYLOAD = {"id": 1, "name": "Leanne Graham-Updated", "username": "Bret",
               "email": "leanne.updated@example.com", "job": "Team lead"}

    @pytest.fixture(scope="class")
    def response(self, session):
        return session.put(f"{BASE_URL}/users/{USER_ID}", json=self.PAYLOAD, timeout=10)

    def test_status_code(self, response):
        assert response.status_code == 200

    def test_json_structure(self, response):
        assert set(response.json()) == {"id", "name", "username", "email", "job"}

    def test_id_unchanged(self, response):
        assert response.json()["id"] == USER_ID

    def test_fields_updated(self, response):
        body = response.json()
        assert body["name"] == "Leanne Graham-Updated"
        assert body["job"] == "Team lead"
        assert body["email"] == "leanne.updated@example.com"
