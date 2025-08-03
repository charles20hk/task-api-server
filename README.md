# task-api-server
A simple API server to manages tasks

# Prerequisites

The server or machine requires python 3.12 or above.

[Optional] Poetry is installed on the machine for better testing or running the application.

# How to run the application locally

1. Download the package to localhost, create an virtual env and activate it
 
2. install the required packages, run the following command 

```
poetry install
```

3. run the application

```
poetry run python -m app.web.main
```

or

```
make run-server
```

# Example API requests

**You can also find the API specification on the running application, http://127.0.0.1:8080/docs**

1. Create a task, POST /tasks

Body
```
{
    "title": "some title",
    "description": "some desc",
    "priority": 1,
    "due_date": "2000-01-30T15:00:00"
}
```

2. Update a task, PUT /tasks/:id

Body
```
{
    "title": "updated title",
    "priority": 2
}
```

3. Get the tasks (with/o params), GET /tasks?completed=false&priority=1

4. Get a task by ID, GET /tasks/:id

5. Delete a task, DELETE /tasks/:id

# Run the tests

All the test commands (format check, lint check, unit tests, integration tests) are all include in Makefile,

To run all the checks and tests,

```
make build
```

or refer to the Makefile for individual run.

# Run the appliction in docker

```
docker compose up --build -d
```
