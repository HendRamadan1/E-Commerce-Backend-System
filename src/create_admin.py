
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlmodel import select,desc
from src.db.model import Customer
from src.auth.utils import generate_password_hash

async def create_admin_(session):
    result = await session.execute(
        select(Customer).where(Customer.Email == "hendtalba@gmail.com")
    )
    admin = result.scalar_one_or_none()

    if admin:
        admin.role = "admin"
        await session.commit()
        print("✅ User promoted to admin")
    else:
        new_admin = Customer(
            FirstName="System",
            LastName="Admin",
            Email="hendtalba@gmail.com",
            role="admin",
            hashed_password=generate_password_hash("Admin@123"),
            is_verified=True
        )
        session.add(new_admin)
        await session.commit()
        print("✅ Admin created")
