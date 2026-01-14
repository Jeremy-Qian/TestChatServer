# Deployment Guide

This guide shows you how to deploy your chat server on various free hosting platforms using GitHub.

## Quick Overview

- **Replit**: Easiest, import from GitHub
- **PythonAnywhere**: Good for Python projects
- **Glitch**: Requires JavaScript rewrite
- **Heroku**: More complex but powerful
- **Railway**: Direct GitHub deployment

---

## GitHub Setup (Required for most platforms)

### 1. Create GitHub Repository
1. Go to [github.com](https://github.com) and create an account
2. Click "New repository"
3. Name it: `chat-server` (or your preferred name)
4. Make it **Public** (required for free hosting)
5. Don't initialize with README (we already have files)

### 2. Push to GitHub
```bash
# Add remote repository (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/chat-server.git

# Push to GitHub
git push -u origin main
```

### 3. Repository Structure
Your GitHub repo should contain:
```
chat-server/
├── server.py          # Main server application
├── client.py          # Client application  
├── README.md          # Documentation
├── DEPLOYMENT.md      # This deployment guide
├── .gitignore         # Git ignore file
└── requirements.txt   # (empty, no dependencies)
```

---

## 1. Replit (Recommended - Easiest)

### Method 1: Import from GitHub
1. Go to [replit.com](https://replit.com) and create an account
2. Click "Import from GitHub"
3. Enter your GitHub repository URL
4. Replit will automatically import all files

### Method 2: Manual Upload
1. Click "Create Repl" → "Python"
2. Upload your files manually from GitHub

### Important Configuration
**Modify the host in `server.py`**:
```python
# Change this line:
def __init__(self, host='0.0.0.0', port=5555):
# To:
def __init__(self, host='0.0.0.0', port=5555):
```

### Deploy
1. Click "Run" to start the server
2. Replit will give you a public URL
3. Share the URL with friends to connect

---

## 2. Railway (Best for GitHub Integration)

### Steps:
1. Create account at [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Authorize Railway to access your GitHub
4. Select your `chat-server` repository
5. Railway will automatically detect Python
6. Click "Deploy"

### Configuration
Railway automatically:
- Detects Python projects
- Sets environment variables
- Provides public URL
- Handles HTTPS

### Environment Variables
Add these in Railway settings:
```
PORT=5555
HOST=0.0.0.0
```

---

## 3. Heroku (GitHub Integration)

### Setup:
1. Create account at [heroku.com](https://heroku.com)
2. Install Heroku CLI
3. Create `requirements.txt` (empty is fine):
```bash
touch requirements.txt
```

4. Create `Procfile`:
```
web: python3 server.py
```

5. Modify `server.py` for Heroku:
```python
import os
port = int(os.environ.get('PORT', 5000))
host = '0.0.0.0'
```

### Deploy via GitHub:
1. Create new Heroku app
2. Connect to GitHub repository
3. Enable automatic deploys
4. Deploy manually or on push

---

## 4. PythonAnywhere

### Steps:
1. Create account at [pythonanywhere.com](https://pythonanywhere.com)
2. Go to "Files" tab
3. Clone your GitHub repository:
```bash
git clone https://github.com/YOUR_USERNAME/chat-server.git
```
4. Go to "Consoles" → "Bash Console"
5. Navigate to project and run:
```bash
cd chat-server
python3 server.py
```

---

## 5. Glitch (JavaScript Version)

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

## Code Modifications for Hosting

### For All Platforms (except local):
1. **Change host from `0.0.0.0` to `0.0.0.0`**:
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
       self.host = host or '0.0.0.0'  # Default to local
   ```

---

## GitHub Actions (Optional - Auto Deploy)

### Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy to Railway

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Deploy to Railway
      uses: railway-app/railway-action@v1
      with:
        api-token: ${{ secrets.RAILWAY_TOKEN }}
        service: your-service-id
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
- [ ] GitHub repository is public
- [ ] Server starts without errors
- [ ] Clients can connect from different computers
- [ ] Messages appear in real-time
- [ ] 500-character limit works
- [ ] Rule violations show proper messages
- [ ] Server handles disconnections gracefully
- [ ] New users see chat history

### Troubleshooting:
- **Connection refused**: Check if server is running
- **Timeout**: Check firewall settings
- **Messages not appearing**: Verify port and host settings
- **GitHub issues**: Make sure repo is public

---

## Recommended Deployment Flow

### For Beginners:
1. **Start with Replit** - Easiest, GitHub import
2. **Move to Railway** - Better performance, GitHub integration
3. **Consider Heroku** - More features, complex setup

### Quick Replit + GitHub Steps:
1. Push code to GitHub
2. Import to Replit from GitHub
3. Change host to `0.0.0.0`
4. Click Run
5. Share the Replit URL

That's it! Your chat server is live and shareable, with version control via GitHub.
