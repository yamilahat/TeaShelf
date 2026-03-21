from fastapi import FastAPI

from app.config import settings
from app.routers.health import router as health_router
from app.routers.tea_sessions import router as tea_sessions_router
from app.routers.teas import router as teas_router
from app.routers.teaware import router as teaware_router


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name)

    app.include_router(health_router, prefix="")
    app.include_router(teas_router, prefix="")
    app.include_router(tea_sessions_router, prefix="")
    app.include_router(teaware_router, prefix="")

    return app


app = create_app()
