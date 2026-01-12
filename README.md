# Open WebUI Lite 👋


## Local Development (Lite Version) 💻

This is the Lite version with frontend-backend separated architecture for local development.

### Prerequisites

- **Python 3.11+** (for backend)
- **Node.js 22.x** (for frontend)
- **Git**

### Initial Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/open-webui/open-webui.git
   cd open-webui
   ```

2. **Install backend dependencies**:
   ```bash
   # Create virtual environment (recommended)
   python -m venv .venv

   # Activate virtual environment
   # Windows:
   .\.venv\Scripts\activate
   # Linux/macOS:
   source .venv/bin/activate

   # Install Open WebUI in development mode
   pip install -e .
   ```

3. **Install frontend dependencies**:
   ```bash
   npm install
   # If you encounter compatibility issues, try:
   npm install --force
   ```

### Starting the Development Servers

**Backend (Terminal 1)**:
```bash
# Activate virtual environment (if not already activated)
.\.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/macOS

# Set optional environment variables to disable heavy features
set ENABLE_WEB_SEARCH=false
set BYPASS_EMBEDDING_AND_RETRIEVAL=true
set ENABLE_OLLAMA_API=false
set CORS_ALLOW_ORIGIN=http://localhost:5173

# Start backend server
.\.venv\Scripts\open-webui serve --host 0.0.0.0 --port 8080
```

Backend will be available at [http://localhost:8080](http://localhost:8080)
- Health check: [http://localhost:8080/health](http://localhost:8080/health)
- API docs: [http://localhost:8080/docs](http://localhost:8080/docs)

**Frontend (Terminal 2)**:
```bash
npm run dev -- --host --port 5173
```

Frontend will be available at [http://localhost:5173](http://localhost:5173)

### Docker Development (Optional)

For containerized development with frontend-backend separation:

```bash
# Build and start both frontend and backend
docker-compose up --build -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```
