#!/usr/bin/env python3
import socket
import threading
import json
from datetime import datetime

class MessageServer:
    def __init__(self, host='0.0.0.0', port=5555):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clients = []
        self.nicknames = []
        self.chat_history = []  # Store chat messages
        self.max_history = 100  # Keep last 100 messages
        
    def broadcast(self, message, client_socket=None, save_to_history=True):
        """Send message to all connected clients"""
        # Save to history if it's a chat message (not system messages)
        if save_to_history and not message.startswith('[') or ': ' in message:
            self.chat_history.append(message)
            # Keep only the last max_history messages
            if len(self.chat_history) > self.max_history:
                self.chat_history.pop(0)
        
        for client in self.clients:
            if client != client_socket:
                try:
                    client.send(message.encode('utf-8'))
                except:
                    self.remove_client(client)
    
    def remove_client(self, client, reason="left"):
        """Remove disconnected client"""
        if client in self.clients:
            index = self.clients.index(client)
            self.clients.remove(client)
            nickname = self.nicknames[index]
            self.nicknames.remove(nickname)
            client.close()
            
            if reason == "violation":
                # Don't broadcast here - it's already handled in handle_client
                print(f"{nickname} was kicked out for rule violation")
            else:
                broadcast_msg = f"[{datetime.now().strftime('%H:%M:%S')}] {nickname} left the chat"
                self.broadcast(broadcast_msg)
                print(f"{nickname} disconnected")
    
    def handle_client(self, client):
        """Handle individual client connection"""
        try:
            # Get nickname
            client.send("NICK".encode('utf-8'))
            nickname = client.recv(1024).decode('utf-8')
            self.nicknames.append(nickname)
            self.clients.append(client)
            
            print(f"{nickname} connected from {client.getpeername()}")
            
            # Announce new connection
            broadcast_msg = f"[{datetime.now().strftime('%H:%M:%S')}] {nickname} joined the chat"
            self.broadcast(broadcast_msg)
            
            # Send welcome message to client
            welcome_msg = f"Welcome to the chat, {nickname}! Connected to server at {self.host}:{self.port}\n   \033[1mWARNING: Messages over 500 characters will result in automatic disconnection.\033[0m"
            client.send(welcome_msg.encode('utf-8'))
            
            # Send chat history to new user
            if self.chat_history:
                history_header = "\n\033[1m--- Chat History (Last {len(self.chat_history)} messages) ---\033[0m"
                client.send(history_header.encode('utf-8'))
                for msg in self.chat_history:
                    client.send(msg.encode('utf-8'))
                history_footer = "\033[1m--- End of History ---\033[0m\n"
                client.send(history_footer.encode('utf-8'))
            
            while True:
                try:
                    message = client.recv(1024).decode('utf-8')
                    if message:
                        # Check message length
                        if len(message) > 500:
                            violation_msg = f"[{datetime.now().strftime('%H:%M:%S')}] {nickname} was kicked out because of rule violation."
                            print(violation_msg)
                            self.broadcast(violation_msg)
                            client.close()
                            self.remove_client(client, reason="violation")
                            break
                        
                        timestamp = datetime.now().strftime('%H:%M:%S')
                        formatted_msg = f"[{timestamp}] {nickname}: {message}"
                        print(formatted_msg)
                        self.broadcast(formatted_msg, client, save_to_history=True)
                    else:
                        break
                except:
                    break
        except:
            pass
        finally:
            self.remove_client(client)
    
    def start(self):
        """Start the server"""
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        print(f"Server started on {self.host}:{self.port}")
        print("Waiting for connections...")
        
        try:
            while True:
                client, address = self.server.accept()
                print(f"Connection from {address}")
                thread = threading.Thread(target=self.handle_client, args=(client,))
                thread.daemon = True
                thread.start()
        except KeyboardInterrupt:
            print("\nShutting down server...")
        finally:
            self.server.close()

if __name__ == "__main__":
    server = MessageServer()
    server.start()
