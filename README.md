# Priority Store
| | |
| --- | --- |
| CI/CD | [![CI - Test](https://github.com/Nneji123/ycombinator-scraper/actions/workflows/tests.yml/badge.svg)](https://github.com/Nneji123/ycombinator-scraper/actions/workflows/tests.yml)  [![codecov](https://codecov.io/gh/Nneji123/prioritysoft-test/graph/badge.svg?token=PmwZ7zM9xC)](https://codecov.io/gh/Nneji123/prioritysoft-test)|
| Package | [![PyPI - Version](https://img.shields.io/pypi/v/ycombinator-scraper.svg?logo=pypi&label=PyPI&logoColor=gold)](https://pypi.org/project/ycombinator-scraper/) [![PyPI - Downloads](https://img.shields.io/pypi/dm/ycombinator-scraper.svg?color=blue&label=Downloads&logo=pypi&logoColor=gold)](https://pypi.org/project/ycombinator-scraper/) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ycombinator-scraper.svg?logo=python&label=Python&logoColor=gold)](https://pypi.org/project/ycombinator-scraper/) |
| Meta |  [![linting - Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff) [![License - MIT](https://img.shields.io/badge/license-MIT-9400d3.svg)](./LICENSE) |

Priority Store is a Django Rest Framework project designed to manage the inventory of items and suppliers efficiently. This project includes various features such as a custom user model, Celery for task handling, Docker for containerization, and more. This documentation provides an extensive overview of the project's structure, setup, and usage.

## Features

- **Custom User Model**: A tailored user model to meet specific authentication needs.
- **Celery**: Handles asynchronous tasks such as password reset emails and supplier notification emails.
- **Pre-commit Hooks**: Configured with `black` and `isort` to ensure code quality and consistency.
- **Makefile**: Simplifies common tasks and commands.
- **Docker Compose**: Supports multiple environments (production and development).
- **Separated Settings**: Different settings for development and production environments.
- **Automated Tests**: Uses GitHub Actions, `pytest`, and `codecov` for continuous integration and code coverage.
- **Modular Apps Structure**: Enhances code modularity and maintainability.
- **OpenAPI Documentation**: Provides extensive API documentation using Swagger and Redoc with drf-spectacular.
- **Custom Admin Interface**: Utilizes Django admin interface package for a customized admin experience.
- **Staticfiles Hosting**: Uses Whitenoise for serving static files.
- **Postgres and Redis Services**: Facilitates easy setup with Docker.
- **Mailpit**: Email testing functionality with visual representation of Mailpit UI.

## Project Structure

```
priority-store/
├── apps/
│   ├── inventory/
│   ├── core/
│   └── accounts/
├── store/
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   └── wsgi.py
├── data/
│   ├── *.pem # These files are required for Mailpit 
├── tests/
│   ├── __init__.py
│   ├── test_inventory.py
│   ├── test_suppliers.py
│   └── test_users.py
├── Dockerfile
├── compose.yml
├── Makefile
├── manage.py
├── README.md
└── requirements.txt
```

## Apps Overview

### Core

The **Core** app contains essential functions and utilities that are shared across the project. These include:

- **Middlewares**: Custom middlewares for request processing.
- **Templates**: Base templates for rendering views.
- **Management Commands**: Custom Django management commands for various administrative tasks.

### Accounts

The **Accounts** app manages user-related functionality, including:

- **Admins**: Users with full access to the system.
- **Employees**: Users who can perform operations on items but can only view supplier information without modification rights.
- **Models**: Defines user roles and permissions.
- **Views**: Manages the API endpoints for user operations.
- **Serializers**: Transforms user data for API responses.
- **Permissions**: Defines access control logic for different user roles.

### Inventory

The **Inventory** app handles the management of items and suppliers:

- **Items**: Products that can have multiple suppliers.
- **Suppliers**: Entities that provide items.
- **Models**: Defines the schema for items and suppliers.
- **Views**: Manages the API endpoints for inventory operations.
- **Serializers**: Transforms inventory data for API responses.
- **Permissions**: Defines access control logic for item and supplier operations.



## Getting Started

### Prerequisites

- Docker
- Docker Compose
- Git
- Python 3.8+ 

### Setup

#### Clone the Repository

```sh
git clone https://github.com/nneji123/priority-store.git
cd priority-store
```

#### Environment Variables

Create a `.env` file in the root directory and add the necessary environment variables. Refer to `.env.sample` for guidance.

#### Using Docker

Build and run the containers:

```sh
docker build -t my_image_name "path to file"
```

For production:

```sh
docker compose -f docker-compose.prod.yml up --build
```

#### Using Docker Compose

Build and run the containers:

```sh
docker compose up --build
```

For production:

```sh
docker compose -f docker-compose.prod.yml up --build
```

#### Using Makefile

To run the project using Makefile:

```sh
make start
```

#### Using Python Commands

If you prefer not to use Docker, you can set up the project with Python:

1. Install dependencies:

```sh
pip install -r requirements.txt
```

2. Apply migrations:

```sh
python manage.py migrate
```

3. Run the development server:

```sh
python manage.py runserver
```

### Running with Gitpod

To run the project in Gitpod:

1. Open the repository in Gitpod.
2. Gitpod will automatically set up the environment and start the development server.

### Running with CodeSpaces

To run the project in GitHub Codespaces:

1. Open the repository in Codespaces.
2. Codespaces will set up the environment and start the development server.

## Testing

To run the tests:

```sh
pytest tests
```

Coverage reports will be generated by Codecov.

## Pre-commit Hooks

Ensure your code meets quality standards by setting up pre-commit hooks:

```sh
pip install pre-commit
pre-commit install
```

## OpenAPI Documentation

This project includes extensive API documentation generated with drf-spectacular. You can access the Swagger UI and Redoc documentation at the following endpoints:

- Swagger UI: `/swagger/`
- Redoc: `/redoc/`

### Adding Images

![Swagger UI](path_to_swagger_image)

![Redoc UI](path_to_redoc_image)

## Mailpit UI

![Mailpit UI](path_to_mailpit_image1)

![Mailpit UI](path_to_mailpit_image2)

## Custom Admin Interface

This project includes a custom admin interface using Django admin interface package. You can access the admin panel at `/admin/`.

## Static Files

Static files are served using Whitenoise. Ensure your static files are collected:

```sh
python manage.py collectstatic
```

## Services

### Postgres

Postgres is used as the database service. It is configured in the Docker Compose files.

### Redis

Redis is used as a message broker for Celery tasks. It is also configured in the Docker Compose files.

### Mailpit

Mailpit is used for email testing. The `.pen` files required for Mailpit to start are located in the `data` directory.

## Contributing

Contributions are welcome! Please follow the guidelines below:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Make your changes.
4. Ensure all tests pass.
5. Submit a pull request.

## License

This project is licensed under the MIT License.

---


# TODO:
- Add Logging Statements
- Update Documentation 
- Record Video
- Add tests