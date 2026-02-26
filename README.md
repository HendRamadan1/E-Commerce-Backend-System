# 🛒 E-Commerce Backend System

A production-ready **E-Commerce Backend API** built with **FastAPI**, designed with scalable architecture, secure authentication, background processing, and payment integration.

---

## 🚀 Features

- 🔐 JWT Authentication & Role-based access
- 🛍️ Full E-commerce workflow (Cart → Order → Payment → Shipping)
- 💳 Stripe Payment Integration
- 📦 Address & Shipping Management
- ⚙️ Background Tasks with Celery (Email verification, async jobs)
- 🔁 Redis for caching & Celery broker
- 🗄️ PostgreSQL with Alembic migrations
- 🧱 Clean Architecture (Schema → Service → Router)
- 🧰 Global Error Handling (`src.error`)
- 🔒 Password hashing & security middleware
- 🛠️ Admin creation & management
- 🔗 Fully defined relationships between all entities

---

## 🏗️ Project Architecture
src/
│
├── auth/
├── cart/
├── category/
├── product/
├── order/
├── payment/
├── address/
├── customer/
│
├── db/
│ ├── models/
│ ├── session.py
│
├── core/
│ ├── config.py
│ ├── security.py
│
├── error/
│ ├── handlers.py
│ ├── exceptions.py
│
├── middleware/
│ ├── auth_middleware.py
│
├── tasks/
│ ├── celery_app.py
│ ├── email_tasks.py
│
├── utils/
│
└── main.py


---

## 🧩 Architecture Pattern

Each table/module follows the same structure:


module/   
   ├── schema.py # Pydantic models
   ├── service.py # Business logic
   ├── router.py # API endpoints     
   ├── model.py # SQLModel table   


✔️ Ensures separation of concerns  
✔️ Easy scaling & maintenance  

---

## 🗄️ Database Models & Relationships

### 👤 Customer
- One-to-many → Orders
- One-to-many → Addresses
- One-to-many → Payments

### 🛒 Cart
- One-to-many → CartItems
- Belongs to Customer

### 📦 Order
- One-to-many → OrderItems
- One-to-one → Payment
- One-to-one → Shipping Address

### 💳 Payment
- Belongs to Order
- Supports:
  - Card (Stripe)
  - Wallet
  - Cash on delivery

### 📍 Address
- Belongs to Customer
- Used as Shipping Address during checkout

---

## 💳 Payment Flow

1. User checkout → creates Order
2. User submits payment + address
3. System:
   - Saves shipping address
   - Creates payment record
   - Integrates with Stripe
   - Updates order status → `paid` → `shipped`

---

## 🔁 Background Tasks (Celery)

Used for:

- 📧 Email verification
- 🔑 Password hashing
- 📬 Order notifications
- 🔔 Async system events

---

## 🧰 Technologies Used

| Technology | Purpose |
|-----------|--------|
| FastAPI | API Framework |
| PostgreSQL | Database |
| SQLModel | ORM |
| Alembic | Database migrations |
| Redis | Cache & Celery broker |
| Celery | Background tasks |
| Stripe | Payment processing |
| JWT | Authentication |
| Docker | Containerization |

---

## ⚙️ Environment Variables

Create `.env` file:


---

## ▶️ Running the Project

### 1️⃣ Install dependencies

```bash
pip install -r requirements.txt
```
### 2️⃣ Run migrations
```bash
alembic upgrade head
```

### 3️⃣ Start server
```bash
uvicorn src.__init__:app --reload
```

📞 Contact

Hend Ramadan
📧 Email: hendtalba@gmail.com

💼 LinkedIn: https://linkedin.com/in/yourprofile

💻 GitHub: https://github.com/yourusername
