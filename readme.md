Here is the translated text:

---

# Khanto Reservations

## What is it? 🤔

This project consists of creating a REST application with 3 main resources: Properties, Listings, and Reservations. It was developed as part of the practical test for the developer position at Seazone.

## Tools 🛠️

The project was developed using Django and DRF frameworks for application creation, along with some of their internal tools for functionalities like unit tests and fixture loading. For package and dependency management, Poetry was used instead of Pipenv or similar tools, considering the latest performance results obtained in comparison.

## How to Run? 🚀

### Prerequisites 📋

- Python 3.10
- Poetry
- PostgreSQL Database

### Installation 🔧

After installing the prerequisites, clone the repository and install the dependencies with Poetry:

```bash
$ poetry install
# Activate the virtual environment (optional)
$ poetry shell
# If activated, 'poetry run' is not needed for subsequent commands
```

### Configuration 🔧

Create a .env file in the root of the project with the following variables:

```bash
SECRET_KEY= # Django secret key
DATABASE_URL= # Database connection URL (e.g., postgres://user:password@host:port/database)
```

### Migrations and Fixtures 🗃️

To create the tables in the database and load the initial data, run the following commands:

```bash
$ poetry run python manage.py migrate

$ poetry run python manage.py loaddata khanto/apps/properties/fixtures/fixture_properties_announcements.json

$ poetry run python manage.py loaddata khanto/apps/reservations/fixtures/fixture_reservations.json
```

### Running Tests 🧪

To run the tests, execute the following commands:

```bash
$ poetry run python manage.py test properties
$ poetry run python manage.py test reservations
```

### Running the Application 🚀

To run the project, use the following command:

```bash
$ poetry run python manage.py runserver
```

## Documentation 📃

The endpoint documentation was created with Swagger and is available at the `/swagger` route.

## Next Steps 📌

- Complete the frontend started with Vue and Buefy
- Deploy on the personal AWS Lightsail instance
- Dockerize the application
