import copy
import random

SIZE = 9
EMPTY = 0

def deep_copy(board):
    return copy.deepcopy(board)

def create_empty_board():
    return [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]

def is_safe(board, row, col, num):
    # Check row and column.
    for index in range(SIZE):
        if board[row][index] == num or board[index][col] == num:
            return False

    # Check the 3x3 box.
    start_row = row - row % 3
    start_col = col - col % 3
    for row_offset in range(3):
        for col_offset in range(3):
            if board[start_row + row_offset][start_col + col_offset] == num:
                return False

    return True

def fill_board(board):
    for row_index in range(SIZE):
        for col_index in range(SIZE):
            if board[row_index][col_index] != EMPTY:
                continue

            candidates = list(range(1, SIZE + 1))
            random.shuffle(candidates)

            for candidate in candidates:
                if not is_safe(board, row_index, col_index, candidate):
                    continue

                board[row_index][col_index] = candidate
                if fill_board(board):
                    return True
                board[row_index][col_index] = EMPTY

            return False

    return True


def find_empty_cell(board):
    for row_index in range(SIZE):
        for col_index in range(SIZE):
            if board[row_index][col_index] == EMPTY:
                return row_index, col_index
    return None


def count_solutions(board, limit=2):
    empty_cell = find_empty_cell(board)
    if empty_cell is None:
        return 1

    row_index, col_index = empty_cell
    solution_count = 0
    candidates = list(range(1, SIZE + 1))
    random.shuffle(candidates)

    for candidate in candidates:
        if not is_safe(board, row_index, col_index, candidate):
            continue

        board[row_index][col_index] = candidate
        solution_count += count_solutions(board, limit)
        board[row_index][col_index] = EMPTY

        if solution_count >= limit:
            return solution_count

    return solution_count


def remove_cells(board, clues):
    cells_to_remove = SIZE * SIZE - clues
    positions = [
        (row_index, col_index)
        for row_index in range(SIZE)
        for col_index in range(SIZE)
    ]
    random.shuffle(positions)

    for row_index, col_index in positions:
        if cells_to_remove <= 0:
            break

        if board[row_index][col_index] == EMPTY:
            continue

        original_value = board[row_index][col_index]
        board[row_index][col_index] = EMPTY

        if count_solutions(board, limit=2) != 1:
            board[row_index][col_index] = original_value
            continue

        cells_to_remove -= 1

def generate_puzzle(clues=35):
    """Create a Sudoku puzzle and its solved board."""
    board = create_empty_board()
    fill_board(board)

    solution = deep_copy(board)
    puzzle = deep_copy(solution)

    remove_cells(puzzle, clues)
    return puzzle, solution
