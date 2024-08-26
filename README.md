# Django Project Setup and Run Guide

## Table of Contents
2 [Installation](#installation)
4. [Environment Setup](#environment-setup)
5. [Database Setup](#database-setup)
6. [Running the Project](#running-the-project)
7. [Static Files](#static-files)
8. [Running Tests](#running-tests)
9. [Deployment](#deployment)
10. [Troubleshooting](#troubleshooting)


## Prerequisites
Before you begin, ensure you have met the following requirements:

- **Python 3.8+**: Make sure Python is installed on your system. You can download it from [python.org](https://www.python.org/).
- **Pip**: Python package manager. It typically comes with Python but can be installed separately.
- **Virtualenv**: It's a good practice to create a virtual environment for your project.

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/yourprojectname.git
    cd yourprojectname
    ```

2. **Create and activate a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages**:
    ```bash
    pip install -r requirements.txt
    ```

## Environment Setup

1. **Create a `.env` file** in the root directory of the project:
    ```bash
    touch .env
    ```

2. **Add the following environment variables** to the `.env` file:
    ```env
    DEBUG=True
    SECRET_KEY=your-secret-key
    ALLOWED_HOSTS=localhost,127.0.0.1
    DATABASE_URL=postgres://USER:PASSWORD@HOST:PORT/DBNAME  # If using PostgreSQL
    ```

   Replace the values with your actual settings.

## Database Setup

1. **Run migrations** to set up the database schema:
    ```bash
    python manage.py migrate
    ```

2. **Create a superuser** for accessing the Django admin:
    ```bash
    python manage.py createsuperuser
    ```

3. **Load initial data** if any fixtures are provided (optional):
    ```bash
    python manage.py loaddata initial_data.json
    ```

## Running the Project

1. **Start the development server**:
    ```bash
    python manage.py runserver
    ```

   The project will be available at `http://127.0.0.1:8000/`.

## Static Files

1. **Collect static files** for production:
    ```bash
    python manage.py collectstatic
    ```

## Running Tests

1. **Run the test suite**:
    ```bash
    python manage.py test
    ```

## Deployment

For deployment, make sure to:

1. Set `DEBUG=False` in your `.env` file.
2. Set `ALLOWED_HOSTS` to your domain or IP address.
3. Configure a production-level database, such as PostgreSQL.
4. Use a production server like Gunicorn, and serve static files with Nginx.

Example commands for production:

```bash
pip install gunicorn
gunicorn assessment.wsgi:application --bind 0.0.0.0:8000
