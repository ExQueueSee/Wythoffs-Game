# Wythoff's Game - Networked Implementation

A Python implementation of Wythoff's Game using TCP sockets for networked multiplayer gameplay. This project features a server that manages the game state and coordinates between two players connected via TCP clients.

## Table of Contents

- [Overview](#-overview)
- [Game Rules](#-game-rules)
- [Features](#-features)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Usage](#-usage)
- [Example Gameplay](#-example-gameplay)
- [Protocol](#-protocol)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)

## Overview

Wythoff's Game is a variant of the classic Nim game played with two piles of objects. This implementation allows two players to connect over a network and play against each other in real-time. The server manages the game state, validates moves, and coordinates turn-based gameplay between the connected clients.

## Game Rules

Wythoff's Game is played with two piles of objects. Players take turns making one of three possible moves:

1. **Remove from Pile 0** (`pile_index = 0`): Remove any number of objects from the first pile only
2. **Remove from Pile 1** (`pile_index = 1`): Remove any number of objects from the second pile only  
3. **Remove from Both Piles** (`pile_index = 2`): Remove the same number of objects from both piles simultaneously

### Winning Condition
The player who makes the final move to empty both piles (reducing both to [0, 0]) wins the game.

### Move Validation
- The number of objects to remove (`count`) must be positive (> 0)
- Cannot remove more objects than are available in the selected pile(s)
- Players can only move during their designated turn

## ✨ Features

- **Networked Multiplayer**: Two players can connect from different machines
- **Real-time Gameplay**: Synchronous turn-based gameplay with immediate feedback
- **Move Validation**: Comprehensive validation with descriptive error messages
- **Threaded Server**: Handles multiple client connections using threading
- **Configurable Game Setup**: Customizable initial pile sizes
- **Clean Protocol**: Simple text-based communication protocol
- **Error Handling**: Robust error handling for network issues and invalid moves

## 🔧 Requirements

- Python 3.6 or higher
- Network connectivity between server and clients
- No external dependencies (uses only Python standard library)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ExQueueSee/Wythoffs-Game.git
cd Wythoffs-Game
```

2. No additional installation required - uses only Python standard library.

## Usage

### Starting the Server

```bash
python WythoffsGameServer.py <port_number> [<pile_0_size> <pile_1_size>]
```

**Parameters:**
- `port_number`: Port number for the server to listen on
- `pile_0_size`: Initial size of pile 0 (default: 5)
- `pile_1_size`: Initial size of pile 1 (default: 10)

**Examples:**
```bash
# Start server on port 6000 with default pile sizes [5, 10]
python WythoffsGameServer.py 6000

# Start server on port 6000 with custom pile sizes [7, 5]
python WythoffsGameServer.py 6000 7 5
```

### Connecting Clients

```bash
python WythoffsGameClient.py <server_address> <port_number>
```

**Parameters:**
- `server_address`: IP address of the server (use `127.0.0.1` for local testing)
- `port_number`: Port number the server is listening on

**Examples:**
```bash
# Connect to local server
python WythoffsGameClient.py 127.0.0.1 6000

# Connect to remote server
python WythoffsGameClient.py 192.168.1.100 6000
```

### Making Moves

When it's your turn, enter moves in the format: `<pile_index> <count>`

- `0 3`: Remove 3 objects from pile 0
- `1 2`: Remove 2 objects from pile 1  
- `2 1`: Remove 1 object from both piles

## Example Gameplay

### Server Console:
```
Waiting for connections.
Player 0 is connected.
Player 1 is connected.
Game is starting: Piles are [7, 5]
Waiting for Player 0's move...
Received move from Player 0: "2 3". Legal move.
Piles after move: [4, 2].
Waiting for Player 1's move...
Received move from Player 1: "0 2". Legal move.
Piles after move: [2, 2].
Waiting for Player 0's move...
Received move from Player 0: "2 2". Legal move.
Game Over. Player 0 wins!
Closing connections.
```

### Client 0 Console (Winner):
```
Connected to server.
Game starting...
---
Current Piles: [7, 5]
It's your turn!
Enter move (pile_index count; use 2 for both): 2 3
---
Current Piles: [4, 2]
It is Player 1's turn.
---
Current Piles: [2, 2]
It's your turn!
Enter move (pile_index count; use 2 for both): 2 2
---
Current Piles: [0, 0]
Congratulations! You win!
Server has closed the connection.
```

### Client 1 Console (Loser):
```
Connected to server.
Game starting...
---
Current Piles: [7, 5]
It is Player 0's turn.
---
Current Piles: [4, 2]
It's your turn!
Enter move (pile_index count; use 2 for both): 0 2
---
Current Piles: [2, 2]
It is Player 0's turn.
---
Current Piles: [0, 0]
Game over. Player 0 is the winner.
Server has closed the connection.
```

## Protocol

The game uses a simple text-based protocol over TCP:

### Server Messages:
- `Connected to server.` - Sent when client connects
- `Game starting...` - Game initialization
- `---\nCurrent Piles: [x, y]` - Game state updates
- `It's your turn!` - Turn notification for current player
- `It is Player X's turn.` - Turn notification for waiting player
- `Received error from server: "<error_message>"` - Error notifications
- `Congratulations! You win!` - Win notification
- `Game over. Player X is the winner.` - Loss notification
- `Server has closed the connection.` - Connection termination

### Client Messages:
- `<pile_index> <count>` - Move commands (e.g., "2 3", "0 1", "1 4")

## Project Structure

```
WythoffsGame/
├── WythoffsGameServer.py    # Server implementation
├── WythoffsGameClient.py    # Client implementation
└── README.md               # This file
```

### Key Components:

**WythoffsGameServer.py:**
- `WythoffsGameServer` class: Main server logic
- Threaded client handling
- Move validation and game state management
- Win condition detection

**WythoffsGameClient.py:**
- `WythoffsGameClient` class: Client interface
- Server message processing
- User input handling
- Game state display

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is part of an academic assignment for BIL452 - Network Programming course.

## Known Issues

- Server must be restarted between games
- No spectator mode implemented
- No game replay functionality

