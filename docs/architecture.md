# System Architecture

## Overview

The WiFi Billing System is a modular application composed of three main layers:
1.  **Frontend**: A Single Page Application (SPA) built with React.
2.  **Backend**: A RESTful API built with Django.
3.  **Infrastructure**: Includes the Database and RADIUS server.

## Components

### 1. Frontend (React + Vite)
- **Role**: User Interface for administrators and customers.
- **Communication**: Consumes REST APIs exposed by the Django backend.
- **Key Features**:
    - Dashboard for stats.
    - Forms for creating plans and vouchers.
    - Tables for listing customers and transactions.

### 2. Backend (Django)
- **Role**: Core business logic, data persistence, and API provider.
- **Apps**:
    - `accounts`: User authentication and management.
    - `billing`: Pricing plans, vouchers, and transactions.
    - `customers`: Customer profiles.
    - `radius`: Integration logic with FreeRADIUS (managing `radcheck`, `radreply` tables).
    - `api`: Exposes functionality via REST endpoints.

### 3. Database
- **Role**: Stores application data.
- **Schema**:
    - Django tables (auth_user, django_session, etc.)
    - App-specific tables (billing_voucher, customers_customer, etc.)
    - RADIUS tables (radcheck, radreply, radacct, etc.) - *Note: The Django app may interface directly with these or via a separate RADIUS database connection.*

### 4. FreeRADIUS
- **Role**: AAA (Authentication, Authorization, Accounting) server.
- **Interaction**:
    - Authenticates users against the database.
    - Enforces limits (time, data, speed) defined by the backend.
    - Logs accounting data (usage) back to the database.

## Data Flow

1.  **Voucher Creation**:
    - Admin creates a voucher in Frontend -> API Request -> Backend creates Voucher record -> Backend creates RADIUS user entries (username/password/attributes).

2.  **User Login (Captive Portal)**:
    - User connects to WiFi -> Redirected to Captive Portal -> Enters Voucher Code -> Captive Portal sends auth request to RADIUS -> RADIUS checks DB -> Access Granted/Denied.

3.  **Payment**:
    - User initiates payment -> M-Pesa Callback -> Backend processes payment -> Backend generates/activates Voucher -> SMS sent to User.
