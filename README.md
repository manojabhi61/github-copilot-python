# Sudoku Game using Flask and GitHub Copilot

## Project Overview

This project is an enhanced version of the original Flask-based Sudoku application provided as part of the GitHub Copilot learning assignment. The application was refactored and extended using GitHub Copilot to improve code quality, user experience, backend validation, automated testing, and gameplay functionality while preserving the original application architecture.

The project demonstrates how GitHub Copilot can assist throughout the software development lifecycle, including code refactoring, feature implementation, debugging, testing, and documentation. Every Copilot-generated suggestion was reviewed, validated, and refined before being accepted into the codebase.

---

# Project Objectives

The primary objectives of this project were to:

- Refactor the existing Sudoku application while maintaining functionality.
- Improve code readability and maintainability.
- Implement additional gameplay features.
- Improve backend request validation.
- Enhance the user interface.
- Increase automated test coverage.
- Demonstrate responsible usage of GitHub Copilot.
- Produce a production-ready Sudoku web application.

---

# Features

## Gameplay Features

### Difficulty Selection

The application supports three difficulty levels:

- Easy
- Medium
- Hard

Each difficulty level generates Sudoku puzzles with a different number of prefilled cells while ensuring a unique solution.

---

### Unique Sudoku Puzzle Generation

Every generated puzzle is validated to ensure that only one valid solution exists. This prevents ambiguous Sudoku boards and improves gameplay quality.

---

### Hint System

The Hint feature provides assistance by revealing one correct value at a time.

Features include:

- Fills only an empty cell
- Never overwrites player-entered values
- Locks hinted cells after insertion
- Tracks the total number of hints used

---

### Check Solution

Players can verify their current progress without revealing the complete puzzle solution.

The application:

- Validates entered values
- Highlights incorrect entries
- Highlights correct entries
- Allows continued gameplay

---

### Automatic Puzzle Completion

The application automatically detects when the puzzle has been solved correctly.

When completed:

- Timer stops automatically
- Congratulations message appears
- Leaderboard updates automatically

---

### Timer

A built-in timer records the total puzzle completion time.

The timer:

- Starts automatically
- Updates continuously
- Stops immediately after puzzle completion

---

## Leaderboard

The application maintains a Top 10 leaderboard.

Each record stores:

- Player Name
- Completion Time
- Difficulty Level
- Hint Count

Leaderboard Features:

- Automatically updates after puzzle completion
- Persists using browser Local Storage
- Keeps only the fastest ten completed games
- Survives browser refreshes

---

## Validation Features

### Real-Time Validation

Player input is validated immediately.

Incorrect entries are highlighted automatically.

Highlights disappear after correction.

---

### Conflict Detection

Conflicting numbers are detected for:

- Rows
- Columns
- 3×3 Sub-grids

---

### Backend Validation

The Flask backend validates:

- Missing JSON requests
- Invalid board sizes
- Invalid board values
- Malformed requests

Proper HTTP error responses are returned whenever invalid data is received.

---

## User Interface

The application includes:

- Responsive Layout
- Dark Mode
- Improved Leaderboard
- Improved Control Layout
- Better Mobile Support
- Clean Sudoku Board
- Better User Feedback

---

# Technologies Used

## Backend

- Python
- Flask

## Frontend

- HTML5
- CSS3
- JavaScript
- Bootstrap

## Testing

- Pytest

## Version Control

- Git
- GitHub

## AI Development

- GitHub Copilot

---

# Project Structure

```
github-copilot-python/
│
├── starter/
│   ├── app.py
│   ├── sudoku_logic.py
│   ├── requirements.txt
│   ├── instruction.md
│   ├── templates/
│   ├── static/
│   ├── tests/
│   └── ...
│
├── README.md
├── LICENSE.txt
└── CODEOWNERS
```

---

# Installation

Clone the repository

```bash
git clone https://github.com/manojabhi61/github-copilot-python.git
```

Move into the project

```bash
cd github-copilot-python/starter
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install required packages

```bash
pip install -r requirements.txt
```

---

# Running the Application

Start the Flask server

```bash
python app.py
```

Open your browser and visit

```
http://127.0.0.1:5000
```

---

# Running Automated Tests

Execute all automated tests

```bash
python -m pytest -q
```

Expected Result

```
16 passed
```

---

# Manual Testing Checklist

Verify the following functionality:

- Difficulty selection
- New Game generation
- Hint functionality
- Check Solution
- Invalid move highlighting
- Conflict highlighting
- Automatic puzzle completion
- Congratulations message
- Timer start and stop
- Leaderboard update
- Leaderboard persistence
- Top 10 leaderboard
- Dark mode
- Responsive layout

---

# GitHub Copilot Usage

GitHub Copilot was used during the development process for:

- Refactoring Python code
- Generating Flask routes
- Improving Sudoku algorithms
- Writing JavaScript logic
- Enhancing HTML
- Improving CSS
- Creating automated tests
- Debugging application issues
- Backend validation
- UI improvements

All AI-generated code was reviewed before acceptance.

Whenever necessary:

- Suggestions were refined
- Suggestions were modified
- Suggestions were rejected if incorrect

The final implementation reflects developer-reviewed and tested code.

---

# Testing Strategy

The project combines:

## Automated Testing

Pytest verifies:

- Sudoku generation
- Difficulty generation
- Hint API
- Check API
- Backend validation
- Board validation
- Invalid request handling

Current Status

```
16 Tests Passed
```

---

## Manual Testing

The following features were manually verified:

- Gameplay
- Hint correctness
- Leaderboard
- Timer
- Responsive layout
- Dark mode
- Local Storage persistence

---

# Screenshots

The repository contains screenshots demonstrating:

- GitHub Copilot prompts
- GitHub Copilot responses
- Refactoring process
- Feature implementation
- Automated testing
- Running application
- Leaderboard
- Hint functionality
- Puzzle completion

---

# Documentation

Additional implementation details are available in:

```
starter/instruction.md
```

---

# Learning Outcomes

This project demonstrates practical experience with:

- Flask web development
- Python programming
- Frontend integration
- Automated testing using Pytest
- Git version control
- GitHub workflow
- AI-assisted software development using GitHub Copilot
- Code refactoring
- Prompt engineering
- Software debugging

---

# Future Enhancements

Potential future improvements include:

- User authentication
- Online leaderboard
- Multiple Sudoku board sizes
- Save and resume games
- Sound effects
- Keyboard shortcuts
- Theme customization
- Accessibility improvements

---

# Conclusion

The original Sudoku application has been successfully transformed into a feature-rich, responsive, and well-tested web application. GitHub Copilot played an important role throughout development by assisting with refactoring, feature implementation, testing, debugging, and documentation. Every AI-generated suggestion was carefully reviewed and validated, resulting in a reliable, maintainable, and user-friendly Sudoku application.