import uvicorn

from watchdog.app.settings import entry_settings


if __name__ == "__main__":
    uvicorn.run(
        "src.app.main:app",
        host=entry_settings.APP_HOST,
        port=entry_settings.APP_PORTP,
        reload=entry_settings.APP_RELOAD
    )
