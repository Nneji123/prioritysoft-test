# Priority Store
| Category | Badges |
| --- | --- |
| CI/CD | [![tests](https://github.com/Nneji123/prioritysoft-test/actions/workflows/tests.yml/badge.svg)](https://github.com/Nneji123/prioritysoft-test/actions/workflows/tests.yml) [![codecov](https://codecov.io/gh/Nneji123/prioritysoft-test/graph/badge.svg?token=PmwZ7zM9xC)](https://codecov.io/gh/Nneji123/prioritysoft-test) ![Docker](https://img.shields.io/badge/Docker-blue?style=flat&logo=docker&logoColor=white) |
| Meta | [![Language](https://img.shields.io/badge/Python-3.8-blue.svg?style=flat&logo=python&logoColor=white)](https://www.python.org) [![Framework](https://img.shields.io/badge/Django-darkgreen.svg?style=flat&logo=django&logoColor=white)](https://www.djangoproject.com/) [![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![isort](https://img.shields.io/badge/code%20style-isort-000000.svg)](https://pycqa.github.io/isort/) [![Ruff](https://img.shields.io/badge/linter-ruff-000000.svg)](https://github.com/charliermarsh/ruff) [![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit) [![Gitpod](https://img.shields.io/badge/Gitpod-ready--to--code-ff69b4?logo=gitpod&logoColor=white)](https://gitpod.io/) [![License - MIT](https://img.shields.io/badge/license-MIT-9400d3.svg)](./LICENSE) |




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
prioritysoft-test/
.
├── LICENSE
├── Makefile
├── README.md
├── apps
│   ├── __init__.py
│   ├── accounts
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── managers.py
│   │   ├── migrations
│   │   ├── mixins.py
│   │   ├── models.py
│   │   ├── schema.py
│   │   ├── serializers.py
│   │   ├── tasks.py
│   │   ├── templates
│   │   ├── throttles.py
│   │   ├── urls.py
│   │   ├── utils.py
│   │   └── views.py
│   ├── core
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── management
│   │   ├── middlewares.py
│   │   ├── migrations
│   │   ├── templates
│   │   └── utils.py
│   └── inventory
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── migrations
│       ├── models.py
│       ├── pagination.py
│       ├── permissions.py
│       ├── schema.py
│       ├── serializers.py
│       ├── signals.py
│       ├── tasks.py
│       ├── templates
│       ├── urls.py
│       ├── utils.py
│       └── views.py
├── compose.yml
├── data
│   ├── cert.pem
│   ├── csr.pem
│   ├── key.pem
├── docker
│   ├── Dockerfile.dev
│   ├── Dockerfile.prod
│   ├── requirements.development.txt
│   └── requirements.production.txt
├── docs
│   └── code_samples
│       └── accounts
├── manage.py
├── requirements.txt
├── scripts
│   ├── deploy.sh
│   └── entrypoint.sh
├── store
│   ├── __init__.py
│   ├── asgi.py
│   ├── celery.py
│   ├── settings
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   └── wsgi.py
├── tests
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_accounts
│   ├── test_core
│   └── test_inventory
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
git clone https://github.com/nneji123/prioritysoft-test.git
cd prioritysoft-test
```

#### Environment Variables

Create a `.env` file in the root directory and add the necessary environment variables. Refer to `.env.sample` for guidance.

#### Using Docker

Build and run the containers:

```sh
docker build -t my_image_name /docker/Dockerfile.dev
docker run -d --name my_container_name my_image_name
```

For production:

```sh
docker build -t my_image_name /docker/Dockerfile.prod
docker run -d --name my_container_name my_image_name

```

#### Using Docker Compose

Build and run the containers:

```sh
docker compose up --build
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


You can use Gitpod, a free online VS Code-like environment, to quickly start contributing.

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/nneji123/prioritysoft-test)

### Running with CodeSpaces

To run the project in GitHub Codespaces:

1. Open the repository in Codespaces.
2. Codespaces will set up the environment and start the development server.

## Testing

To run the tests:

```sh
pip install pytest pytest-mock pytest-celery pytest-cov pytest-django
DJANGO_SETTINGS_MODULE=store.settings.development pytest --cov=apps tests --cov-report=xml
```

Coverage reports will be generated by Codecov.

### Setting Up Pre-Commit Hooks

We use `pre-commit` to ensure code quality. Install it by running:

```bash
pip install pre-commit
pre-commit install
```

Now, `pre-commit` will run automatically before each commit to check for linting and other issues.


## OpenAPI Documentation

This project includes extensive API documentation generated with drf-spectacular. You can access the Swagger UI and Redoc documentation at the following endpoints:

- Swagger UI: `/swagger/`
- Redoc: `/docs/`

### Adding Images

<details>
<summary>Swagger UI</summary>
<img src=".github/images/Screenshot%20(694).png" alt="Swagger UI">
<img src=".github/images/Screenshot%20(695).png" alt="Swagger UI2">
</details>

<details>
<summary>Redoc UI</summary>
<img src=".github/images/Screenshot%20(698).png" alt="Redoc UI">
<img src=".github/images/Screenshot%20(699).png" alt="Redoc UI">
</details>

## Mailpit UI

<details>
<summary>Mailpit UI</summary>
<img src=".github/images/Screenshot%20(696).png" alt="Mailpit UI">
<img src=".github/images/Screenshot%20(697).png" alt="Mailpit UI">
</details>


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

Mailpit is used for email testing. The `.pem` files required for Mailpit to start are located in the `data` directory.

## Contributing

Contributions are welcome! Please follow the guidelines below:

### Submitting a Pull Request

1. Fork the repository and create a new branch for your contribution:

    ```bash
    git checkout -b feature-or-fix-branch
    ```

2. Make your changes, run tests and commit them:

    ```bash
    git add .
    git commit -am "Your meaningful commit message"
    ```

3. Push the changes to your fork:

    ```bash
    git push origin feature-or-fix-branch
    ```

4. Open a pull request on GitHub. Provide a clear title and description of your changes.

## License

This project is licensed under the MIT License.
