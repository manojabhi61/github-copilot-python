# GitHub Copilot Instructions

# Sudoku Project

The Sudoku application has been refactored and enhanced with several new features to improve gameplay, usability, and responsiveness.

## Features Implemented

- Refactored the existing Sudoku codebase using GitHub Copilot.
- Added automated testing using Pytest.
- Implemented three difficulty levels:
  - Easy
  - Medium
  - Hard
- Difficulty level determines the number of prefilled cells.
- Implemented Sudoku puzzle generation with exactly one unique solution.
- Locked all prefilled cells to prevent editing.
- Added a player name input field.
- Added a game timer to track completion time.
- Added a New Game button.
- Added a Hint button that reveals exactly one correct empty cell and locks it.
- Added a Check Solution button to validate user entries.
- Implemented live validation for invalid moves.
- Highlighted conflicting cells in rows, columns, and 3×3 boxes.
- Displayed a congratulatory message when the puzzle is solved correctly.
- Added Dark Mode and Light Mode toggle.
- Persisted the selected theme using Local Storage.
- Implemented a Top 10 leaderboard.
- Stored leaderboard data using Local Storage.
- Leaderboard stores:
  - Player Name
  - Difficulty Level
  - Completion Time
  - Number of Hints Used
- Leaderboard is automatically sorted by fastest completion time.
- Leaderboard retains only the fastest 10 completed games.
- Leaderboard persists after page refresh or browser restart.
- Applied alternating colors to each 3×3 Sudoku sub-grid for better readability.
- Improved overall UI styling using responsive design.
- Optimized the layout for desktop, tablet, and mobile devices.
- Ensured buttons, text, forms, and Sudoku cells remain readable across different screen sizes.
- Preserved all existing functionality while adding new features.
- Verified functionality using Pytest, with all tests passing successfully.

## Technologies Used

- Python
- Flask
- HTML5
- CSS3
- JavaScript
- Bootstrap 5
- Pytest
- Local Storage
- Git
- GitHub
- GitHub Copilot

## Testing

Run the following commands:

```bash
pip install -r requirements.txt
python -m pytest -q
python app.py