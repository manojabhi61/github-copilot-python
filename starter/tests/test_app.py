import pytest

import sudoku_logic
from app import app, CURRENT, is_valid_board


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
    assert b'"player-name"' in response.data
    assert b"Top 10 Leaderboard" in response.data
    assert b'id="leaderboard-table"' in response.data
    assert b"<th>Rank</th>" in response.data
    assert b"<th>Name</th>" in response.data
    assert b"<th>Time</th>" in response.data
    assert b"<th>Level</th>" in response.data
    assert b"<th>Hints</th>" in response.data


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

    payload = {"board": CURRENT["solution"]}
    check_response = client.post("/check", json=payload)
    assert check_response.status_code == 200

    result = check_response.get_json()
    assert result["incorrect"] == []
    assert "correct" in result
    assert isinstance(result["correct"], list)


def test_check_route_returns_400_for_missing_or_malformed_board(client):
    response = client.post("/check", data="not-json", content_type="application/json")
    assert response.status_code == 400
    assert response.get_json() == {"error": "A 9x9 board is required"}

    missing_board_response = client.post("/check", json={})
    assert missing_board_response.status_code == 400
    assert missing_board_response.get_json() == {"error": "A 9x9 board is required"}


def test_hint_route_returns_400_for_missing_json_body(client):
    client.get("/new?difficulty=easy")

    response = client.post("/hint", data="not-json", content_type="application/json")

    assert response.status_code == 400
    assert response.get_json() == {"error": "A 9x9 board is required"}


def test_hint_route_returns_400_for_invalid_board_shape(client):
    client.get("/new?difficulty=easy")
    valid_board = sudoku_logic.deep_copy(CURRENT["solution"])
    assert is_valid_board(valid_board)

    invalid_board = valid_board[:8]
    response = client.post("/hint", json={"board": invalid_board})

    assert response.status_code == 400
    assert response.get_json() == {"error": "A 9x9 board is required"}
    assert not is_valid_board(invalid_board)


def test_hint_route_returns_400_for_invalid_board_values(client):
    client.get("/new?difficulty=easy")
    valid_board = sudoku_logic.deep_copy(CURRENT["solution"])
    assert is_valid_board(valid_board)

    invalid_board = sudoku_logic.deep_copy(valid_board)
    invalid_board[0][0] = 10
    response = client.post("/hint", json={"board": invalid_board})

    assert response.status_code == 400
    assert response.get_json() == {"error": "A 9x9 board is required"}
    assert not is_valid_board(invalid_board)


def test_check_route_returns_400_for_invalid_board_dimensions(client):
    client.get("/new?difficulty=easy")
    valid_board = sudoku_logic.deep_copy(CURRENT["solution"])
    assert is_valid_board(valid_board)

    invalid_board = valid_board[:8]
    response = client.post("/check", json={"board": invalid_board})

    assert response.status_code == 400
    assert response.get_json() == {"error": "A 9x9 board is required"}
    assert not is_valid_board(invalid_board)


def test_check_route_returns_400_for_invalid_cell_values(client):
    client.get("/new?difficulty=easy")
    valid_board = sudoku_logic.deep_copy(CURRENT["solution"])
    assert is_valid_board(valid_board)

    invalid_board = sudoku_logic.deep_copy(valid_board)
    invalid_board[0][0] = -1
    response = client.post("/check", json={"board": invalid_board})

    assert response.status_code == 400
    assert response.get_json() == {"error": "A 9x9 board is required"}
    assert not is_valid_board(invalid_board)


def test_new_endpoint_accepts_difficulty_parameter(client):
    response = client.get("/new?difficulty=easy")
    assert response.status_code == 200
    data = response.get_json()
    assert "puzzle" in data
    assert len(data["puzzle"]) == 9
    assert all(len(row) == 9 for row in data["puzzle"])


