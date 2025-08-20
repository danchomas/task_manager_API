# main.py
from fastapi import FastAPI
from app.routers import tasks
from app.database import engine, Base
import uvicorn

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Manager API",
    description="A simple CRUD API for managing tasks.",
    version="1.0.0"
)

app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])


if __name__ == "__main__":
    uvicorn.run('main:app', host="127.0.0.1", port=8000, reload=True)
