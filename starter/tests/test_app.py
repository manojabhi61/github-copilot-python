import pytest

from app import app, CURRENT


@pytest.fixture()
def client():
    app.config.update(TESTING=True)
    with app.test_client() as client:
        yield client


def test_flask_app_starts_correctly(client):
    assert client is not None
    assert app.name == "app"


def test_home_page_loads_successfully(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"<title>Sudoku Game</title>" in response.data


def test_existing_application_routes_still_work_without_logic_changes(client):
    response = client.get("/new?clues=35")
    assert response.status_code == 200
    data = response.get_json()

    assert "puzzle" in data
    assert isinstance(data["puzzle"], list)
    assert len(data["puzzle"]) == 9
    assert all(len(row) == 9 for row in data["puzzle"])

    assert CURRENT["puzzle"] is not None
    assert CURRENT["solution"] is not None

    assert CURRENT["solution"] is not None
    payload = {"board": CURRENT["solution"]}
    check_response = client.post("/check", json=payload)
    assert check_response.status_code == 200
    assert check_response.get_json() == {"incorrect": []}


def test_new_endpoint_accepts_difficulty_parameter(client):
    response = client.get("/new?difficulty=easy")
    assert response.status_code == 200
    data = response.get_json()
    assert "puzzle" in data
    assert len(data["puzzle"]) == 9
    assert all(len(row) == 9 for row in data["puzzle"])
