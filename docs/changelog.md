# Changelog

## 2026-06-28

### Notice Detail

Added:

* notice_detail.html
* get_notice_by_slug()

Updated:

* board.html
* notice.py

Result:

Create → List → Detail workflow completed.

---

## 2026-06-29

### Notice Edit & Soft Delete

Added:

* Notice Edit
* Shared Create/Edit Form
* Soft Delete Support

Updated:

* notice.py
* notice_service.py
* notice_form.html

Result:

Notice CRUD workflow completed.

Features:

* Create
* List
* Detail
* Edit
* Soft Delete

---

## 2026-06-30

### Pagination & Search

Added:

* Notice Pagination
* Search Bar
* Search Result Filtering

Updated:

* board.py
* notice_service.py
* board.html

Result:

Notice browsing experience improved.

Features:

* Pagination
* Search

---

### User System

Added:

* User Model
* User Registration
* User Login
* User Logout
* Session Authentication

Added Files:

* user.py
* user_service.py
* security.py
* auth.py

Result:

Nebula now supports authenticated users.

Features:

* Register
* Login
* Logout
* Session Authentication

---

## 2026-07-01

### Nebula v1.0 Release

Added:

* Stable User System
* PostgreSQL Migration Workflow
* Authentication Dependency Layer
* Search & Pagination Integration

Architecture:

* Router Layer
* Dependency Layer
* Service Layer
* SQLModel ORM Layer

Result:

Nebula reached stable release status.

Status:

v1.0 Stable Release

