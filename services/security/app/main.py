from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv

from database import engine, get_db
import models
from routers import threat_intelligence, user_behavior_analytics

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Grimoire Security Module",
    description="Security Module for grimOS providing Threat Intelligence and User Behavior Analytics",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    threat_intelligence.router,
    prefix="/api/security/threat-intelligence",
    tags=["Threat Intelligence"],
)
app.include_router(
    user_behavior_analytics.router,
    prefix="/api/security/uba",
    tags=["User Behavior Analytics"],
)

@app.get("/", tags=["Health Check"])
def read_root():
    """Health check endpoint"""
    return {"status": "healthy", "module": "security"}

@app.get("/api/security/info", tags=["Module Info"])
def module_info():
    """Get information about the Security Module"""
    return {
        "name": "Security Module",
        "version": "0.1.0",
        "features": [
            "Basic Threat Intelligence Aggregation",
            "Foundational User Behavior Analytics (Login Anomalies)"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)