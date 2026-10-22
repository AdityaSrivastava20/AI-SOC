from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.scanners import router as scanner_router
from backend.database.database import Base, engine
from backend.database import models

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI-SOC API",
    description="AI-powered Security Operations Center",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    scanner_router,
    prefix="/scan",
    tags=["Scanner"]
)


@app.get("/")
def root():
    return {
        "message": "AI-SOC API is running",
        "status": "online"
    }