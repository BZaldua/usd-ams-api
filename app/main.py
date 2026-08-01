from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from dotenv import load_dotenv
from fastapi import APIRouter, FastAPI

from app.api.exceptions import init_exception_handlers
from app.api.v1.endpoints import asset_router, render_router, task_router
from app.container import AppProvider

load_dotenv()

app = FastAPI(
    title="USD Asset Management System API",
    description="API to manage USD files",
    version="1.0.0",
)

v1_router = APIRouter(prefix="/api/v1")
v1_router.include_router(asset_router, tags=["Assets"])
v1_router.include_router(task_router, tags=["Tasks"])
v1_router.include_router(render_router, tags=["Renders"])

app.include_router(v1_router)

init_exception_handlers(app)

container = make_async_container(AppProvider())
setup_dishka(container, app)
