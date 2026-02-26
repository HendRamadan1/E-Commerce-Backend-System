# E-Commerce Backend System — First Release

A production-grade backend for a modern e-commerce platform built with **FastAPI**, **SQLModel**, and **PostgreSQL**, designed for scalability, reliability, and clean architecture.  
The system implements a complete commerce workflow from cart management to payment processing and shipping, with strong emphasis on asynchronous processing, security, and maintainability.

This release focuses on a modular service-oriented architecture with clear domain boundaries and production-ready integrations such as Stripe payments, Redis caching, and Celery background workers.

---

## Description

This backend provides a full transactional pipeline:


- Customer → Cart → Order → OrderItems → Payment → Shipping Address → Fulfillment**
- Asynchronous workflows using Celery and Redis
- Stripe webhook handling for payment confirmation
- Secure JWT authentication and role-based access control.
- Centralized error handling and middleware-based request processing
- Alembic-driven schema evolution with PostgreSQL

The system supports three primary roles:

- **Customer**
  - Browse products
  - Manage cart
  - Place orders
  - Add shipping address
  - Make payments
  - Track order status

- **Seller**
  - Add and manage products
  - Update inventory and pricing
  - View orders containing their products

- **Admin**
  - Manage users and roles
  - Oversee orders and payments
  - Monitor system activity
  - Promote users to sellers/admins

RBAC is enforced via middleware and dependency-based authorization in FastAPI.

The project is structured to support horizontal scaling and service extraction if needed.

---

## Interesting Techniques Used

### 1. Authentication & Security (JWT Authentication)
Stateless authentication using access and refresh tokens.

**Techniques used:**
- Token signing & verification
- Expiration & refresh flow
- Dependency-based route protection 
Related concepts:  
https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication
---

### 2.Password Hashing
Passwords are hashed using secure algorithms (e.g., bcrypt).

**Why it matters**
- Why it matters
- Mitigates credential leaks

Related concepts:  
http://developer.mozilla.org/en-US/docs/Web/Security

---

### 3. Asynchronous Database Access
The project uses **SQLModel + AsyncSession** to enable non-blocking database operations.

**Benefits**
- Improves throughput under high concurrency
- Enables efficient I/O handling in FastAPI

Related concepts:  
https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Asynchronous

---

### 4. Webhook Verification for Payment Integrity
Stripe webhook signatures are verified to ensure payload authenticity.

**Benefits**
- Prevents replay attacks
- Ensures event source integrity

Stripe docs:  
https://stripe.com/docs/webhooks/signatures

---

### 5. Background Processing with Task Queues
Celery workers handle non-blocking operations such as:

- Email verification
- Order notifications
- Deferred processing

Concept reference:  
https://developer.mozilla.org/en-US/docs/Web/API/Background_Tasks_API

---

### 6. Enum-Driven Domain State Machines
Order and payment lifecycles are enforced using Python Enums.

**Benefits**
- Prevents invalid state transitions
- Improves readability and maintainability

---

### 7. Service Layer Pattern
Business logic is isolated in service classes rather than routers.

**Benefits**
- Testability
- Clear domain boundaries
- Reusable logic

---

### 8. Middleware-Based Security & Request Handling
Custom middleware enforces authentication and request validation.

Related concept:  
https://developer.mozilla.org/en-US/docs/Web/HTTP/Middleware

---


## Non-Obvious Technologies & Libraries

These tools may be of particular interest to mid-level backend developers:

- **SQLModel** — type-safe ORM built on SQLAlchemy  
  https://sqlmodel.tiangolo.com/

- **Alembic** — schema migrations with version control  
  https://alembic.sqlalchemy.org/

- **Celery** — distributed task queue  
  https://docs.celeryq.dev/

- **Redis** — in-memory data store used as broker & cache  
  https://redis.io/

- **Stripe Python SDK** — payment processing  
  https://stripe.com/docs/api

- **Passlib (bcrypt)** — secure password hashing  
  https://passlib.readthedocs.io/

- **python-dotenv** — environment configuration  
  https://pypi.org/project/python-dotenv/

---

## Project Structure

```text
src/
├── auth/
├── customer/
├── product/
├── category/
├── cart/
├── order/
├── orderitems/
├── payment/
├── address/
├── db/
├── core/
├── middleware/
├── error/
├── tasks/
├── utils/
└── __init__.py

alembic/

```
Directory Notes

   - src/customer/ — customer profiles and account management.
   
   - src/seller/ — seller onboarding and product ownership.
   
   - src/admin/ — administrative controls and role management.
   
   - src/product/ — product catalog and inventory.
   
   - src/category/ — product categorization and hierarchy.
   
   - src/cart/ — shopping cart lifecycle and item management.
   
   - src/order/ — order orchestration and checkout workflow.
   
   - src/order_items/ — order line items linking products to orders.
   
   - src/payment/ — Stripe integration, webhook handling, payment lifecycle.
   
   - src/address/ — shipping address management tied to orders.
   
   - src/tasks/ — Celery app and async background jobs.
   
   - src/error/ — centralized exception handling and custom error types.
   
   - alembic/ — database migration history.

## External Integrations
### Stripe

Handles card payments and webhook-based confirmation.
#### Docs:
https://stripe.com/docs/payments

### Redis
Used for:
Celery broker
Caching
Rate limiting (extensible)
#### Docs:
https://redis.io/docs/


## Architectural Highlights

   - Role-Based Access Control (Customer, Seller, Admin)
   
   - Clean separation: Schema → Service → Router
   
   - Async-first design
   
   - Idempotent payment handling
   
   - State-driven order lifecycle
   
   - Centralized configuration via environment variables
   
   - Designed for containerized deployment
   
   - Background processing with Celery & Redis
   
   - Secure password hashing and authentication workflows
   
   - Middleware-driven request lifecycle management
---

## ⚙️ Environment Variables

Create `.env` file:

---

##  Running the Project

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run migrations

```bash
alembic upgrade head
```

### Start server

```bash
uvicorn src.__init__:app --reload
```

## Contact 

For any questions or inquiries, please feel free to reach out through the following channels:

- Hend Ramadan  
[![Mail](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:hendtalba@gmail.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/hend-ramadan-72a9712a5)
[![Kaggle](https://img.shields.io/badge/Kaggle-20BEFF?style=for-the-badge&logo=Kaggle&logoColor=white)](https://www.kaggle.com/hannod)
