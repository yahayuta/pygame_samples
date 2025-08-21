# 🎮 Pygame Samples

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Pygame](https://img.shields.io/badge/Pygame-2.0+-green.svg)](https://www.pygame.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)](https://github.com/yourusername/pygame_samples)

A collection of **17 classic arcade games** built with [Pygame](https://www.pygame.org/). Perfect for learning game development and having fun! 🚀

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

- ✅ **17 Complete Games** - All fully playable
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

# Or try the new Snake game
cd snake
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
python space_invaders/main.py
python snake/main.py
```

## 🎯 How to Play

### 🟡 Pac-Man
- **Objective**: Eat all dots while avoiding ghosts
- **Controls**: Arrow keys to move
- **Scoring**: Dots = 10, Power Pellets = 50, Ghosts = 200
- **Game Over**: Touch a ghost
- **Features**:
  - Simpler, open maze for easier navigation
  - Power pellets in the corners
  - Ghost AI personalities
  - Improved respawn logic: Pac-Man and ghosts always respawn inside the maze, never on a wall or outside

### 🃏 Blackjack
- **Objective**: Beat dealer without going over 21
- **Controls**: 
  - `H` - Hit (draw card)
  - `S` - Stay (end turn)
  - Mouse: Click chips to bet, click buttons to play
- **Scoring**: Closest to 21 wins
- **Features**:
  - Modern, casino-style UI with clear layout and no overlaps
  - **Chip-based betting system**: Click chips to place your bet before each hand
  - **Bankroll management**: Start with $1000, win or lose based on your bets
  - **Dynamic status messages**: See your bet, bankroll, and results after each hand
  - **Responsive buttons**: HIT, STAND, DEAL, and NEW GAME
  - Keyboard and mouse support for all actions
  - Clean separation of dealer/player areas and status

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
- **Features**:
  - Cross road safely, collect power-ups, and progress through levels

### 🃏 Poker
- **Objective**: Get the best 5-card hand and win all the chips!
- **Rules**: Follows standard casino Five Card Draw rules
- **Players**: 1 human vs up to 3 AI (multi-player support)
- **Ante**: All players ante 10 chips at the start of each hand
- **Betting**: Minimum bet 10 chips, maximum bet 100 chips per round
- **Dealer**: Dealer button alternates each hand; non-dealer acts first pre-draw, dealer acts first post-draw
- **Controls**:
  - 1-9,0: Set bet/raise amount (10-100 chips)
  - B: Bet   C: Call   R: Raise   F: Fold
  - 1-5: Select cards to discard   D: Draw
  - H: Show/hide help overlay
  - S: Show/hide stats/leaderboard
  - M: Mute/unmute sound
  - SPACE: Continue after showdown or game over
- **Features**:
  - Sound effects for dealing, betting, calling, raising, folding, drawing, winning, losing, and game over
  - Mute toggle (M key)
  - Variable betting and raising amounts
  - Modern, always-visible in-game UI (chips, pot, bet amount, phase, dealer)
  - Stats/leaderboard overlay (track wins, streaks, biggest pot, etc.)
  - On-screen help overlay (rules, controls, hand rankings)
  - Smarter computer AI for betting and discarding
  - Enhanced hand descriptions (e.g., "Pair of Aces", "Full House: Jacks over Sevens")
  - Clear winner/loser and chip count display at showdown and game over

### 🏓 Pong
- **Objective**: Score by getting ball past computer
- **Controls**: Up/Down arrows to move right paddle
- **Scoring**: Points when ball passes opponent
- **AI**: Computer-controlled left paddle with smart tracking

### ⚫ Reversi
- **Objective**: Capture opponent's pieces
- **Controls**: Mouse click to place piece
- **Scoring**: Most pieces at end wins
- **Features**:
  - Modern UI: gradient board, anti-aliased grid, 3D discs with shadows/highlights
  - Valid move highlighting for current player
  - Animated piece flipping (smooth color morph)
  - Modern rounded score/status panel with clear font

### ✂️ Rock Paper Scissors
- **Objective**: Beat the computer
- **Controls**: 
  - `R` - Rock
  - `P` - Paper  
  - `S` - Scissors
- **Scoring**: Win/Loss/Draw tracking with color-coded results
- **Features**:
  - **Enhanced Visual Design** - Color-coded results (Green for wins, Red for losses, Gold for draws)
  - **Improved UI Layout** - Professional boxes and backgrounds for better organization
  - **Clear Result Display** - Prominent "RESULT" header with organized choice display
  - **Better Game Flow** - Results stay visible until you press any key to continue
  - **Score Tracking** - Color-coded win/loss/draw counters with background
  - **Modern Typography** - Multiple font sizes for better visual hierarchy
  - **Responsive Design** - Clean, organized layout with proper spacing

### 🎰 Slot Machine
- **Objective**: Match symbols to win
- **Controls**:
  - Mouse click: Spin
  - `P`: Show/hide prize list (paytable)
- **Features**:
  - Modern, visually appealing slot machine UI with gold frame, lever, and glass reflection
  - Result message is shown above the machine after each spin, never overlapping the reels
  - **Prize List Board (Paytable)**: Press `P` to view all winning combinations and their payouts, including symbol images and special features
  - **Prizes:**
    - Three Sevens: JACKPOT (progressive)
    - Three Cherries: 50x bet + 10 Free Spins
    - Three Bells: 10x bet + Bonus Round
    - Three Plums, Watermelons, etc.: Standard payouts
    - Two/One Sevens, Cherries, etc.: Smaller payouts
  - **Special Features:**
    - Progressive jackpot
    - Free spins
    - Bonus rounds with multipliers
    - Win animations and sound effects
  - Clean, centered layout with no UI overlaps
  - Bet controls, auto play, and statistics

### 👾 Space Invaders
- **Objective**: Shoot all alien invaders
- **Controls**: 
  - Arrow keys to move
  - Spacebar to shoot
- **Scoring**: Points for each alien destroyed
- **Game Over**: Alien touches player

### 🧩 Tetris (Enhanced)
- **Objective**: Complete horizontal lines to clear them and score points
- **Controls**:
  - **Arrow Keys**: Move pieces left/right, rotate (up), soft drop (down)
  - **Spacebar**: Hard drop (instant drop)
  - **H**: Hold piece (store for later use)
  - **P**: Pause/Resume game
- **Scoring System**:
  - **1 line**: 100 × level
  - **2 lines**: 300 × level  
  - **3 lines**: 500 × level
  - **4 lines**: 800 × level
  - **Combo bonus**: 50 points per consecutive line clear
  - **Hard drop**: 2 points per cell dropped
- **Features**:
  - **Ghost piece**: Shows where piece will land
  - **Hold piece**: Store one piece for later use (once per piece)
  - **Next piece preview**: See upcoming piece
  - **Wall kicks**: Advanced rotation system
  - **Level progression**: Speed increases every 10 lines
  - **High score tracking**: Persistent high scores
  - **Modern UI**: Dark theme with compact side panel (no overlap)
  - **Game states**: Menu, pause, game over screens
  - **Enhanced graphics**: Grid lines, piece borders, better colors
  - **Bugfix**: Bricks now stack all the way to the bottom row

### ❌ Tic Tac Toe
- **Objective**: Get 3 in a row (X's and O's)
- **Controls**: Mouse click to place your mark
- **Game Modes**: 
  - Human vs Human
  - Human vs Computer (AI uses minimax algorithm)
- **Scoring**: Persistent scoreboard tracking wins for X, O, and ties
- **Features**:
  - **Smart AI**: Computer uses minimax algorithm for optimal play
  - **Visual Feedback**: Hover effects, winning line highlighting in gold
  - **Sound Effects**: Hit sound for moves, end sound for game completion
  - **Score Tracking**: Persistent scoreboard showing X wins, O wins, and ties
  - **Restart Button**: Easy game reset without closing
  - **Message Boxes**: Clear win/tie announcements with overlay
  - **Modern UI**: Clean interface with rounded buttons and professional styling

### 🚀 Torpedo Attack
- **Objective**: Sink enemy ships
- **Controls**: Any key to fire torpedo
- **Scoring**: Points for each ship sunk
- **Audio**: Fire and hit sound effects

### 🐍 Snake
- **Objective**: Eat food to grow longer
- **Controls**: Arrow keys to change direction
- **Scoring**: Points for each food eaten
- **Game Over**: Hit yourself or walls
- **Features**: Visible walls with collision detection, speed increases with score

### 🚀 Asteroids
- **Objective**: Destroy all asteroids and survive as long as possible
- **Controls**:
  - Arrow keys: Rotate and thrust
  - Spacebar: Shoot
- **Scoring**: Points for each asteroid destroyed
- **Game Over**: Ship destroyed with no lives left
- **Features**:
  - Rotating, jagged asteroids with rocky textures
  - Parallax, twinkling starfield background
  - Particle effects for thrust, explosions, and asteroid fragments
  - Ship trail and animated flame
  - Glowing shield on respawn
  - Score popups, screen shake, and flash feedback
  - Glow effects for ship, bullets, and asteroids
  - Modernized retro visuals and sound effects

### 🎯 Missile Command
- **Objective**: Defend your cities from incoming missiles by launching counter-missiles
- **Controls**:
  - **Mouse**: Move crosshair and left-click to fire
  - **Arrow Keys**: Move crosshair
  - **Spacebar**: Fire missile
  - **1, 2, 3**: Select missile base
  - **R**: Restart game
  - **Q**: Quit game
- **Scoring**: 100 points per enemy missile destroyed
- **Game Over**: All cities destroyed
- **Features**:
  - **Three Missile Bases**: Left, center, and right with unlimited ammo
  - **Multiple Levels**: Progressive difficulty with faster missiles and more frequent spawns
  - **Power-ups**: Big explosions, slow motion, and extra city protection
  - **Sound Effects**: Launch, explosion, city destruction, and game over sounds
  - **High Score System**: Persistent high score tracking
  - **Enhanced Graphics**: Background stars, detailed city sprites, animated explosions
  - **Main Menu**: Professional menu with instructions screen
  - **Easy Mode**: Very slow enemy missiles for beginner-friendly gameplay
  - **Visual Feedback**: Crosshair, base selection, power-up indicators
  - **Retro Style**: Authentic Atari 2600 era aesthetics with modern polish

## 📁 Project Structure

```
pygame_samples/
├── 🎮 Games (18 total)
│   ├── asteroids/           # Asteroids arcade game
│   ├── blackjack/          # Blackjack card game  
│   ├── breakout/           # Breakout brick breaker
│   ├── car_race/           # Car racing game
│   ├── frogger/            # Frogger arcade game
│   ├── missile_command/    # Missile Command arcade game
│   ├── minesweeper/        # Minesweeper puzzle game
│   ├── pacman/             # Pac-Man clone
│   ├── poker/              # Poker card game
│   ├── pong/               # Pong vs Computer
│   ├── reversi/            # Reversi strategy game
│   ├── rock_paper_scissors/ # Rock Paper Scissors
│   ├── slot_machine/       # Slot machine game
│   ├── snake/              # Snake arcade game
│   ├── space_invaders/     # Space Invaders shooter
│   ├── tetris/             # Tetris puzzle game
│   ├── tictactoe/          # Tic Tac Toe (enhanced)
│   └── torpedo_attack/     # Torpedo Attack shooter
├── 🎵 Assets
│   └── sound_files/        # Root level sound files (for breakout)
├── 🚀 Launchers
│   └── start_games.bat     # Windows game launcher
├── 🛠️ Tools
│   └── generate_sounds.py  # Sound file generator
└── 📄 Documentation
    ├── README.md           # Project documentation
    ├── LICENSE             # MIT License
    ├── .gitignore          # Git ignore rules
    └── .gitattributes     # Git attributes
```

**Each game directory contains:**
- `main.py` - Main game file
- `sound_files/` - Game-specific audio effects
- `images/` or `cards/` or `image_files/` - Game assets
- `*_high_score.*` - Score tracking files (where applicable)

## 🆕 Recent Updates

### 🧹 **Project Cleanup & Organization - Major Restructure!**
- **Removed Duplicate Files**: Eliminated redundant nested directories and duplicate sound files
- **Cleaned Cache Files**: Removed all `__pycache__` directories and `.pyc` files
- **Organized File Structure**: Each game now has its own clean directory with proper assets
- **Removed Empty Directories**: Cleaned up unused `sounds/` and `docs/` directories
- **Improved Project Size**: Reduced repository size by removing duplicate files
- **Better Maintainability**: Clear, consistent file organization across all games
- **Enhanced Navigation**: Logical file placement for easier development

### 🟡 **Enhanced Pac-Man - Major Upgrade!**
- **Classic Maze Layout** - Authentic Pac-Man maze with walls and corridors
- **Power Pellets** - Make ghosts vulnerable for 10 seconds
- **Ghost AI Personalities** - Different behaviors: chase, scatter, frightened
- **Multiple Lives** - 3 lives with respawn system
- **Comprehensive Scoring** - Dots (10), Power Pellets (50), Ghosts (200)
- **Sound Effects** - Eat, power pellet, ghost eaten, and death sounds
- **Smooth Movement** - Grid-based movement with direction buffering
- **Visual Feedback** - Pac-Man mouth animation, ghost color changes

### 🐍 **Snake Game - Latest Addition!**
- **Classic Arcade Gameplay** - Eat food to grow longer
- **Visible Walls** - Gray walls with collision detection
- **Progressive Difficulty** - Speed increases with score
- **Sound Effects** - Eat and game over audio feedback
- **On-Screen Instructions** - Learn to play instantly
- **Smooth Controls** - Responsive arrow key movement
- **Score Tracking** - Points for each food eaten
- **Restart Functionality** - Press SPACE to restart

### ✂️ **Enhanced Rock Paper Scissors - Major UI Upgrade!**
- **Color-Coded Results** - Green for wins, Red for losses, Gold for draws
- **Professional UI Design** - Modern boxes and backgrounds for better organization
- **Improved Game Flow** - Results stay visible until you press any key to continue
- **Enhanced Typography** - Multiple font sizes with better visual hierarchy
- **Better Score Display** - Color-coded counters with background boxes
- **Clear Result Layout** - Prominent "RESULT" header with organized choice display

### ❌ **Enhanced Tic Tac Toe - Major Upgrade!**
- **Smart AI**: Computer opponent uses minimax algorithm for optimal play
- **Dual Game Modes**: Human vs Human and Human vs Computer
- **Visual Enhancements**: Hover effects, winning line highlighting in gold
- **Sound System**: Hit sound for moves, end sound for game completion
- **Persistent Scoreboard**: Tracks wins for X, O, and ties across games
- **Modern UI**: Clean interface with rounded buttons and professional styling
- **Game State Management**: Proper boundary checking and error prevention
- **Message System**: Clear win/tie announcements with overlay display
- **Restart Functionality**: Easy game reset without closing the application

### 🎨 **Breakout - Graphics & Visuals Update (July 2025)**
- Added a background color gradient for a modern look.
- Ball and paddle now have colored borders and a shine effect.
- Bricks have a border and a simple shine/gradient on top.

Enjoy the improved visuals! If you want further enhancements (animations, images, etc.), let me know.

### 🔊 Custom Sound Files (All Games)

All games use `.wav` files for sound effects and music. If you see errors about missing sound files (such as `FileNotFoundError: No file 'sound_files/paddle.wav' found...`), you need to generate them:

- **To generate sound files for all games:**
  ```sh
  python generate_sounds.py
  ```
- **To generate only Breakout's special sounds:**
  ```sh
  cd breakout
  python generate_breakout_sounds.py
  ```
- This will create all required `.wav` files in each game's `sound_files/` folder (e.g., `breakout/sound_files/`, `pong/sound_files/`, etc.).
- If you see a `FileNotFoundError` for a `.wav` file, make sure it exists in the correct folder for that game. If you are running a game from inside its folder, you may need to run the sound generation script from the project root.
- If you move or rename any sound files, update the paths in the corresponding `main.py`.
- **Note:** All sound file references and generators now use `.wav` for consistency. Old `.mp3` files are no longer used and can be safely deleted.

### ✨ **New Features:**
- **🟡 Enhanced Pac-Man** - Complete classic implementation with maze, power pellets, and ghost AI
- **🐍 Snake Game** - Classic arcade game with wrap-around edges and progressive difficulty
- **✂️ Enhanced Rock Paper Scissors** - Professional UI with color-coded results and improved game flow
- **📖 On-Screen Instructions** - Every game now displays controls and objectives directly on screen
- **🎮 Enhanced Gameplay** - Improved mechanics in Space Invaders, Poker, and Frogger
- **🚀 Easy Launcher** - One-click game launcher for Windows users (now with 17 games!)
- **📋 Better Documentation** - Comprehensive README with game details
- **🤖 AI Opponents** - Computer-controlled opponents in Pong
- **🎵 Sound Generation** - Programmatically created audio effects

### 🔧 **Improvements:**
- **Pac-Man**: Complete rewrite with classic maze layout, power pellets, ghost AI personalities, and sound effects
- **Snake**: Complete implementation with visible walls, collision detection, progressive speed, and sound effects
- **Space Invaders**: Added enemy types, varied movement patterns, better spawning
- **Poker**: Improved hand ranking logic and winner determination
- **Frogger**: Removed duplicate code, cleaner implementation
- **Pong**: Added computer AI opponent with smart ball tracking
- **Torpedo Attack**: Added sound effects and slower ship speeds
- **Batch Launcher**: Updated to include all 17 games with proper navigation
- **All Games**: Added on-screen instructions for instant learning

### 🎯 **User Experience:**
- **Instant Learning** - No need to read external documentation
- **Consistent Interface** - Same instruction format across all games
- **Professional Polish** - Clean, modern game interfaces
- **Easy Access** - Simple launcher for quick game selection (16 games!)
- **Single Player Options** - AI opponents for solo gameplay
- **Immersive Audio** - Generated sound effects for all games
- **Cross-Platform Compatibility** - Works on Windows, macOS, and Linux

### 🔊 **Audio System:**
- **Generated Sounds** - 26+ sound effects created programmatically
- **High Quality** - 44.1kHz, 16-bit audio
- **Game-Specific** - Unique sounds for each game type
- **Realistic Effects** - Proper decay and frequency modulation
- **Snake Sounds** - Eat and game over effects for immersive gameplay
- **Pac-Man Sounds** - Eat, power pellet, ghost eaten, and death effects
- **Wall Mode** - Visible boundaries with collision detection for classic Snake gameplay

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
