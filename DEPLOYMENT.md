# Deployment Guide

This guide shows you how to deploy your chat server on various free hosting platforms.

## Quick Overview

- **Replit**: Easiest, no setup required
- **PythonAnywhere**: Good for Python projects
- **Glitch**: Requires JavaScript rewrite
- **Heroku**: More complex but powerful

---

## 1. Replit (Recommended - Easiest)

### Steps:
1. Go to [replit.com](https://replit.com) and create an account
2. Click "Create Repl" → "Python"
3. Upload your files:
   - `server.py`
   - `client.py` (optional, for testing)
4. **Important**: Modify the host in `server.py`:
   ```python
   # Change this line:
   def __init__(self, host='127.0.0.1', port=5555):
   # To:
   def __init__(self, host='0.0.0.0', port=5555):
   ```
5. Click "Run" to start the server
6. Replit will give you a public URL
7. Share the URL with friends to connect

### Client Connection:
- Others can connect using the Replit URL
- Modify `client.py` to use the Replit URL instead of `127.0.0.1`

---

## 2. PythonAnywhere

### Steps:
1. Create account at [pythonanywhere.com](https://pythonanywhere.com)
2. Go to "Files" tab
3. Upload your `server.py`
4. Go to "Consoles" → "Bash Console"
5. Install dependencies (none needed for this project)
6. Run: `python3 server.py`
7. Note the server details for sharing

### Limitations:
- Free tier has some restrictions
- May need to upgrade for persistent connections

---

## 3. Glitch (JavaScript Version)

### Requirements:
- Need to rewrite in JavaScript/Node.js
- Use Socket.io for real-time communication

### Basic Structure:
```javascript
// server.js (Glitch version)
const express = require('express');
const http = require('http');
const socketIo = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = socketIo(server);

io.on('connection', (socket) => {
  console.log('User connected:', socket.id);
  
  socket.on('chat message', (data) => {
    io.emit('chat message', data);
  });
  
  socket.on('disconnect', () => {
    console.log('User disconnected');
  });
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
```

---

## 4. Heroku

### Setup:
1. Install Heroku CLI
2. Create `requirements.txt`:
   ```
   # No external dependencies needed
   ```
3. Create `Procfile`:
   ```
   web: python3 server.py
   ```
4. Modify `server.py` for Heroku:
   ```python
   import os
   port = int(os.environ.get('PORT', 5000))
   host = '0.0.0.0'
   ```
5. Deploy:
   ```bash
   heroku create
   git add .
   git commit -m "Deploy chat server"
   git push heroku main
   ```

---

## 5. Railway

### Steps:
1. Create account at [railway.app](https://railway.app)
2. Create new project
3. Upload your files
4. Railway will automatically detect Python
5. Deploy and get public URL

---

## Code Modifications for Hosting

### For All Platforms (except local):
1. **Change host from `127.0.0.1` to `0.0.0.0`**:
   ```python
   def __init__(self, host='0.0.0.0', port=5555):
   ```

2. **Use environment variables for port**:
   ```python
   import os
   port = int(os.environ.get('PORT', 5555))
   ```

3. **Update client connection**:
   ```python
   # In client.py, allow custom host:
   def __init__(self, host=None, port=5555):
       self.host = host or '127.0.0.1'  # Default to local
   ```

---

## Security Considerations

### For Public Hosting:
1. **Rate Limiting**: Add message rate limits
2. **Input Validation**: Already have 500 char limit
3. **Connection Limits**: Limit concurrent users
4. **Logging**: Log connections and violations

### Example Rate Limiting:
```python
import time
from collections import defaultdict

class MessageServer:
    def __init__(self, host='0.0.0.0', port=5555):
        # ... existing code ...
        self.message_times = defaultdict(list)
        self.rate_limit = 10  # 10 messages per minute
    
    def check_rate_limit(self, nickname):
        now = time.time()
        times = self.message_times[nickname]
        # Remove old messages (older than 1 minute)
        times[:] = [t for t in times if now - t < 60]
        if len(times) >= self.rate_limit:
            return False
        times.append(now)
        return True
```

---

## Testing Your Deployment

### Checklist:
- [ ] Server starts without errors
- [ ] Clients can connect from different computers
- [ ] Messages appear in real-time
- [ ] 500-character limit works
- [ ] Rule violations show proper messages
- [ ] Server handles disconnections gracefully

### Troubleshooting:
- **Connection refused**: Check if server is running
- **Timeout**: Check firewall settings
- **Messages not appearing**: Verify port and host settings

---

## Recommended: Start with Replit

**Why Replit is best for beginners:**
- Zero configuration needed
- Built-in terminal and editor
- Automatic HTTPS
- Easy sharing
- Free for small projects

**Quick Replit Steps:**
1. Upload files
2. Change host to `0.0.0.0`
3. Click Run
4. Share the URL

That's it! Your chat server is live and shareable.
