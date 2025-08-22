from fastapi import FastAPI
from tasks.routers import router as tasks_router
from tasks.database import engine, Base
import uvicorn

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(tasks_router, prefix="/tasks", tags=["tasks"])


if __name__ == "__main__":
    uvicorn.run('main:app', host="127.0.0.1", port=8000, reload=True)
