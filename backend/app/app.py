from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.db import Base, engine
from app.routes.users import auth_backend, fastapi_users
from app.schemas.users import UserRead, UserCreate, UserUpdate

# Routers
from app.routes.todo import router as todo_router
from app.routes.product import router as product_router
from app.routes.cart import router as cart_router
from app.routes.checkout import router as checkout_router
from app.routes.order import router as order_router


# ----------------------------
# Database Initialization
# ----------------------------
async def create_db_and_tables():
    """Initializes the database and creates all defined tables."""
    print("Database initialization starting...")
    
    # Import all models here so Base.metadata knows all tables
    from app.models.users import User
    from app.models.todo import Todo
    from app.models.product import Product
    from app.models.cart import CartItem
    from app.models.order import Order
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created successfully.")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield


# ----------------------------
# FastAPI App
# ----------------------------
app = FastAPI(lifespan=lifespan)

# ----------------------------
# CORS Middleware
# ----------------------------
origins = ["http://localhost:3000"]  # your Next.js dev server

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# Auth Routes (Cookie-based)
# ----------------------------
app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)


# ----------------------------
# Other Routers
# ----------------------------
app.include_router(todo_router)
app.include_router(product_router)
app.include_router(cart_router)
app.include_router(checkout_router)
app.include_router(order_router)