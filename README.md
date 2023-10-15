# Reading Time Tracking System

Reading Time Tracking System is an API-based application developed using Django Rest Framework (DRF). 
It allows users to track the time they spend reading books. Users can start and end reading sessions, 
and the system saves the duration of each session as well as the total reading time for each book. 
The system also provides statistics for users, including total reading time over the last 7 and 30 days.

## Features

* JWT authentication.
* Admin panel at /admin/
* Documentation at /api/doc/swagger/
* Books management at /api/books/
* User creation at /api/users/register/
* User profile management at /api/users/profile/
* Reading sessions management.
* Scheduled collecting user reading statistics with Celery and Redis.
* Docker-compose support for easy deployment.
* Pytest tests for ensuring code quality and reliability.

## Installation & Getting started

Python 3.10 must be already installed.

1. Clone project and create virtual environment.
    ```shell
    git clone https://github.com/arsenmakovei/reading-time.git
    cd reading_time
    python -m venv venv
    Windows: venv\Scripts\activate
    Linux, Unix: source venv/bin/activate
    pip install -r requirements.txt
    ```

2. Create .env file and set environment variables. 
For Docker, you can use environment variables from .env.sample.
You can also use SQLite instead of PostgreSQL if you want 
to run it manually; it is not configured to run in Docker.

    ```shell
    DJANGO_SECRET_KEY=<your Django secret key>
    POSTGRES_HOST=<your Postgres db host>
    POSTGRES_DB=<your Postgres db name>
    POSTGRES_USER=<your Postgres db user>
    POSTGRES_PASSWORD=<your Postgres db password>
    CELERY_BROKER_URL=<your Celery broker url>
    CELERY_RESULT_BACKEND=<your Celery result backend url>
    ```

3. Make migrations and run server.
    ```shell
    python manage.py migrate
    python manage.py loaddata reading_time_data.json # Load test data if you want.
    python manage.py runserver
    ```
4. If you loaded test data or ran the server in Docker, you can use the demo user:
    ```shell
    Email: admin@admin.com
    Password: admin
    ```
5. Run a periodic task that calculates the total reading time 
for the last 7 and 30 days and saves it in the user's profile.
   * Run Redis server.
   * In separate terminals, run commands: `celery -A reading_time worker -l INFO` 
   and `celery -A reading_time beat -l INFO`

6. Also, you can run pytest tests using command `pytest`

## Run with Docker

Docker should be installed and running

```shell
docker-compose up --build
```

