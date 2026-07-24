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
    if solution is None:
        return jsonify({'error': 'No game in progress'}), 400
    incorrect = []
    for i in range(sudoku_logic.SIZE):
        for j in range(sudoku_logic.SIZE):
            if board[i][j] != solution[i][j]:
                incorrect.append([i, j])
    return jsonify({'incorrect': incorrect})

if __name__ == '__main__':
    app.run(debug=True)