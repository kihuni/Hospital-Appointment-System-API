# Hospital Appointment System API

The Hospital Appointment System API is a Django REST Framework (DRF) application designed to manage hospital appointments. It supports user registration, login, and appointment booking with role-based access for Patients, Doctors, and Admins. The API uses JWT authentication (djangorestframework-simplejwt) and is containerized with Docker for consistent development and deployment.

Table of Contents

- [Features](#features)
- [Technologies](#technologies)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
  - [Clone the Repository](#clone-the-repository)
  - [Environment Configuration](#environment-configuration)
  - [Docker Setup](#docker-setup)
  - [Apply Migrations](#apply-migrations)
  - [Create a Superuser](#create-a-superuser)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
  - [Authentication Endpoints](#authentication-endpoints)
  - [Protected Endpoints](#protected-endpoints)
- [Testing the API](#testing-the-api)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Features

- User registration and login with JWT authentication.
- Role-based access control (Patient, Doctor, Admin).
- Appointment management (create, view, update, delete).
- Doctor profiles and availability tracking.
- Secure API with token-based authentication.
- Dockerized setup for easy development and deployment.
- Browsable API interface via Django REST Framework.

## Technologies

- Backend: Django 4.2.11, Django REST Framework 3.15.2
- Authentication: djangorestframework-simplejwt 5.3.1
- Database: PostgreSQL 15
- Containerization: Docker, Docker Compose (v2.29.2)
- Dependencies: psycopg2-binary 2.9.9, python-decouple 3.8, gunicorn 22.0.0
- Python: 3.11 (used in Docker)

## Prerequisites

- Docker and Docker Compose (v2.29.2 or higher). [Install Docker](https://docs.docker.com/get-docker/).
- Git for cloning the repository.
- An API testing tool (e.g., Postman, curl, or a browser for the browsable API).
- Basic knowledge of Django, REST APIs, and Docker.

## Setup Instructions

**Clone the Repository**

Clone the project to your local machine:

```
git clone https://github.com/kihuni/hospital-appointment-system.git
cd hospital-appointment-system
```
**Environment Configuration**

Create a .env file in the project root with the following variables:

```
SECRET_KEY=your-secret-key-here
DEBUG=True
DB_NAME=hospital_db
DB_USER=hosi
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```
Generate a secure SECRET_KEY using a Python script:

```
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())

```

**Docker Setup**
The project uses Docker to manage the application (app) and database (db) services.

Verify Docker Installation:

```
docker --version
docker compose version
```

Ensure Docker Compose is v2.29.2 or higher. If using an older version, update it:

```
sudo apt update
sudo apt install docker.io docker-compose-v2
```

Build and Start Services:

```
docker compose up --build -d
```

This builds the app image, starts the PostgreSQL db service, and runs the Django server on http://localhost:8000.

Check Service Status:

```
docker compose ps
```
Ensure both app and db services are running.


_Apply Migrations_

Apply database migrations to create the necessary tables:

```
docker compose exec app python manage.py migrate
```
_Create a Superuser_

Create an admin user to access the Django admin panel (http://localhost:8000/admin):

```
docker compose exec app python manage.py createsuperuser
```

**Follow the prompts to set the username, email, and password.**

## Running the Application

Start Docker Services:

```
docker compose up -d
```
_Access the Application:_

- API Root: http://localhost:8000/api/

- Admin Panel: http://localhost:8000/admin/

- Browsable API: Use a browser or API client to explore endpoints.

_Stop Services:_

```
docker compose down
```

## API Endpoints

### Authentication Endpoints

These endpoints are accessible without authentication (AllowAny permission).

**Register a new user (default: Patient)**

- POST /api/register/ 

`{"username": "testuser", "email": "test@example.com", "password": "securepassword123", "first_name": "Test", "last_name": "User"}`

![image](https://github.com/user-attachments/assets/c9f78408-5afd-42a8-8d9e-840a46b39127)


**Log in and obtain JWT tokens**

- POST /api/login/

`{"username": "testuser", "password": "securepassword123"}`


**Refresh the JWT access token**

- POST /api/token/refresh/

`{"refresh": "<refresh_token>"}`

![image](https://github.com/user-attachments/assets/93c1e676-c66c-4c34-8cbc-88c8f0093201)



## Protected Endpoints

These endpoints require a JWT access token in the Authorization header (Bearer <access_token>).

**List or create roles**

- GET, POST /api/roles/

Admin only (custom permission)

Admin:

![image](https://github.com/user-attachments/assets/856345cf-5e75-46ba-ba31-ad6f9b45a60f)


Regular user:

![image](https://github.com/user-attachments/assets/bb869d53-db44-4ae5-af1b-3e3621f3e10a)


**List or create doctors**

- GET, POST /api/doctors/

Admin or Doctor
![image](https://github.com/user-attachments/assets/c8601ae3-e68d-452c-81fd-64a1cb1f7c2c)

**List or create appointments**

- GET, POST /api/appointments/

Authenticated users

List appointments

![image](https://github.com/user-attachments/assets/640c548d-22db-4ded-93a8-2196c29ec646)

create appointments

![image](https://github.com/user-attachments/assets/be675520-abc0-48e1-b910-2fdd6c39de44)


**Retrieve, update, or delete a role**

- GET, PUT, DELETE /api/roles/{id}/

Admin only

![image](https://github.com/user-attachments/assets/65816efd-2bc6-4ba9-93d7-31a1c7ba21cb)


## Testing the API

Use curl, Postman, or the DRF browsable API to test endpoints.
Register a User

```
curl -X POST http://localhost:8000/api/register/ \
-H "Content-Type: application/json" \
-d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "securepassword123",
    "first_name": "Test",
    "last_name": "User"
}'
```
Response (HTTP 201):

```
{
    "user": {
        "username": "testuser",
        "email": "test@example.com",
        "role": "PATIENT"
    },
    "message": "User registered successfully"
}
```
Login

```
curl -X POST http://localhost:8000/api/login/ \
-H "Content-Type: application/json" \
-d '{
    "username": "testuser",
    "password": "securepassword123"
}'
```
Response (HTTP 200):

```
{
    "access": "<access_token>",
    "refresh": "<refresh_token>",
    "user": {
        "username": "testuser",
        "email": "test@example.com",
        "role": "PATIENT"
    }
}
```
Access Protected Endpoint

```
curl -X GET http://localhost:8000/api/appointments/ \
-H "Authorization: Bearer <access_token>"
```
Refresh Token
```
curl -X POST http://localhost:8000/api/token/refresh/ \
-H "Content-Type: application/json" \
-d '{
    "refresh": "<refresh_token>"
}'
```










