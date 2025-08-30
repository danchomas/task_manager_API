# main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
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
    openapi_security=[{
        "BearerAuth": []
    }]
)

app.mount("/frontend/static", StaticFiles(directory="frontend"), name="static")

@app.get("/frontend/")
async def read_frontend():
    return FileResponse('frontend/index.html')

@app.get("/frontend/{file_path:path}")
async def read_frontend_file(file_path: str):
    file_path = f"frontend/{file_path}"
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return FileResponse('frontend/index.html')

app.include_router(tasks_router, prefix="/tasks", tags=["tasks"])
app.include_router(user_router, prefix="/users", tags=["users"])

if __name__ == "__main__":
    uvicorn.run('main:app', host="127.0.0.1", port=8000, reload=True)
