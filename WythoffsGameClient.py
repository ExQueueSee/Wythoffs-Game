# python WythoffsGameServer.py <port_number> [<pile_0_size> <pile_1_size>]")
import socket
import sys


class WythoffsGameClient:
    def __init__(self, server_ip, port):
        self.server_ip = server_ip
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = True

    # connect to server
    # handle game logic
    def start(self):
        self.client_socket.connect((self.server_ip, self.port))
        
        while self.running:
            try:
                msg = self.client_socket.recv(1024).decode() #1024 is common buffer size
                if not msg:
                    break
                    
                print(msg)
                
                # Check if it's our turn to make a move OR if we need to re-enter after an error
                should_prompt = False
                
                if "It's your turn!" in msg:
                    should_prompt = True
                elif "Please enter a valid move" in msg:
                    should_prompt = True
                
                if should_prompt:
                    move = input("Enter move (pile_index count; use 2 for both): ")
                    self.client_socket.sendall(move.encode())
                elif ("Server has closed the connection" in msg or 
                      "Congratulations! You win!" in msg or 
                      "Game over. Player" in msg):
                    self.running = False
                    
            except Exception as e:
                print(f"Connection closed or error: {e}")
                self.running = False

        self.client_socket.close()

# main
if __name__ == '__main__':

    server_ip = sys.argv[1]
    port = int(sys.argv[2])

    client = WythoffsGameClient(server_ip, port)
    client.start()
