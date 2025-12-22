# Threes! Game

## Overview
A Python implementation of the puzzle game Threes! using Pygame for graphics rendering.

## Project Structure
- `client.py` - Main game entry point with Pygame window setup and game loop
- `gameState.py` - Game logic including Tile, TileBag, and Threes game classes

## Technology Stack
- Python 3.11
- Pygame 2.6.1 for graphics rendering

## Running the Game
The game runs as a desktop GUI application using VNC display in the Replit environment.

Run command: `python client.py`

## Game Logic
- **Tile**: Represents game tiles with ordinal values that map to display values (1, 2, 3, 6, 12, etc.)
- **TileBag**: Manages the pool of tiles to be drawn during gameplay
- **Threes**: Main game class managing the 4x4 board and game state
