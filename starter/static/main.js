// Client-side rendering and interaction for the Flask-backed Sudoku
const SIZE = 9;
const THEME_STORAGE_KEY = 'sudoku-theme';
const LEADERBOARD_STORAGE_KEY = 'sudoku-leaderboard';
let puzzle = [];
let timerInterval = null;
let elapsedSeconds = 0;
let hintsUsed = 0;
let hasCompletedGame = false;

function applyTheme(theme) {
  document.documentElement.dataset.theme = theme;
  localStorage.setItem(THEME_STORAGE_KEY, theme);

  const themeToggle = document.getElementById('theme-toggle');
  if (themeToggle) {
    themeToggle.textContent = theme === 'dark' ? 'Light mode' : 'Dark mode';
    themeToggle.setAttribute('aria-pressed', String(theme === 'dark'));
  }
}

function initializeTheme() {
  const savedTheme = localStorage.getItem(THEME_STORAGE_KEY);
  const preferredTheme = savedTheme || 'light';
  applyTheme(preferredTheme);
}

function normalizeLeaderboardEntry(entry) {
  if (!entry || typeof entry !== 'object') {
    return null;
  }

  return {
    playerName: entry.playerName || entry.name || 'Player',
    difficulty: entry.difficulty || entry.level || 'medium',
    completionSeconds: Number(entry.completionSeconds ?? entry.time ?? 0),
    hintsUsed: Number(entry.hintsUsed ?? entry.hints ?? 0),
  };
}

function getLeaderboardEntries() {
  try {
    const rawEntries = localStorage.getItem(LEADERBOARD_STORAGE_KEY);
    if (!rawEntries) {
      return [];
    }

    const parsedEntries = JSON.parse(rawEntries);
    if (!Array.isArray(parsedEntries)) {
      return [];
    }

    const normalizedEntries = parsedEntries
      .map(normalizeLeaderboardEntry)
      .filter(Boolean);

    if (normalizedEntries.length !== parsedEntries.length) {
      saveLeaderboardEntries(normalizedEntries);
    }

    return normalizedEntries;
  } catch (error) {
    return [];
  }
}

function saveLeaderboardEntries(entries) {
  localStorage.setItem(LEADERBOARD_STORAGE_KEY, JSON.stringify(entries));
}

