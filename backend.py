""" FastAPI backend aplikacije za login uz upotrebu pydantic-a za robusnost modela kroz validaciju podataka """

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, constr
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import hashlib
import uuid

# Initialize FastAPI app
app = FastAPI()

# SQLAlchemy setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./users2.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # Allows all origins; for production, specify your frontend URL here
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)


# SQLAlchemy User model
class User(Base):
    __tablename__ = "users2"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    user_uuid = Column(String, unique=True, nullable=False)


# Create the database tables
Base.metadata.create_all(bind=engine)


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Hashing function
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# Generate verification code
def generate_verification_code(username, password):
    combined = username + password
    return hashlib.sha256(combined.encode()).hexdigest()[:8]


# Pydantic models for data validation
class UserCreate(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    username: str
    user_uuid: str

    class Config:
        orm_mode = True  # To allow automatic conversion from SQLAlchemy models


# Register new user
@app.post("/register", response_model=UserResponse)
async def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check if the user already exists
    user_exist = db.query(User).filter(User.username == user_data.username).first()
    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists"
        )

    user_uuid = str(uuid.uuid4())
    password_hash = hash_password(user_data.password)

    new_user = User(
        username=user_data.username, password_hash=password_hash, user_uuid=user_uuid
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# Login user
@app.post("/login")
async def login_user(user_data: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_data.username).first()
    if not user or user.password_hash != hash_password(user_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    verification_code = generate_verification_code(
        user_data.username, user_data.password
    )

    return {
        "message": "Login successful",
        "verification_code": verification_code,
        "user_uuid": user.user_uuid,
        "username": user.username,
    }


# Get user details (for welcome page)
@app.get("/user/{user_uuid}", response_model=UserResponse)
async def get_user(user_uuid: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_uuid == user_uuid).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return user
