# 3B Store Project

This repository contains the source code and necessary configuration for the development of the 3B Store application. Follow the steps below to set up and run the development environment.

## Prerequisites

Make sure you have Docker Desktop installed on your system. You can download it from the following link: [Download Docker Desktop](https://docs.docker.com/compose/install/#scenario-one-install-docker-desktop)

## Setting up the Development Environment

Once you have Docker Desktop installed, follow these steps to set up the development environment:

1. Create a virtual environment by running the following command (STEP 1 - 3 ONLY FOR WARNING CODES ON EDITOR):

    ```bash
    py -m venv venv
    ```
2. Activate the virtual environment. For example, on macOS, use:

    ```bash
    source venv/bin/activate
    ```

3. Install the required libraries by running:

    ```bash
    pip install -r ./requirements.txt
    ```

## Building and Running

To build the container, make sure you are in the root directory of the project and run:

```bash
docker-compose build
```

#### **Note:** The container creation process might take some time as it generates images for PostgreSQL, Redis, Celery worker, Celery beat, MongoDB, and Django. This also results in a download of approximately 250mb for the PostgreSQL, MongoDB, and Redis images.

To run the container, use the following command:

```bash
docker-compose up
```

Please note that it might take a little while for the Django application to fully start up. This is because Django waits for a connection to PostgreSQL before running makemigrations and migrate to set up the database schema.

## Restore Database

The project includes a preloaded backup. To restore it, make sure you are in the root directory of the project and run:

```bash
docker exec -i 3b_store_db psql -U postgres -d Store < ./compose/local/backup.sql
```

The backup includes 10 preloaded products and two users:

### Administrator User
- **Username:** corack
- **Password:** pass123

### Regular User
- **Username:** mortel
- **Password:** pass123

### Administrator Permissions:
- Access to update and delete products.
- Add inventory to a product.
- View and update all users.
- View all orders.

### Regular User Permissions:
- Create an order.
- View only their own orders.
- View and update their own user information.

## Connecting to PostgreSQL

If you wish to connect to the PostgreSQL instance:

- **Host:** localhost
- **Port:** 5433
- **Database:** Store
- **Username:** postgres
- **Password:** postgres123

## Connecting to MongoDB

If you wish to connect to the MongoDB instance:

- **Host:** localhost
- **Port:** 27018
- **Database:** Store
- **Username:** mongo
- **Password:** mongo123


## Running Tests

If you want to run the tests, first ensure that PostgreSQL and MongoDB containers are running. Then build the container (if you haven't already) and use the following command:

```bash
docker compose run --rm app pytest -s
```

Now you are ready to start developing and testing the 3B Store application!