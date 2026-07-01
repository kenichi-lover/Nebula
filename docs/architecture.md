# Nebula Architecture

## Project Overview

Nebula is a lightweight publishing platform built with FastAPI, SQLModel and PostgreSQL.

The project follows a simple layered architecture designed for long-term maintainability.

Suitable for:

* Personal Blogs
* Team Announcement Boards
* Internal Dashboards
* Community Publishing Systems

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

## Application Architecture

```text
Browser
    ↓
FastAPI Router
    ↓
Dependency Layer
    ↓
Service Layer
    ↓
SQLModel
    ↓
PostgreSQL
```

---

## Directory Structure

```text
app/

├── config/
│   ├── settings.py
│   └── database.py
│
├── dependencies/
│   └── auth.py
│
├── models/
│   ├── notice.py
│   └── user.py
│
├── schemas/
│   ├── notice.py
│   └── user.py
│
├── services/
│   ├── notice_service.py
│   └── user_service.py
│
├── routers/
│   ├── board.py
│   ├── notice.py
│   └── auth.py
│
└── utils/
    ├── slug.py
    ├── security.py
    ├── jwt.py
    ├── pagination.py
    └── md_renderer.py
```

---

## Database Design

### User

```text
id
username
email
hashed_password
full_name
avatar_url
is_active
is_superuser
created_at
updated_at
```

### Notice

```text
id
title
slug
content
category
priority
pinned
published
deleted
created_at
updated_at
```

---

## Data Relationship

```text
User
 └──< Notice

1 User
N Notices
```

---

## Development Principles

### Thin Router

Routers should only handle:

* Request
* Response
* Dependency Injection

Business logic belongs in services.

---

### Service First

Database operations belong in services.

Avoid direct SQL queries inside routers.

---

### Reusable Components

Shared templates:

* base.html
* navbar.html

Shared utilities:

* pagination.py
* security.py
* slug.py
* md_renderer.py

---

## Implemented Features

### Notice System

* Create Notice
* Notice List
* Notice Detail
* Edit Notice
* Soft Delete

### Content Features

* Markdown Rendering
* Pagination
* Search

### User System

* Registration
* Login
* Logout
* Session Authentication

### User Interface

* Dark Mode
* Glass UI

### Database

* PostgreSQL
* Alembic Migration

---

## Current Status

Version: 1.0

Status: Stable Release

Development Mode:

Maintenance

