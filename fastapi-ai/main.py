from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import router
from config.logging import configure_logging
from config.settings import settings

configure_logging()

app = FastAPI(title="ujmikamiapp AI service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)

app.include_router(router)
