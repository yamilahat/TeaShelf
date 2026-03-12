from fastapi import FastAPI

from app.config import settings

from app.routers.health import router as health_router
from app.routers.teas import router as teas_router


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name)

    app.include_router(health_router, prefix="")
    app.include_router(teas_router, prefix="")

    return app


app = create_app()
