from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.api.api_v1.api import api_router
from app.services.ai_service import AIService
from app.services.vercel_ai import VercelAISDK


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Load models, establish connections, etc.
    print("Starting AI service...")
    yield
    # Shutdown: Clean up resources
    print("Shutting down AI service...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

# Set up CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Initialize AI service
ai_service = AIService()

# Set up Vercel AI SDK
vercel_ai_sdk = VercelAISDK(ai_service)

# Include API routers
app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(vercel_ai_sdk.router, prefix="/vercel-ai")


@app.get("/")
async def root():
    return {
        "message": "Welcome to grimOS AI Service",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "api": f"{settings.API_V1_STR}",
            "vercel_ai_sdk": "/vercel-ai",
        }
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)