from flask import Flask, render_template, jsonify, request
import sudoku_logic

app = Flask(__name__)

DIFFICULTY_CLUES = {
    'easy': 45,
    'medium': 35,
    'hard': 28,
}

DEFAULT_CLUES = 35

# Keep a simple in-memory store for current puzzle and solution
CURRENT = {
    'puzzle': None,
    'solution': None
}


def resolve_clues():
    difficulty = request.args.get('difficulty', '').strip().lower()
    if difficulty in DIFFICULTY_CLUES:
        return DIFFICULTY_CLUES[difficulty]

    clues = request.args.get('clues')
    if clues is not None:
        try:
            return int(clues)
        except (TypeError, ValueError):
            return DEFAULT_CLUES

    return DEFAULT_CLUES


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/new')
def new_game():
    clues = resolve_clues()
    puzzle, solution = sudoku_logic.generate_puzzle(clues)
    CURRENT['puzzle'] = puzzle
    CURRENT['solution'] = solution
    return jsonify({'puzzle': puzzle})

@app.route('/check', methods=['POST'])
def check_solution():
    data = request.json
    board = data.get('board')
    solution = CURRENT.get('solution')
    puzzle = CURRENT.get('puzzle')

    if solution is None or puzzle is None:
        return jsonify({'error': 'No game in progress'}), 400

    incorrect = []
    correct = []

    for i in range(sudoku_logic.SIZE):
        for j in range(sudoku_logic.SIZE):
            if puzzle[i][j] != sudoku_logic.EMPTY:
                continue

            if board[i][j] == solution[i][j]:
                correct.append([i, j])
            else:
                incorrect.append([i, j])

    return jsonify({'incorrect': incorrect, 'correct': correct})


@app.route('/hint', methods=['POST'])
def give_hint():
    puzzle = CURRENT.get('puzzle')
    solution = CURRENT.get('solution')
    if puzzle is None or solution is None:
        return jsonify({'error': 'No game in progress'}), 400

    for row in range(sudoku_logic.SIZE):
        for col in range(sudoku_logic.SIZE):
            if puzzle[row][col] == sudoku_logic.EMPTY:
                puzzle[row][col] = solution[row][col]
                return jsonify({
                    'row': row,
                    'col': col,
                    'value': solution[row][col]
                })

    return jsonify({'error': 'No empty cells available'}), 400


if __name__ == '__main__':
    import os

    if __name__ == "__main__":
        port = int(os.environ.get("PORT", 5000))
        app.run(host="0.0.0.0", port=port)