def test_difficulty_parameter_changes_prefilled_cell_counts(client):
    easy_response = client.get("/new?difficulty=easy")
    medium_response = client.get("/new?difficulty=medium")
    hard_response = client.get("/new?difficulty=hard")

    easy_puzzle = easy_response.get_json()["puzzle"]
    medium_puzzle = medium_response.get_json()["puzzle"]
    hard_puzzle = hard_response.get_json()["puzzle"]

    easy_clues = sum(cell != 0 for row in easy_puzzle for cell in row)
    medium_clues = sum(cell != 0 for row in medium_puzzle for cell in row)
    hard_clues = sum(cell != 0 for row in hard_puzzle for cell in row)

    assert easy_clues > medium_clues > hard_clues


def test_generated_puzzle_has_exactly_one_solution():
    puzzle, _ = sudoku_logic.generate_puzzle(35)
    solution_count = sudoku_logic.count_solutions(
        sudoku_logic.deep_copy(puzzle),
        limit=2,
    )

    assert solution_count == 1


def test_hint_route_fills_exactly_one_empty_cell(client):
    response = client.get("/new?difficulty=easy")
    assert response.status_code == 200

    before_hint = sudoku_logic.deep_copy(CURRENT["puzzle"])
    empty_cells_before = sum(
        cell == sudoku_logic.EMPTY for row in before_hint for cell in row
    )

    hint_response = client.post("/hint")
    assert hint_response.status_code == 200

    data = hint_response.get_json()
    assert set(data) == {"row", "col", "value"}

    row = data["row"]
    col = data["col"]
    value = data["value"]

    assert CURRENT["puzzle"][row][col] == value
    assert CURRENT["solution"][row][col] == value

    empty_cells_after = sum(
        cell == sudoku_logic.EMPTY for row in CURRENT["puzzle"] for cell in row
    )
    assert empty_cells_after == empty_cells_before - 1


def test_hint_route_returns_error_when_no_empty_cells_available(client):
    client.get("/new?difficulty=easy")

    for row in range(sudoku_logic.SIZE):
        for col in range(sudoku_logic.SIZE):
            CURRENT["puzzle"][row][col] = CURRENT["solution"][row][col]

    hint_response = client.post("/hint")
    assert hint_response.status_code == 400
    assert hint_response.get_json()["error"] == "No empty cells available"


def test_hint_route_uses_the_player_board_and_does_not_overwrite_existing_value(client):
    client.get("/new?difficulty=easy")

    player_board = sudoku_logic.deep_copy(CURRENT["puzzle"])
    first_empty = next(
        (row, col)
        for row in range(sudoku_logic.SIZE)
        for col in range(sudoku_logic.SIZE)
        if player_board[row][col] == sudoku_logic.EMPTY
    )
    player_board[first_empty[0]][first_empty[1]] = 5

    hint_response = client.post("/hint", json={"board": player_board})
    assert hint_response.status_code == 200

    data = hint_response.get_json()
    assert (data["row"], data["col"]) != first_empty
    assert player_board[first_empty[0]][first_empty[1]] == 5


def test_check_route_reports_incorrect_and_correct_user_cells(client):
    client.get("/new?difficulty=easy")

    original_puzzle = sudoku_logic.deep_copy(CURRENT["puzzle"])
    board = sudoku_logic.deep_copy(CURRENT["solution"])

    empty_positions = [
        (row, col)
        for row in range(sudoku_logic.SIZE)
        for col in range(sudoku_logic.SIZE)
        if original_puzzle[row][col] == sudoku_logic.EMPTY
    ]
    wrong_row, wrong_col = empty_positions[0]
    board[wrong_row][wrong_col] = (board[wrong_row][wrong_col] % 9) + 1

    check_response = client.post("/check", json={"board": board})
    result = check_response.get_json()

    assert result["incorrect"] == [[wrong_row, wrong_col]]
    assert len(result["correct"]) == len(empty_positions) - 1
