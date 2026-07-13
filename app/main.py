from dotenv import load_dotenv
from fastapi import FastAPI

from app.api.v1.asset_router import router as asset_router

load_dotenv()

app = FastAPI(
    title="USD Asset Management System API",
    description="API to manage USD files",
    version="1.0.0",
)

app.include_router(asset_router, prefix="/api/v1", tags=["Assets"])
