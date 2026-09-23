import os
import uvicorn


def start():
    dev_mode = os.getenv("DEV", "false").lower() == "true"
    uvicorn.run(
        "api.app:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000")),
        reload=dev_mode,
    )


if __name__ == "__main__":
    start()
