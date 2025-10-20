# app/main.py
from fastapi import FastAPI
from dotenv import load_dotenv
from starlette.middleware.sessions import SessionMiddleware
import os
from app.db import database

load_dotenv()
from app.routes import auth, users, webhooks, payouts, currency

app = FastAPI(title="Diana's Fullstack Fintech App")

routers = [currency.router, payouts.router, users.router, webhooks.router, auth.router]
for router in routers:
    app.include_router(router, prefix="/api")

app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET_KEY"))
database.Base.metadata.create_all(bind=database.engine)

@app.get("/")
def root():
    return {"message": "Backend is running!"}