function escapeHtml(text) {
  return String(text)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function formatTimerDisplay() {
  const minutes = String(Math.floor(elapsedSeconds / 60)).padStart(2, '0');
  const seconds = String(elapsedSeconds % 60).padStart(2, '0');
  return `${minutes}:${seconds}`;
}

function updateTimerDisplay() {
  const timerElement = document.getElementById('timer');
  timerElement.textContent = `Time: ${formatTimerDisplay()}`;
}

function renderLeaderboard() {
  const leaderboardBody = document.getElementById('leaderboard-body');
  if (!leaderboardBody) {
    return;
  }

  const entries = getLeaderboardEntries()
    .sort((a, b) => {
      if (a.completionSeconds !== b.completionSeconds) {
        return a.completionSeconds - b.completionSeconds;
      }
      return a.hintsUsed - b.hintsUsed;
    })
    .slice(0, 10);

  leaderboardBody.innerHTML = '';

  if (entries.length === 0) {
    const emptyRow = document.createElement('tr');
    const emptyCell = document.createElement('td');
    emptyCell.colSpan = 5;
    emptyCell.textContent = 'No completed games yet.';
    emptyRow.appendChild(emptyCell);
    leaderboardBody.appendChild(emptyRow);
    return;
  }

  entries.forEach((entry, index) => {
    const row = document.createElement('tr');
    const rankCell = document.createElement('td');
    const nameCell = document.createElement('td');
    const timeCell = document.createElement('td');
    const levelCell = document.createElement('td');
    const hintsCell = document.createElement('td');

    rankCell.textContent = String(index + 1);
    nameCell.textContent = entry.playerName || 'Player';
    timeCell.textContent = formatTimerDisplayForEntry(entry.completionSeconds);
    levelCell.textContent = entry.difficulty;
    hintsCell.textContent = String(entry.hintsUsed);

    row.appendChild(rankCell);
    row.appendChild(nameCell);
    row.appendChild(timeCell);
    row.appendChild(levelCell);
    row.appendChild(hintsCell);

    leaderboardBody.appendChild(row);
  });
}

function formatTimerDisplayForEntry(seconds) {
  const minutes = String(Math.floor(seconds / 60)).padStart(2, '0');
  const secondsPart = String(seconds % 60).padStart(2, '0');
  return `${minutes}:${secondsPart}`;
}

function recordLeaderboardEntry() {
  if (hasCompletedGame) {
    return;
  }

  const playerNameInput = document.getElementById('player-name');
  const difficultySelect = document.getElementById('difficulty-select');
  const playerName = (playerNameInput.value || 'Player').trim() || 'Player';
  const difficulty = difficultySelect.value;
  const completionSeconds = elapsedSeconds;

  const entries = getLeaderboardEntries();
  entries.push({
    playerName,
    difficulty,
    completionSeconds,
    hintsUsed,
  });

  const sortedEntries = entries
    .sort((a, b) => {
      if (a.completionSeconds !== b.completionSeconds) {
        return a.completionSeconds - b.completionSeconds;
      }
      return a.hintsUsed - b.hintsUsed;
    })
    .slice(0, 10);

  saveLeaderboardEntries(sortedEntries);
  renderLeaderboard();
  hasCompletedGame = true;
}

function startTimer() {
  if (timerInterval !== null) {
    clearInterval(timerInterval);
  }

  elapsedSeconds = 0;
  updateTimerDisplay();
  timerInterval = setInterval(() => {
    elapsedSeconds += 1;
    updateTimerDisplay();
  }, 1000);
}

function stopTimer() {
  if (timerInterval !== null) {
    clearInterval(timerInterval);
    timerInterval = null;
  }
}

function resetGameState() {
  hintsUsed = 0;
  hasCompletedGame = false;
}

function createBoardElement() {
  const boardDiv = document.getElementById('sudoku-board');
  boardDiv.innerHTML = '';
  for (let i = 0; i < SIZE; i++) {
    const rowDiv = document.createElement('div');
    rowDiv.className = 'sudoku-row';
    for (let j = 0; j < SIZE; j++) {
      const input = document.createElement('input');
      const boxParity = ((Math.floor(i / 3) + Math.floor(j / 3)) % 2 === 0) ? 'box-even' : 'box-odd';
      input.type = 'text';
      input.maxLength = 1;
      input.className = `sudoku-cell ${boxParity}`;
      input.dataset.row = i;
      input.dataset.col = j;
      input.dataset.boxParity = boxParity;
      input.addEventListener('input', async (e) => {
        const val = e.target.value.replace(/[^1-9]/g, '');
        e.target.value = val;
        await checkSolution({silent: true});
        maybeAutoCompletePuzzle();
      });
      rowDiv.appendChild(input);
    }
    boardDiv.appendChild(rowDiv);
  }
}

function isHighlightableCell(input) {
  const rawValue = input.value;
  return !input.disabled
    && rawValue !== ''
    && rawValue !== null
    && rawValue !== undefined
    && rawValue !== 0
    && rawValue !== '0';
}

function applyBoardHighlightState(inputs, incorrect, correct) {
  for (let idx = 0; idx < inputs.length; idx++) {
    const input = inputs[idx];
    input.classList.remove('incorrect', 'correct', 'live-invalid');

    const existingClasses = Array.from(input.classList).filter((className) => {
      return className !== 'incorrect' && className !== 'correct' && className !== 'live-invalid';
    });

    input.className = `sudoku-cell ${input.dataset.boxParity}`;

    if (existingClasses.includes('prefilled')) {
      input.classList.add('prefilled');
    }

    if (existingClasses.includes('hinted')) {
      input.classList.add('hinted');
    }

    if (!isHighlightableCell(input)) {
      continue;
    }

    if (incorrect.has(idx)) {
      input.classList.add('incorrect');
    } else if (correct.has(idx)) {
      input.classList.add('correct');
    }
  }
}

function renderPuzzle(puz) {
  puzzle = puz;
  createBoardElement();
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  for (let i = 0; i < SIZE; i++) {
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = puzzle[i][j];
      const inp = inputs[idx];
      if (val !== 0) {
        inp.value = val;
        inp.disabled = true;
        inp.className = `sudoku-cell ${inp.dataset.boxParity} prefilled`;
      } else {
        inp.value = '';
        inp.disabled = false;
        inp.className = `sudoku-cell ${inp.dataset.boxParity}`;
      }
    }
  }
}

