# Nebula

A lightweight publishing platform built with FastAPI, SQLModel, PostgreSQL and Jinja2.

Nebula focuses on simplicity, readability and maintainability. It provides a clean content publishing experience suitable for personal blogs, team announcement boards and internal knowledge sharing.

---

## Features

### Notice Management

* Create Notice
* Notice List
* Notice Detail
* Edit Notice
* Soft Delete
* Markdown Rendering

### Content Enhancement

* Pagination
* Search

### User System

* User Registration
* User Login
* User Logout
* Session Authentication

### User Interface

* Dark Mode
* Glass UI
* Responsive Layout

### Database

* PostgreSQL
* Alembic Migration
* SQLModel ORM

---

## Technology Stack

### Backend

* FastAPI
* SQLModel
* SQLAlchemy Async
* PostgreSQL
* asyncpg

### Frontend

* Jinja2 Templates
* TailwindCSS
* Vanilla JavaScript

### Deployment

* Debian Linux
* Uvicorn

---

## Project Structure

```text
app/
├── config/
├── dependencies/
├── models/
├── routers/
├── schemas/
├── services/
└── utils/

templates/
static/
docs/
alembic/
```

---

## Installation

Create virtual environment:

```bash
uv venv
source .venv/bin/activate
```

Install dependencies:

```bash
uv sync
```

Configure environment variables:

```bash
DATABASE_URL=postgresql+asyncpg://user:password@localhost/nebula
SECRET_KEY=your-secret-key
```

Run database migration:

```bash
alembic upgrade head
```

Start application:

```bash
uv run python main.py
```

---

## Status

Version: 1.0

Status: Stable Release

Current development mode:

Maintenance

