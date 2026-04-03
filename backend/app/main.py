from fastapi import FastAPI, HTTPException

from app.api.router import api_router
from app.core.config import settings
from app.db.session import check_db_connection

app = FastAPI(
    title=settings.app_name,
    debug=settings.app_debug,
)

app.include_router(api_router)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "app": settings.app_name,
        "environment": settings.app_env,
    }


@app.get("/health/db")
def health_db():
    try:
        check_db_connection()
        return {"status": "ok", "database": "connected"}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {exc}")