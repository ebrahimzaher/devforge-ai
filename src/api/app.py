from fastapi import FastAPI
from api.routes import router


def create_app() -> FastAPI:
    app = FastAPI(
        title="DevForge AI",
        description="Multi-agent system that generates a full codebase from a plain-language request.",
        version="0.1.0",
    )
    app.include_router(router)
    return app


app = create_app()
