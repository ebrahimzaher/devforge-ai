from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router


def create_app() -> FastAPI:
    app = FastAPI(
        title="DevForge AI",
        description="Multi-agent system that generates a full codebase from a plain-language request.",
        version="0.1.0",
    )

    # Allow all origins so the frontend (localhost:3000 or Cloudflare tunnel) can call the API
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router)
    return app


app = create_app()
