from fastapi import FastAPI

app = FastAPI(
    title="TaskFlow API",
    description="Internal Team Work Management Backend — Session 1: API Design",
    version="0.1.0",
)


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}