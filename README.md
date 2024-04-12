![Lint-free](https://github.com/nyu-software-engineering/containerized-app-exercise/actions/workflows/lint.yml/badge.svg)
![Passing-Tests](https://github.com/nyu-software-engineering/containerized-app-exercise/actions/workflows/unit-tests.yml/badge.svg)

# Containerized App Exercise

The Containerized App Exercise is a project aimed at building a containerized application consisting of multiple subsystems, each operating within its own Docker container. The project includes:

- **Machine Learning Client**: TODO
- **Web App**: A Flask-based Web App that captures an image from the user's camera and places the data in the databse.
- **Database**: A local MongoDB database used by both the machine learning client and the web app to store and retrieve data.

## Instructions

The App Uses [docker-compose](https://docs.docker.com/compose/) to build the three docker containers necessary. To build, run
```bash
docker compose up
```
from the project root.

### [Pytest](https://docs.pytest.org/en/stable/)

To run tests using pytest, run:

```bash
pytest
```
or for the Dockerized version
```bash
docker build -t test-image -f PytestDockerfile .
docker run test-image
```
from the project root

## Teammates

* [Corina Luca](https://github.com/CorinaLucaFocsan)
* [Jakob Hablitz](https://github.com/jsh9965)
* [Josckar Palomeque-Elias](https://github.com/josckar)
* [Stella Zhang](https://github.com/qq3173732005)
