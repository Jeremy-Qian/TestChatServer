#!/usr/bin/env python3
import socket
import threading
import sys
from datetime import datetime

class MessageClient:
    def __init__(self, host='127.0.0.1', port=5555):
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.nickname = ""
        
    def receive(self):
        """Receive messages from server"""
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if message == 'NICK':
                    self.client.send(self.nickname.encode('utf-8'))
                else:
                    # Clear the current line and print the message
                    print(f"\r\033[K{message}")
                    print('> ', end='', flush=True)
            except Exception as e:
                print("\nConnection lost!")
                self.client.close()
                break
    
    def write(self):
        """Send messages to server"""
        while True:
            try:
                # Print prompt and get input in one go
                message = input('> ')
                if message.lower() == '/quit':
                    self.client.close()
                    print("\rDisconnected from server.")
                    sys.exit(0)
                
                # Check message length before sending
                if len(message) > 500:
                    print(f"\r\033[K\033[1A\r\033[KERROR: Message too long! Maximum 500 characters allowed. You were disconnected.")
                    self.client.close()
                    sys.exit(0)
                
                # Format the message locally for immediate display
                timestamp = datetime.now().strftime('%H:%M:%S')
                formatted_msg = f"[{timestamp}] {self.nickname}: {message}"
                # Clear the current line (which contains "> message") and print the formatted message
                print(f"\r\033[K\033[1A\r\033[K{formatted_msg}")
                # Send the raw message - server will format it for others
                self.client.send(message.encode('utf-8'))
            except KeyboardInterrupt:
                self.client.close()
                print("\nDisconnecting...")
                sys.exit(0)
            except Exception as e:
                print(f"\rError: {e}")
                break
    
    def start(self):
        """Start the client"""
        try:
            self.client.connect((self.host, self.port))
            print(f"Connected to server at {self.host}:{self.port}")
            
            # Get nickname
            self.nickname = input("Choose your nickname: ")
            
            # Start threads for receiving and writing
            receive_thread = threading.Thread(target=self.receive)
            receive_thread.daemon = True
            receive_thread.start()
            
            write_thread = threading.Thread(target=self.write)
            write_thread.daemon = True
            write_thread.start()
            
            print("Type messages and press Enter to send. Type '/quit' to exit.")
            
            # Keep main thread alive
            write_thread.join()
            
        except ConnectionRefusedError:
            print(f"Connection refused. Make sure the server is running on {self.host}:{self.port}")
        except KeyboardInterrupt:
            print("\nDisconnecting...")
            self.client.close()
        except Exception as e:
            print(f"Error: {e}")
            self.client.close()

if __name__ == "__main__":
    client = MessageClient()
    client.start()
