from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from api.tasks_routers import router as tasks_router
from api.user_routers import router as user_router
from core.database import engine, Base
import uvicorn

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Manager API",
    description="A simple task manager API",
    version="0.0.1",
    docs_url="/docs",
    # openapi_security=[{  # Убрано, так как это некорректно для APIKeyHeader
    #     "BearerAuth": []
    # }]
)

# Подключаем роутеры
app.include_router(tasks_router, prefix="/tasks", tags=["tasks"])
app.include_router(user_router, prefix="/users", tags=["users"])

# Монтируем папку frontend как статику
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

# Корневой маршрут для обслуживания index.html
@app.get("/", response_class=HTMLResponse)
async def serve_root():
    with open("frontend/index.html") as f:
        return HTMLResponse(content=f.read())

if __name__ == "__main__":
    uvicorn.run('main:app', host="127.0.0.1", port=8000, reload=True)