from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from dotenv import load_dotenv
from fastapi import FastAPI

from app.api.exceptions import init_exception_handlers
from app.api.v1.asset_router import router as asset_router
from app.api.v1.task_router import router as task_router
from app.container import AppProvider

load_dotenv()

app = FastAPI(
    title="USD Asset Management System API",
    description="API to manage USD files",
    version="1.0.0",
)

app.include_router(asset_router, prefix="/api/v1", tags=["Assets"])
app.include_router(task_router, prefix="/api/v1", tags=["Tasks"])
init_exception_handlers(app)

container = make_async_container(AppProvider())
setup_dishka(container, app)
