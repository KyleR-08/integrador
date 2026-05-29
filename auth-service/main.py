from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import select

from models import User, create_db_and_tables, get_session
from auth import encrypt_password, decrypt_password


@asynccontextmanager
async def lifespan(app):
    create_db_and_tables()
    yield


app = FastAPI(
    title="Auth Service - UIDE",
    description="Microservicio de autenticación - Proyecto Integrador 3er Semestre",
    lifespan=lifespan,
)


class UserCreate(BaseModel):
    username: str
    password: str


@app.get("/")
def root():
    return {
        "service": "auth-service",
        "info": "Proyecto Integrador 3er Semestre UIDE - VLAN 10",
        "endpoints": ["/register", "/login"],
    }


@app.post("/register")
def register(data: UserCreate, session = Depends(get_session)):
    statement = select(User).where(User.username == data.username)
    existing_user = session.exec(statement).first()

    if existing_user is not None:
        raise HTTPException(status_code=400, detail="El username ya está registrado.")

    encrypted = encrypt_password(data.password)

    new_user = User(username=data.username, encrypted_password=encrypted)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return {
        "message": "Usuario registrado correctamente.",
        "user_id": new_user.id,
        "username": new_user.username,
    }


@app.post("/login")
def login(data: UserCreate, session = Depends(get_session)):
    statement = select(User).where(User.username == data.username)
    user = session.exec(statement).first()

    if user is None:
        raise HTTPException(status_code=401, detail="Credenciales inválidas.")

    decrypted = decrypt_password(user.encrypted_password)

    if decrypted != data.password:
        raise HTTPException(status_code=401, detail="Credenciales inválidas.")

    return {
        "message": "Login exitoso.",
        "username": user.username,
    }
