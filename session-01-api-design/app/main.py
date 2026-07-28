from fastapi import FastAPI

from app.api.v1.routes.users import router as users_router

app = FastAPI(
    title="TaskFlow API",
    description="Internal Team Work Management Backend — Session 1: API Design",
    version="0.1.0",
)

app.include_router(users_router)


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}