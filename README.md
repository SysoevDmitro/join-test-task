# Event Management REST API

This project is a Django-based RESTful API for managing events (conferences, meetups, etc.). The API allows users to create, view, update, and delete events, register for events, view event registrations, and more.

## Features

- **Event Management**:
  - CRUD operations for events (create, read, update, delete).
- **User Registration and Authentication**:
  - Secure user registration and login.
  - Token-based authentication using JSON Web Tokens (JWT).
- **Event Registration**:
  - Users can register for specific events.
  - View all registered users for an event.
- **Advanced Features**:
  - Event search and filtering.
  - Email notifications upon successful registration.
- **Dockerized**:
  - Simplified deployment using Docker.
- **API Documentation**:
  - Integrated Swagger documentation.

---

## Getting Started

### Prerequisites
- Python 3.10+
- Docker (for containerized setup)
- PostgreSQL

### Installation

1. **Clone the repository:**
   ```
   git clone https://github.com/SysoevDmitro/join-test-task.git
   cd event-management-api
   ```
2. **Create a Virtual Environment:**
   ```
   python -m venv env
   source env/bin/activate
   ```
3. **Install Dependencies:**
   ```
   pip install -r requirements.txt
   ```
4. **Apply Migrations:**
   ```
   python manage.py makemigrations
   ```
5. **Create .env file with your parameters:**
   ```
    SECRET_KEY=
    POSTGRES_PASSWORD=password
    POSTGRES_USER=event
    POSTGRES_DB=event
    POSTGRES_HOST=db
    POSTGRES_PORT=5432
    
    CELERY_BROKER_URL=redis://redis:6379/0
    CELERY_RESULT_BACKEND=redis://redis:6379/0
    
    EMAIL_HOST_USER=your_email@example.com
    EMAIL_HOST_PASSWORD=your_email_password

   ```

6. **Run with Docker:**
   ```
   docker-compose up --build
   ```

### Documentation
- Go to `/api/doc/swagger/` to test api
  - Register with `/api/user/register/`
  - Receive token `/api/user/token/`
  - Paste token to `Authorize header` at the top of the page
