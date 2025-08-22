# 🎮 Pygame Samples

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Pygame](https://img.shields.io/badge/Pygame-2.0+-green.svg)](https://www.pygame.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)](https://github.com/yourusername/pygame_samples)

A collection of **19 classic arcade games** built with [Pygame](https://www.pygame.org/). Perfect for learning game development and having fun! 🚀

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

- ✅ **19 Complete Games** - All fully playable
- 🎨 **Modern UI** - Clean, responsive interfaces
- 💵 **Casino-Style Betting in Blackjack** - Chip-based betting, bankroll management, and polished casino look
- 🔊 **Sound Effects** - Immersive audio experience
- 🎯 **Score Systems** - Track your progress
- 🎮 **Easy Controls** - Intuitive gameplay
- 🚀 **Fast Performance** - Smooth 60 FPS gameplay
- 📱 **Cross-Platform** - Works on Windows, macOS, Linux
- 📖 **On-Screen Instructions** - Learn to play instantly
- 🎯 **Enhanced Gameplay** - Improved mechanics and variety
- 🤖 **AI Opponents** - Computer-controlled opponents
- 🎵 **Generated Audio** - Programmatically created sound effects
- 🧩 **Enhanced Tetris** - Modern Tetris with ghost piece, hold, wall kicks, and advanced scoring
- 🧩 **Tetris UI Optimized** - Compact layout, no side panel overlap, and correct brick stacking

## 🎮 Games Included

| Game | Type | Controls | Description |
|------|------|----------|-------------|
| 🟡 **Pac-Man** | Arcade | Arrow Keys | Eat dots, avoid ghosts |
| 🃏 **Blackjack** | Card | H/S Keys | Beat dealer to 21 |
| 🏓 **Breakout** | Arcade | Arrow Keys | Break bricks with ball |
| 🏎️ **Car Race** | Racing | Arrow Keys | Dodge enemy cars |
| 🐸 **Frogger** | Arcade | Arrow Keys | Cross road safely, collect power-ups, and progress through levels |
| 🃏 **Poker** | Card | Spacebar | Classic 5-card poker |
| 🏓 **Pong** | Arcade | Up/Down | Player vs Computer |
| ⚫ **Reversi** | Strategy | Mouse Click | Flip opponent's pieces |
| ✂️ **Rock Paper Scissors** | Casual | R/P/S Keys | Beat the computer |
| 🎰 **Slot Machine** | Casino | Mouse Click | Spin to win |
| 👾 **Space Invaders** | Arcade | Arrow Keys + Space | Shoot alien invaders |
| 🧩 **Tetris (Enhanced)** | Puzzle | Arrow Keys + Space + H + P | Modern Tetris with ghost piece, hold, wall kicks |
| ❌ **Tic Tac Toe** | Strategy | Mouse Click | Classic X's and O's |
| 🚀 **Torpedo Attack** | Arcade | Any Key | Sink enemy ships |
| 🐍 **Snake** | Arcade | Arrow Keys | Eat food to grow longer |
| 🚀 **Asteroids** | Arcade | Arrow Keys + Space | Destroy asteroids, avoid collisions |
| 🎯 **Missile Command** | Arcade | Mouse/Arrow Keys + Space | Defend cities from incoming missiles |
| 💣 **Minesweeper** | Puzzle | Mouse Click | Find all the mines without detonating any of them. |
| ⛏️ **Dig Dug** | Arcade | Arrow Keys + Space | Dig tunnels, defeat enemies with an air pump, and drop rocks. |

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

### Step 3: Generate Sound Files (Optional)
```bash
# Generate all sound effects
python generate_sounds.py
```

### Step 4: Run Games
```bash
# Use the launcher (Windows)
start_games.bat

# Or run individual games
python pacman/main.py
python tetris/main.py
```

## 🎯 How to Play

(Includes all previous game instructions, plus...)

### 💣 Minesweeper
- **Objective**: Find all the mines without detonating any of them.
- **Controls**:
  - **Left Click**: Reveal a tile.
  - **Right Click**: Flag a tile.
- **Game Over**: Click on a mine.

### ⛏️ Dig Dug
- **Objective**: Defeat all enemies by pumping them up or dropping rocks on them.
- **Controls**:
  - **Arrow Keys**: Move and dig.
  - **Spacebar**: Fire harpoon and pump enemies.
- **Game Over**: Collide with an enemy or get crushed by a rock.

## 📁 Project Structure

```
pygame_samples/
├── 🎮 Games (19 total)
│   ├── asteroids/
│   ├── blackjack/
│   ├── breakout/
│   ├── car_race/
│   ├── digdug/
│   ├── frogger/
│   ├── missile_command/
│   ├── minesweeper/
│   ├── pacman/
│   ├── poker/
│   ├── pong/
│   ├── reversi/
│   ├── rock_paper_scissors/
│   ├── slot_machine/
│   ├── snake/
│   ├── space_invaders/
│   ├── tetris/
│   ├── tictactoe/
│   └── torpedo_attack/
├── 🎵 Assets
│   └── sound_files/
├── 🚀 Launchers
│   └── start_games.bat
├── 🛠️ Tools
│   └── generate_sounds.py
└── 📄 Documentation
    ├── README.md
    ├── LICENSE
    ├── .gitignore
    └── .gitattributes
```