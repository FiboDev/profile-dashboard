# Profile Application

A full-stack profile management application built with React frontend, FastAPI backend, and PostgreSQL database, all running in Docker containers.

## Features

- User profile management
- Skills tracking with radar chart visualization
- Modern React frontend with TypeScript
- FastAPI backend with SQLAlchemy ORM
- PostgreSQL database with Alembic migrations
- Docker containerization with Docker Compose
- User authentication and authorization

## Tech Stack

### Frontend
- React 18 with TypeScript
- Vite for build tooling
- Tailwind CSS for styling
- Recharts for data visualization
- Nginx for serving and API proxying

### Backend
- FastAPI with Python 3.12
- SQLAlchemy ORM
- Alembic for database migrations
- Poetry for dependency management
- Pydantic for data validation

### Database
- PostgreSQL 16
- Docker volume for data persistence

## Project Structure

```
├── docker-compose.yml          # Container orchestration
├── frontend/                   # React application
│   ├── src/
│   │   ├── components/         # Reusable components
│   │   ├── pages/             # Page components
│   │   ├── services/          # API services
│   │   └── types/             # TypeScript types
│   ├── Dockerfile
│   └── nginx.conf             # Nginx configuration
├── backend/                    # FastAPI application
│   ├── app/
│   │   ├── user/              # User management module
│   │   ├── skill/             # Skills management module
│   │   └── core/              # Core configuration
│   ├── database/              # Database configuration
│   ├── alembic/               # Database migrations
│   ├── Dockerfile
│   └── pyproject.toml         # Python dependencies
└── README.md
```

## Getting Started

### Prerequisites
- Docker and Docker Compose
- Git

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd profile-management-app
```

2. **Install Docker** (if not already installed):

   Choose the installation guide for your operating system:
   
   - **Ubuntu/Linux**: [Docker Engine Installation](https://docs.docker.com/engine/install/ubuntu/)
   - **Windows**: [Docker Desktop for Windows](https://docs.docker.com/desktop/setup/install/windows-install/)
   - **macOS**: [Docker Desktop for Mac](https://docs.docker.com/desktop/setup/install/mac-install/)

3. Start the application with Docker Compose:
```bash
docker-compose up --build
```

4. Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Usage

Once the application is running, you can access the frontend at http://localhost:3000. The system comes pre-loaded with demo user accounts that you can use to log in and explore the application:

### Test Credentials

| Email | Password | Role |
|-------|----------|------|
| `juan.perez@example.com` | `password123` | Senior Developer |
| `maria.garcia@example.com` | `password456` | Data Scientist |
| `carlos.lopez@example.com` | `password789` | DevOps Engineer |

### Features Available After Login

- View your profile details
- See your skills visualized in a radar chart

### Development

The application is configured for development with:
- Hot reloading for both frontend and backend
- Volume mounts for code changes
- Automatic database migrations

### Database Setup

The database is automatically initialized with:
- User and Skill tables
- Sample data for testing
- Proper relationships and constraints

## API Endpoints

### Users
- `GET /api/v1/users/` - List all users
- `POST /api/v1/users/` - Create a new user
- `GET /api/v1/users/{user_id}` - Get user by ID
- `PUT /api/v1/users/{user_id}` - Update user
- `DELETE /api/v1/users/{user_id}` - Delete user

### Skills
- `GET /api/v1/skills/` - List all skills
- `POST /api/v1/skills/` - Create a new skill
- `GET /api/v1/skills/{skill_id}` - Get skill by ID
- `PUT /api/v1/skills/{skill_id}` - Update skill
- `DELETE /api/v1/skills/{skill_id}` - Delete skill

## Environment Variables

### Frontend (.env)
```
VITE_API_BASE_URL=http://backend_profile_app:8000
VITE_ENVIRONMENT=development
```

### Backend
```
DATABASE_URL=postgresql://profile_user:profile_password@postgres_profile_app:5432/profile_db
SECRET_KEY=your-secret-key-here
```
