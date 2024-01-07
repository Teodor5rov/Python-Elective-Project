# Tic-Tac-Toe and Minesweeper Game Library

## Introduction
Welcome to our Tic-Tac-Toe and Minesweeper Game Library! This repository houses two classic games enhanced with AI/Bot features. These games are designed to offer an engaging and challenging experience for players of all skill levels. The library's starter class serves as the entry point, allowing players to choose their preferred game.

## Features
- **Two Classic Games**: Play either Tic-Tac-Toe or Minesweeper.
- **Difficulty Levels**: Choose your challenge level in both games.
- **Interactive Game Boards**: Enjoy a user-friendly interface.
- **AI/Bot Integration**: Compete against an AI in Tic-Tac-Toe or receive AI assistance in Minesweeper.

## Getting Started
To begin, run the starter class from the PyCharm app. This will present a menu where you can choose between Tic-Tac-Toe and Minesweeper.

### Tic-Tac-Toe
Upon selecting Tic-Tac-Toe, you'll be prompted to choose a difficulty level: Easy, Medium, Hard, or Impossible. The default settings place you as 'X', with the option to switch to 'O'. Gameplay begins by clicking the "Start game" button. Use your mouse to interact with the board.

#### Features
- **Settings**: Adjust difficulty or switch your marker.
- **Reset**: Clears the board for a new game.
- **Menu**: Return to the main starter menu.
- **AI Strategy**: The Tic-Tac-Toe bot uses the Minimax algorithm, adjusting its skill level based on the chosen difficulty.

### Minesweeper
Selecting Minesweeper brings up a menu detailing game rules and difficulty settings: Easy, Medium, or Hard. The playing field changes accordingly, with varying numbers of mines.

#### Features
- **Settings**: Return to adjust difficulty.
- **Menu**: Navigate back to the starter menu.
- **AI Helper**: An AI that helps you make moves, especially when the next step is uncertain.
- **Adaptive Gameplay**: The AI updates its strategy based on the current state of the board, using logical inference to avoid mines.

## AI Implementation
- **Tic-Tac-Toe Bot**: Utilizes the Minimax algorithm. For varying difficulties, the bot may make suboptimal moves to provide a balanced challenge.
- **Minesweeper AI**: Analyzes the board, applying logical inference to guide the player, with occasional random moves in uncertain situations.
