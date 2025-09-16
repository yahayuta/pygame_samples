# 🎮 Pygame Samples

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Pygame](https://img.shields.io/badge/Pygame-2.0+-green.svg)](https://www.pygame.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)](https://github.com/yourusername/pygame_samples)

A collection of **20 classic arcade games** built with [Pygame](https://www.pygame.org/). Perfect for learning game development and having fun! 🚀

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

- ✅ **20 Complete Games** - All fully playable
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
| 💧 **Puyo Puyo** | Puzzle | Arrow Keys | Match 4+ same-colored Puyos to clear them and trigger combos. |

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
pip install pygame numpy
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

### 🟡 Pac-Man
- **Objective**: Eat all dots while avoiding ghosts
- **Controls**: Arrow keys to move

### 🃏 Blackjack
- **Objective**: Beat dealer without going over 21
- **Controls**: `H` - Hit, `S` - Stay

### 🏓 Breakout
- **Objective**: Break all bricks with the ball
- **Controls**: Left/Right arrows to move paddle

### 🏎️ Car Race
- **Objective**: Avoid enemy cars as long as possible
- **Controls**: Left/Right arrows to change lanes

### 🐸 Frogger
- **Objective**: Cross the road to reach the top
- **Controls**: Arrow keys to move

### 🃏 Poker
- **Objective**: Get the best 5-card hand
- **Controls**: See in-game help

### 🏓 Pong
- **Objective**: Score by getting ball past computer
- **Controls**: Up/Down arrows to move right paddle

### ⚫ Reversi
- **Objective**: Capture opponent's pieces
- **Controls**: Mouse click to place piece

### ✂️ Rock Paper Scissors
- **Objective**: Beat the computer
- **Controls**: `R` - Rock, `P` - Paper, `S` - Scissors

### 🎰 Slot Machine
- **Objective**: Match symbols to win
- **Controls**: Mouse click to Spin

### 👾 Space Invaders
- **Objective**: Shoot all alien invaders
- **Controls**: Arrow keys to move, Spacebar to shoot

### 🧩 Tetris (Enhanced)
- **Objective**: Complete horizontal lines to clear them
- **Controls**: Arrow Keys, Space, H, P

### ❌ Tic Tac Toe
- **Objective**: Get 3 in a row
- **Controls**: Mouse click to place your mark

### 🚀 Torpedo Attack
- **Objective**: Sink enemy ships
- **Controls**: Any key to fire torpedo

### 🐍 Snake
- **Objective**: Eat food to grow longer
- **Controls**: Arrow keys to change direction

### 🚀 Asteroids
- **Objective**: Destroy all asteroids and survive
- **Controls**: Arrow keys to move, Space to shoot

### 🎯 Missile Command
- **Objective**: Defend your cities from incoming missiles
- **Controls**: Mouse/Arrow Keys + Space

### 💣 Minesweeper
- **Objective**: Find all the mines without detonating any of them.
- **Controls**: Left Click to reveal, Right Click to flag.

### ⛏️ Dig Dug
- **Objective**: Defeat all enemies by pumping them up or dropping rocks on them.
- **Controls**: Arrow Keys to move, Spacebar to pump.

### 💧 Puyo Puyo
- **Objective**: Match 4 or more same-colored Puyos to clear them from the board.
- **Controls**: Left/Right to move, Up to rotate, Down to drop faster.

## 📁 Project Structure

```
pygame_samples/
├── 🎮 Games (20 total)
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
│   ├── puyopuyo/
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