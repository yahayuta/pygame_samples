# 🎮 Pygame Samples

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Pygame](https://img.shields.io/badge/Pygame-2.0+-green.svg)](https://www.pygame.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)](https://github.com/yourusername/pygame_samples)

A collection of **14 classic arcade games** built with [Pygame](https://www.pygame.org/). Perfect for learning game development and having fun! 🚀

## 📋 Table of Contents

- [🎯 Features](#-features)
- [🎮 Games Included](#-games-included)
- [⚡ Quick Start](#-quick-start)
- [🔧 Installation](#-installation)
- [🎯 How to Play](#-how-to-play)
- [📁 Project Structure](#-project-structure)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

## 🎯 Features

- ✅ **14 Complete Games** - All fully playable
- 🎨 **Modern UI** - Clean, responsive interfaces
- 🔊 **Sound Effects** - Immersive audio experience
- 🎯 **Score Systems** - Track your progress
- 🎮 **Easy Controls** - Intuitive gameplay
- 🚀 **Fast Performance** - Smooth 60 FPS gameplay
- 📱 **Cross-Platform** - Works on Windows, macOS, Linux

## 🎮 Games Included

| Game | Type | Controls | Description |
|------|------|----------|-------------|
| 🟡 **Pac-Man** | Arcade | Arrow Keys | Eat dots, avoid ghosts |
| 🃏 **Blackjack** | Card | H/S Keys | Beat dealer to 21 |
| 🏓 **Breakout** | Arcade | Arrow Keys | Break bricks with ball |
| 🏎️ **Car Race** | Racing | Arrow Keys | Dodge enemy cars |
| 🐸 **Frogger** | Arcade | Arrow Keys | Cross road safely |
| 🃏 **Poker** | Card | Spacebar | Classic 5-card poker |
| 🏓 **Pong** | Arcade | W/S, Up/Down | Classic paddle game |
| ⚫ **Reversi** | Strategy | Mouse Click | Flip opponent's pieces |
| ✂️ **Rock Paper Scissors** | Casual | R/P/S Keys | Beat the computer |
| 🎰 **Slot Machine** | Casino | Mouse Click | Spin to win |
| 👾 **Space Invaders** | Arcade | Arrow Keys + Space | Shoot alien invaders |
| 🧩 **Tetris** | Puzzle | Arrow Keys | Stack falling blocks |
| ❌ **Tic Tac Toe** | Strategy | Mouse Click | Classic X's and O's |
| 🚀 **Torpedo Attack** | Arcade | Any Key | Sink enemy ships |

## ⚡ Quick Start

### Windows Users
```bash
# Double-click to launch all games
start_games.bat
```

### All Platforms
```bash
# Navigate to any game folder and run
cd pacman
python main.py
```

## 🔧 Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/pygame_samples.git
cd pygame_samples
```

### Step 2: Install Dependencies
```bash
pip install pygame
```

### Step 3: Run Games
```bash
# Use the launcher (Windows)
start_games.bat

# Or run individual games
python pacman/main.py
python tetris/main.py
python space_invaders/main.py
```

## 🎯 How to Play

### 🟡 Pac-Man
- **Objective**: Eat all dots while avoiding ghosts
- **Controls**: Arrow keys to move
- **Scoring**: Points for dots eaten
- **Game Over**: Touch a ghost

### 🃏 Blackjack
- **Objective**: Beat dealer without going over 21
- **Controls**: 
  - `H` - Hit (draw card)
  - `S` - Stay (end turn)
- **Scoring**: Closest to 21 wins

### 🏓 Breakout
- **Objective**: Break all bricks with the ball
- **Controls**: Left/Right arrows to move paddle
- **Scoring**: Points for bricks broken
- **Game Over**: Ball falls below paddle

### 🏎️ Car Race
- **Objective**: Avoid enemy cars as long as possible
- **Controls**: Left/Right arrows to change lanes
- **Scoring**: Distance traveled
- **Game Over**: Collision with enemy car

### 🐸 Frogger
- **Objective**: Cross the road to reach the top
- **Controls**: Arrow keys to move
- **Scoring**: Points for reaching top
- **Game Over**: Hit by enemy

### 🃏 Poker
- **Objective**: Get the best 5-card hand
- **Controls**: Spacebar to deal new hand
- **Scoring**: Hand rankings determine winner

### 🏓 Pong
- **Objective**: Score by getting ball past opponent
- **Controls**: 
  - Left player: `W`/`S`
  - Right player: `Up`/`Down`
- **Scoring**: Points when ball passes opponent

### ⚫ Reversi
- **Objective**: Capture opponent's pieces
- **Controls**: Mouse click to place piece
- **Scoring**: Most pieces at end wins

### ✂️ Rock Paper Scissors
- **Objective**: Beat the computer
- **Controls**: 
  - `R` - Rock
  - `P` - Paper  
  - `S` - Scissors
- **Scoring**: Win/Loss/Draw tracking

### 🎰 Slot Machine
- **Objective**: Match symbols to win
- **Controls**: Click spin button
- **Scoring**: Points for matching combinations

### 👾 Space Invaders
- **Objective**: Shoot all alien invaders
- **Controls**: 
  - Arrow keys to move
  - Spacebar to shoot
- **Scoring**: Points for each alien destroyed
- **Game Over**: Alien touches player

### 🧩 Tetris
- **Objective**: Complete horizontal lines
- **Controls**:
  - Left/Right arrows to move
  - Up arrow to rotate
  - Down arrow to drop faster
- **Scoring**: Points for completed lines

### ❌ Tic Tac Toe
- **Objective**: Get 3 in a row
- **Controls**: Mouse click to place X or O
- **Scoring**: Win/Loss/Draw

### 🚀 Torpedo Attack
- **Objective**: Sink enemy ships
- **Controls**: Any key to fire torpedo
- **Scoring**: Points for each ship sunk

## 📁 Project Structure

```
pygame_samples/
├── 🎮 Games
│   ├── pacman/           # Pac-Man clone
│   ├── blackjack/        # Blackjack card game
│   ├── breakout/         # Breakout brick breaker
│   ├── car_race/         # Car racing game
│   ├── frogger/          # Frogger arcade game
│   ├── poker/            # Poker card game
│   ├── pong/             # Pong paddle game
│   ├── reversi/          # Reversi strategy game
│   ├── rock_paper_scissors/  # Rock Paper Scissors
│   ├── slot_machine/     # Slot machine game
│   ├── space_invaders/   # Space Invaders shooter
│   ├── tetris/           # Tetris puzzle game
│   ├── tictactoe/        # Tic Tac Toe
│   └── torpedo_attack/   # Torpedo Attack shooter
├── 🎵 Assets
│   ├── cards/            # Card images
│   ├── sound_files/      # Audio effects
│   └── image_files/      # Game graphics
├── 🚀 Launchers
│   └── start_games.bat   # Windows game launcher
└── 📄 Documentation
    ├── README.md         # This file
    └── .gitignore        # Git ignore rules
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### 🐛 Reporting Bugs
1. Check if the bug has already been reported
2. Create a new issue with:
   - Clear description of the problem
   - Steps to reproduce
   - Expected vs actual behavior

### 💡 Suggesting Features
1. Open an issue with the "enhancement" label
2. Describe the feature and its benefits
3. Include mockups if applicable

### 🔧 Submitting Code
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### 📋 Code Style
- Follow PEP 8 Python style guide
- Add comments for complex logic
- Include docstrings for functions
- Test your changes before submitting

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Pygame Community** - For the amazing game development library
- **Open Source Contributors** - For inspiration and code examples
- **Game Asset Creators** - For the graphics and sounds

---

<div align="center">

**Made with ❤️ and 🐍 Python**

[⭐ Star this repo](https://github.com/yourusername/pygame_samples) | [🐛 Report a bug](https://github.com/yourusername/pygame_samples/issues) | [💡 Request a feature](https://github.com/yourusername/pygame_samples/issues)

</div>
