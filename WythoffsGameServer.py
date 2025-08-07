#python WythoffsGameClient.py <server_address> <port_number>

import socket
import threading
import sys

# manage game server
# server listens for 2 clients
# handle game logic
class WythoffsGameServer:
    def __init__(self, port, pile0=5, pile1=10):
        self.piles = [pile0, pile1]  
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []  # assumption: only 2 players
        self.lock = threading.Lock() 
        self.turn = 0  # player0 = 0, player1 = 1
        self.running = True 

    # start server
    # handle client connections
    def start(self):
        self.server_socket.bind(("", self.port))
        self.server_socket.listen(2)
        print("Waiting for connections.")

        
        while len(self.clients) < 2:                # will not take any action before 2 players connect
            conn, addr = self.server_socket.accept()
            self.clients.append(conn)
            player_id = len(self.clients) - 1
            print(f"Player {player_id} is connected.")
            conn.sendall("Connected to server.".encode())

        print(f"Game is starting: Piles are {self.piles}")
        self.broadcast(f"Game starting...\n---\nCurrent Piles: {self.piles}\n")
        
        # Send initial turn message
        self.clients[0].sendall("It's your turn!".encode())
        self.clients[1].sendall("It is Player 0's turn.".encode())
        print("Waiting for Player 0's move...")

        # 1 thread per player
        for i in range(2):
            t = threading.Thread(target=self.handle_client, args=(i,))
            t.start()

    # sends a message to both players
    def broadcast(self, msg):
        for client in self.clients:
            try:
                client.sendall(msg.encode())
            except:
                pass

    # single client's moves
    def handle_client(self, player_id):
        conn = self.clients[player_id]
        while self.running:
            try:
                move = conn.recv(1024).decode()
                if not move:  # Connection closed
                    break
                    
                print(f"Received move from Player {player_id}: \"{move}\".", end="")

                try:
                    pile_index, count = map(int, move.strip().split())
                except:
                    print(" Illegal move: invalid format.")
                    conn.sendall("Received error from server: \"Invalid input format.\"\nPlease enter a valid move.".encode())
                    print(f"Waiting for Player {player_id}'s move...")
                    continue

                with self.lock:
                    if self.turn != player_id:
                        # if it's not the player's turn, flag.
                        print(" Illegal move: not your turn.")
                        conn.sendall("Received error from server: \"It's not your turn.\"\nPlease wait for your turn.".encode())
                        print(f"Waiting for Player {player_id}'s move...")
                        continue

                    if self.is_valid_move(pile_index, count):
                        print(" Legal move.")
                        self.apply_move(pile_index, count)

                        if self.piles == [0, 0]:
                            # game end
                            print(f"Game Over. Player {player_id} wins!")
                            print("Closing connections.")
                            
                            # Send win message to winner (with newline)
                            conn.sendall(f"---\nCurrent Piles: {self.piles}\nCongratulations! You win!\nServer has closed the connection.".encode())
                            
                            # Send loss message to other player (with newline)
                            other_player = 1 - player_id
                            self.clients[other_player].sendall(f"---\nCurrent Piles: {self.piles}\nGame over. Player {player_id} is the winner.\nServer has closed the connection.".encode())
                            
                            self.running = False
                            print(f"Player {player_id} disconnected.") 
                            self.shutdown()
                            return
                        else:
                            # switch turn
                            self.turn = 1 - player_id
                            print(f"Waiting for Player {self.turn}'s move...")
                            
                            # Send msg to both players
                            self.broadcast(f"---\nCurrent Piles: {self.piles}\n")
                            self.clients[self.turn].sendall("It's your turn!".encode())
                            self.clients[1 - self.turn].sendall(f"It is Player {self.turn}'s turn.".encode())
                            
                    else:
                        # invalid move - determine the specific error
                        error_msg = self.get_error_message(pile_index, count)
                        print(f" Illegal move: {error_msg}.")
                        conn.sendall(f"Received error from server: \"Illegal move: {error_msg}\"\nPlease enter a valid move.".encode())
                        print(f"Waiting for Player {player_id}'s move...")
            except Exception as e:
                if self.running:
                    print(f"Error with player {player_id}: {e}")
                break

        print(f"Player {player_id} disconnected.")

    # invalid move error msg logic
    def get_error_message(self, pile_index, count):
        if count <= 0:
            return "count must be positive"
        if pile_index == 0:
            if count > self.piles[0]:
                return f"not enough objects in pile 0"
        elif pile_index == 1:
            if count > self.piles[1]:
                return f"not enough objects in pile 1"
        elif pile_index == 2:
            if count > self.piles[0]:
                return f"not enough objects in pile 0"
            elif count > self.piles[1]:
                return f"not enough objects in pile 1"
        else:
            return "invalid pile index"
        return "invalid move"

    # legal move check
    def is_valid_move(self, pile_index, count):
        if count <= 0:
            return False
        if pile_index == 0:
            return count <= self.piles[0]
        elif pile_index == 1:
            return count <= self.piles[1]
        elif pile_index == 2:
            return count <= self.piles[0] and count <= self.piles[1]
        return False

    # if valid, apply the move
    def apply_move(self, pile_index, count):
        if pile_index == 0:
            self.piles[0] -= count
        elif pile_index == 1:
            self.piles[1] -= count
        elif pile_index == 2:
            self.piles[0] -= count
            self.piles[1] -= count
        print(f"Piles after move: {self.piles}.")

    # if game ends, close connections
    def shutdown(self):
        self.running = False
        for conn in self.clients:
            try:
                conn.shutdown(socket.SHUT_RDWR)  # Ensure data is sent before closing
                conn.close()
            except:
                pass
        try:
            self.server_socket.close()
        except:
            pass

if __name__ == '__main__':
    #default value ekledim ama buyuk ihtimal kullanilmaz. unutulursa filan diye.
    port = int(sys.argv[1])
    pile0 = int(sys.argv[2]) if len(sys.argv) > 2 else 5 
    pile1 = int(sys.argv[3]) if len(sys.argv) > 3 else 10
    

    server = WythoffsGameServer(port, pile0, pile1)
    server.start()
