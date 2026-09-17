from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from .config import settings
from .db import Base, engine, SessionLocal
from .models.entities import Detection
from .api.dashboard import router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AEGISFARM API",
    description="35% Project prototype — adaptive AI invisible fence for crop protection.",
    version="0.1.0",
)

origins = [x.strip() for x in settings.cors_origins.split(",") if x.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)

# Seed one harmless demo event only if database is empty.
db = SessionLocal()
try:
    if db.query(Detection).count() == 0:
        pass
finally:
    db.close()

@app.get("/")
def root():
    return {
        "project": "AEGISFARM",
        "status": "online",
        "flow": "Detect → Identify → Predict → Deter → Observe → Adapt → Verify → Learn",
        "docs": "/docs",
    }
