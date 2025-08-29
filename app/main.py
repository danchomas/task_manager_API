from fastapi import FastAPI
from api.tasks_routers import router as tasks_router
from api.user_routers import router as user_router
from core.database import engine, Base
import uvicorn

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(tasks_router, prefix="/tasks", tags=["tasks"])
app.include_router(user_router, prefix="/users", tags=["users"])


if __name__ == "__main__":
    uvicorn.run('main:app', host="127.0.0.1", port=8000, reload=True)
