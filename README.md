# Django Starter Template

A production-ready Django REST API backend designed to pair with the
[Flutter Starter Template](https://github.com/sahil-shefeek/flutter-starter-template).

## Features

- **Django 4.2+ REST API** with comprehensive endpoint coverage
- **Authentication and Authorization**
  - JWT Authentication
  - OAuth support via django-allauth
  - Registration, login, password reset flows
- **Task Processing (coming soon)**
  - Background job processing with Celery
  - Task result storage
- **Documentation**
  - Auto-generated OpenAPI/Swagger documentation via drf-spectacular
- **Storage**
  - Flexible file storage with django-storages
- **Developer Experience**
  - Environment variable configuration
  - CORS support for frontend development
- **Database**
  - PostgreSQL support
  - SQLite support for development and testing

## Prerequisites

- Python 3.8+
- PostgreSQL
- SQLite (for development and testing)

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/sahil-shefeek/django-for-flutter-starter-template.git
cd django-starter
```

### 2. Create and activate virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

A `.env.example` file is provided in the project root as a template. Copy it to
create your own `.env` file:

```bash
cp .env.example .env
```

Then edit the `.env` file to replace the placeholder values with your actual
configuration:

- **Django Core Settings**
  - `SECRET_KEY`: Generate a secure random string
  - `DEBUG`: Set to `False` in production
  - `ALLOWED_HOSTS`: Comma-separated list of allowed hostnames

- **Database Configuration**
  - Update with your PostgreSQL database credentials
  - For development, you can use the default values or SQLite

- **OAuth Settings**
  - Set up a Google OAuth application and add your credentials
  - Make sure the callback URL matches your frontend URL

- **CORS Settings**
  - Add your frontend URLs to allow cross-origin requests

- **Email Settings**
  - Configure SendGrid or another email provider for sending emails
  - Required for password reset and email verification functions

- **Frontend URL**
  - Set this to your frontend application URL for email verification links

### 5. Run database migrations

```bash
python manage.py migrate
```

### 6. Create superuser

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

## API Documentation

When the server is running, API documentation is available at:

- Swagger UI: `/api/schema/swagger-ui/`
- ReDoc: `/api/schema/redoc/`
- OpenAPI Schema: `/api/schema/`

## Integration with Flutter Starter Template

This backend is designed to work seamlessly with the
[Flutter Starter Template](https://github.com/sahil-shefeek/flutter-starter-template).
The API endpoints match the expected routes and authentication mechanisms used
by the Flutter app.

Key integrations:

- JWT-based authentication
- RESTful API endpoints for all app features
- Matching data models and serialization formats
- File upload capabilities for media content

## Deployment

### Using Docker

Coming soon!

### Traditional Deployment

For traditional deployment, follow these steps:

1. Set up a production PostgreSQL database
2. Set up Gunicorn with Nginx or Apache
3. Configure environment variables for production
4. Run migrations
5. Collect static files

```bash
python manage.py collectstatic
gunicorn myproject.wsgi:application
```

## User Schema

The user schema includes the following fields:

- `id`: Primary key
- `username`: Unique username
- `email`: Unique email address
- `password`: Hashed password
- `first_name`: First name
- `last_name`: Last name
- `is_active`: Boolean indicating if the user is active
- `is_staff`: Boolean indicating if the user is a staff member
- `date_joined`: Date and time when the user joined

## Email Configuration

To configure email settings, update the following environment variables in your
`.env` file:

- `EMAIL_BACKEND`: Email backend to use (e.g.,
  `django.core.mail.backends.smtp.EmailBackend`)
- `EMAIL_HOST`: SMTP server host
- `EMAIL_PORT`: SMTP server port
- `EMAIL_USE_TLS`: Whether to use TLS (True or False)
- `EMAIL_USE_SSL`: Whether to use SSL (True or False)
- `EMAIL_HOST_USER`: SMTP server username
- `EMAIL_HOST_PASSWORD`: SMTP server password
- `DEFAULT_FROM_EMAIL`: Default email address to use for outgoing emails

```
```
