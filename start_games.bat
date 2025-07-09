@echo off
title Pygame Games Launcher
color 0A

:menu
cls
echo.
echo  ========================================
echo  =         PYGAME GAMES LAUNCHER       =
echo  ========================================
echo.
echo  Select a game to play:
echo.
echo  1.  Pac-Man
echo  2.  Blackjack
echo  3.  Breakout
echo  4.  Car Race
echo  5.  Frogger
echo  6.  Poker
echo  7.  Pong
echo  8.  Reversi
echo  9.  Rock Paper Scissors
echo  10. Slot Machine
echo  11. Space Invaders
echo  12. Tetris
echo  13. Tic Tac Toe
echo  14. Torpedo Attack
echo  15. Snake
echo.
echo  0.  Exit
echo.
echo  ========================================
echo.

set /p choice="Enter your choice (0-15): "

if "%choice%"=="1" goto pacman
if "%choice%"=="2" goto blackjack
if "%choice%"=="3" goto breakout
if "%choice%"=="4" goto car_race
if "%choice%"=="5" goto frogger
if "%choice%"=="6" goto poker
if "%choice%"=="7" goto pong
if "%choice%"=="8" goto reversi
if "%choice%"=="9" goto rock_paper_scissors
if "%choice%"=="10" goto slot_machine
if "%choice%"=="11" goto space_invaders
if "%choice%"=="12" goto tetris
if "%choice%"=="13" goto tictactoe
if "%choice%"=="14" goto torpedo_attack
if "%choice%"=="15" goto snake
if "%choice%"=="0" goto exit
goto menu

:pacman
cls
echo Starting Pac-Man...
cd pacman
python main.py
cd ..
goto menu

:blackjack
cls
echo Starting Blackjack...
cd blackjack
python main.py
cd ..
goto menu

:breakout
cls
echo Starting Breakout...
cd breakout
python main.py
cd ..
goto menu

:car_race
cls
echo Starting Car Race...
cd car_race
python main.py
cd ..
goto menu

:frogger
cls
echo Starting Frogger...
cd frogger
python main.py
cd ..
goto menu

:poker
cls
echo Starting Poker...
cd poker
python main.py
cd ..
goto menu

:pong
cls
echo Starting Pong...
cd pong
python main.py
cd ..
goto menu

:reversi
cls
echo Starting Reversi...
cd reversi
python main.py
cd ..
goto menu

:rock_paper_scissors
cls
echo Starting Rock Paper Scissors...
cd rock_paper_scissors
python main.py
cd ..
goto menu

:slot_machine
cls
echo Starting Slot Machine...
cd slot_machine
python main.py
cd ..
goto menu

:space_invaders
cls
echo Starting Space Invaders...
cd space_invaders
python main.py
cd ..
goto menu

:tetris
cls
echo Starting Tetris...
cd tetris
python main.py
cd ..
goto menu

:tictactoe
cls
echo Starting Tic Tac Toe...
cd tictactoe
python main.py
cd ..
goto menu

:torpedo_attack
cls
echo Starting Torpedo Attack...
cd torpedo_attack
python main.py
cd ..
goto menu

:snake
cls
echo Starting Snake...
cd snake
python main.py
cd ..
goto menu

:exit
cls
echo Thanks for playing!
pause
exit 