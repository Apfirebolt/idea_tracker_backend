# Idea Tracker Backend API

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)
![NodeJS](https://img.shields.io/badge/node.js-6DA55F?style=for-the-badge&logo=node.js&logoColor=white)
![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)
![Postgres](https://img.shields.io/badge/Postgres-316192?style=for-the-badge&logo=postgresql&logoColor=white)

## Tech Stack

- FastAPI
- PostGres
- Swagger
- Docker

## Introduction

Idea tracker app API which would be used to generate ideas, create tasks associated with those ideas. Additional features like segregation of ideas based on category would also be possible.

## Updates

- Any updates in the project would be added in future

## Screenshots

Any screenshots of the APIs go here

## Deployment using Docker containers

```sh
$ docker-compose up -d --build
$ docker-compose exec web alembic upgrade head
```

## Alembic

```
alembic revision --autogenerate -m "Initial tables"
```

```
alembic upgrade head
```

```
pip install 'pydantic[email]'
```

### Steps to clean database

```
rm alembic/versions*.py
```

This would remove all the migration files inside the Alembic folder. Then, you can delete the tables in the database and start fresh.

```
 alembic revision --autogenerate -m "initial migrations added"
```
