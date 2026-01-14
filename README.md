# Local Chat Server

A simple client-server messaging application that runs locally on 0.0.0.0.

## Features

- Real-time messaging between multiple clients
- Nickname support
- Connection/disconnection notifications
- Timestamps for all messages
- Clean disconnect with `/quit` command
- **Message length validation (500 character limit)**
- **Automatic disconnection for rule violations**
- **Bold warning messages for important notices**

## Usage

### 1. Start the Server

```bash
python3 server.py
```

The server will start on `0.0.0.0:5555` and wait for connections.

### 2. Connect Clients

Open new terminal windows and run:

```bash
python3 client.py
```

Each client will be prompted to choose a nickname, then can start chatting.

### 3. Chatting

- Type messages and press Enter to send
- All connected clients will see the messages
- Type `/quit` to disconnect gracefully
- Server console shows connection status and messages
- **Messages over 500 characters will result in automatic disconnection**
- **Rule violations are announced to all users**

## Rules and Restrictions

- **Maximum message length: 500 characters**
- Violating the message length limit will:
  - Immediately disconnect your client
  - Broadcast a violation notice to all users
  - Show an error message on your screen

## Requirements

- Python 3.x
- No external dependencies required

## Default Configuration

- **Host**: 0.0.0.0 (localhost)
- **Port**: 5555
- **Protocol**: TCP
- **Message limit**: 500 characters

## Example Session

1. Terminal 1: `python3 server.py`
2. Terminal 2: `python3 client.py` → nickname: Alice
3. Terminal 3: `python3 client.py` → nickname: Bob
4. Alice and Bob can now exchange messages in real-time

## Troubleshooting

- If you get "Connection refused", make sure the server is running first
- Use Ctrl+C to stop the server
- Each client needs its own terminal window
- **Keep messages under 500 characters to avoid disconnection**

## Security Features

- Automatic message length enforcement
- Immediate disconnection for rule violations
- Server-side validation prevents abuse
- Clear warning messages displayed to all users
