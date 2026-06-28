# Nebula Architecture

## Project Overview

Nebula is a lightweight announcement board and personal publishing platform built with FastAPI, SQLModel, PostgreSQL and Jinja2.

The project focuses on simplicity, readability and elegant visual presentation.

Unlike traditional CMS systems, Nebula aims to provide a clean information publishing experience suitable for:

* Personal blogs
* Team announcement boards
* Internal dashboards
* Community notice systems

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
* Nginx (future)

---

## Current Architecture

Browser

↓

FastAPI Router

↓

Service Layer

↓

SQLModel

↓

PostgreSQL

---

## Directory Structure

app/

├── config/

├── models/

├── routers/

├── schemas/

├── services/

└── utils/

### config

Application configuration.

Examples:

* settings.py
* database.py

### models

Database entities.

Examples:

* Notice

### schemas

Pydantic request and response models.

Examples:

* NoticeCreate
* NoticeRead

### services

Business logic layer.

Examples:

* create_notice()
* get_all_notices()

### routers

HTTP route handlers.

Examples:

* board.py
* notice.py

### utils

Utility functions.

Examples:

* generate_slug()

---

## Implemented Features

### Board Hall

Display all published notices.

Features:

* Priority badge
* Category badge
* Pin support
* Time display

### Notice Creation

Create notices through web form.

Workflow:

User Input

↓

POST /notice/new

↓

Service Layer

↓

Database

↓

Redirect Home

---

## Database Design

Table: notices

Fields:

* id
* title
* slug
* content
* category
* priority
* pinned
* published
* created_at
* updated_at

---

## Development Principles

### Thin Router

Routers should only handle:

* Request
* Response
* Dependency Injection

Business logic belongs in services.

### Service First

Database operations should be placed inside services.

Avoid direct SQL queries in routers.

### Reusable Templates

Shared UI components:

* navbar.html
* base.html

Future components:

* card.html
* pagination.html

---

## Current Status

Version: 0.1

Completed:

✓ PostgreSQL Integration

✓ Notice Model

✓ Create Notice

✓ Notice Listing

✓ Dark Mode

✓ Glass UI

Planned:

□ Notice Detail

□ Edit Notice

□ Delete Notice

□ Markdown Support

□ Pagination

□ Authentication

□ Public API

