# Task Management System

A full-stack web application for managing tasks efficiently. Built with FastAPI (Python backend), React (TypeScript frontend), and PostgreSQL database, all containerized with Docker.

## Prerequisites

### For Docker Setup

- Docker & Docker Compose

### For Manual Setup

- Python 3.11+
- Node.js 16+
- PostgreSQL 15

## Docker Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/DilukaDev/task-management-system.git
   cd task-management-system
   ```

2. **Create environment file**

   ```bash
   # Copy the example env file
   cp .env.example .env
   ```

   Update `.env` with your database credentials if needed.

3. **Start all services**

   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Manual Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/DilukaDev/task-management-system.git
   cd task-management-system
   ```

2. **Create environment file**

   ```bash
   # Copy the example env file
   cp .env.example .env
   ```

   Update `.env` with your database credentials if needed.

### Backend Setup

3. **Navigate to backend directory**

   ```bash
   cd backend
   ```

4. **Create virtual environment and install dependencies**

   ```bash
   uv sync
   ```

5. **Activate virtual environment**

   ```bash
   .venv\Scripts\activate
   ```

6. **Start PostgreSQL**

   ```bash
   # Make sure PostgreSQL is running on port 5432
   ```

7. **Run migrations and start server**
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend Setup

8. **Navigate to frontend directory**

   ```bash
   cd frontend
   ```

9. **Install dependencies**

   ```bash
   npm install
   ```

10. **Start development server**

    ```bash
    npm run dev
    ```

11. **Access frontend**

- Open http://localhost:5173 in your browser

## Project Structure

```
task-management-system/
├── backend/                         # Python FastAPI backend
│   ├── app/
│   │   ├── main.py                  # FastAPI application setup
│   │   ├── controllers/             # API route handlers
│   │   ├── services/                # Business logic layer
│   │   ├── repositories/            # Data access layer
│   │   ├── models/                  # Pydantic models & database schemas
│   │   ├── core/                    # Configuration
│   │   └── database/                # Database connection & initialization
│   ├── tests/                       # Unit and integration tests
│   ├── Dockerfile                   # Backend containerization
│   ├── pyproject.toml               # Python dependencies
│   └── README.md
│
├── frontend/                        # React TypeScript frontend
│   ├── src/
│   │   ├── App.tsx                  # Main application component
│   │   ├── main.tsx                 # React entry point
│   │   ├── components/              # React components
│   │   │   ├── TaskForm.tsx         # Task creation form
│   │   │   └── TaskList.tsx         # Tasks display component
│   │   ├── services/                # API client services
│   │   ├── types/                   # TypeScript type definitions
│   │   └── config/                  # Configuration
│   ├── Dockerfile                   # Frontend containerization
│   ├── package.json                 # NPM dependencies
│   ├── vite.config.ts               # Vite configuration
│   ├── index.html                   # HTML entry point
│   └── README.md
│
├── docker-compose.yml               # Docker compose configuration
└── README.md
```

## API Endpoints

### Tasks

- `POST /api/v1/tasks/create` - Create new task
- `GET /api/v1/tasks/recent` - Get recent tasks
- `PATCH /api/v1/tasks/{id}/complete` - Mark task as completed

### Health Check

- `GET /health` - API health check

### Documentation

- `GET /docs` - Swagger UI interactive documentation

## Running Tests

### Backend Tests

```bash
cd backend

# Run all tests
pytest
```

### Testing API with curl

#### Create a Task

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/api/v1/tasks/create' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "string",
  "description": "string"
}'
```

#### Get Recent Tasks

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/api/v1/tasks/recent' \
  -H 'accept: application/json'
```

#### Mark Task as Completed

```bash
curl -X 'PATCH' \
  'http://127.0.0.1:8000/api/v1/tasks/{task_id}/complete' \
  -H 'accept: application/json'
```

Replace `{task_id}` with the actual task ID (e.g., `38`)