function getBoard() {
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  const board = [];

  for (let i = 0; i < SIZE; i++) {
    board[i] = [];
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = inputs[idx].value;
      board[i][j] = val ? parseInt(val, 10) : 0;
    }
  }

  return board;
}

function hasEmptyEditableCells() {
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');

  for (let index = 0; index < inputs.length; index++) {
    const input = inputs[index];
    if (input.disabled) {
      continue;
    }

    if (!input.value) {
      return true;
    }
  }

  return false;
}

async function maybeAutoCompletePuzzle() {
  if (hasCompletedGame || hasEmptyEditableCells()) {
    return;
  }

  await checkSolution({silent: true});
}

function applyHint(row, col, value) {
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  const idx = row * SIZE + col;
  const inp = inputs[idx];

  if (!inp) {
    return;
  }

  inp.value = value;
  inp.disabled = true;
  inp.className = `sudoku-cell ${inp.dataset.boxParity} hinted`;
  puzzle[row][col] = value;
  maybeAutoCompletePuzzle();
}

async function newGame() {
  const difficultySelect = document.getElementById('difficulty-select');
  const difficulty = difficultySelect.value;
  const res = await fetch(`/new?difficulty=${encodeURIComponent(difficulty)}`);
  const data = await res.json();
  renderPuzzle(data.puzzle);
  resetGameState();
  startTimer();
  document.getElementById('message').innerText = '';
}

async function checkSolution(options = {}) {
  const {silent = false} = options;
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  const board = getBoard();
  const res = await fetch('/check', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({board})
  });
  const data = await res.json();
  const msg = document.getElementById('message');
  if (data.error) {
    msg.style.color = '#d32f2f';
    if (!silent) {
      msg.innerText = data.error;
    }
    return;
  }

  const incorrect = new Set(data.incorrect.map(x => x[0] * SIZE + x[1]));
  const correct = new Set(data.correct.map(x => x[0] * SIZE + x[1]));

  applyBoardHighlightState(inputs, incorrect, correct);

  if (incorrect.size === 0) {
    stopTimer();
    recordLeaderboardEntry();
    for (let idx = 0; idx < inputs.length; idx++) {
      const inp = inputs[idx];
      inp.disabled = true;
    }
    msg.style.color = '#388e3c';
    msg.innerText = '🎉 Congratulations! You solved the puzzle!';
  } else if (!silent) {
    msg.style.color = '#d32f2f';
    msg.innerText = 'Some cells are incorrect.';
  }
}

async function getHint() {
  const board = getBoard();

  const res = await fetch('/hint', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({board})
  });
  const data = await res.json();
  if (data.error) {
    const msg = document.getElementById('message');
    msg.style.color = '#d32f2f';
    msg.innerText = data.error;
    return;
  }

  hintsUsed += 1;
  applyHint(data.row, data.col, data.value);
  const msg = document.getElementById('message');
  msg.style.color = '#388e3c';
  msg.innerText = 'Hint used.';
}

// Wire buttons
window.addEventListener('load', () => {
  initializeTheme();
  renderLeaderboard();

  document.getElementById('new-game').addEventListener('click', newGame);
  document.getElementById('check-solution').addEventListener('click', checkSolution);
  document.getElementById('hint-button').addEventListener('click', getHint);
  document.getElementById('theme-toggle').addEventListener('click', () => {
    const nextTheme = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
    applyTheme(nextTheme);
  });

  // initialize
  newGame();
});