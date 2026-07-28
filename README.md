# Multi-Tenant CRM Backend System

A secure and scalable multi-tenant CRM backend API built using Django REST Framework and PostgreSQL.

The system allows multiple organizations (tenants) to use the application while keeping their data completely isolated. Each user can belong to one or more organizations with different roles and permissions.

---

## Features

### Authentication
- User registration
- JWT-based authentication
- Access and refresh tokens
- Logout functionality
- Change password

### Multi-Tenancy
- Organization-based data isolation
- Users can belong to multiple organizations
- Role-based access control
- Prevent unauthorized access between organizations

### CRM Features

#### Customer Management
- Create customers
- Update customer information
- Delete customers
- View organization-specific customers

#### Task Management
- Create tasks
- Assign tasks to organization members
- Track task status
- Role-based task visibility

### Authorization
Implemented using role-based access control:

Roles:
- Owner
- Manager
- Staff

Permissions:
- Owners have full organization access
- Managers can manage organization resources
- Staff have limited access

---

# Tech Stack

Backend:
- Python 
- Django
- Django REST Framework

Database:
- PostgreSQL 16

Authentication:
- JWT Authentication

Documentation:
- Swagger / OpenAPI

Containerization:
- Docker
- Docker Compose

---

# Project Architecture

The project follows a modular Django application structure.

