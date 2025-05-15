from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import time
import traceback
from contextlib import asynccontextmanager

from app.core.config import settings
from app.api.v1.router import router as api_router
from app.core.exceptions import BaseAPIException

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("grimos")

# External services connections
redis_client = None
kafka_producer = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Initialize external connections when the app starts
    and close them when it shuts down
    """
    # Set up Redis connection if enabled
    if settings.REDIS_URL:
        try:
            import redis
            global redis_client
            logger.info(f"Connecting to Redis at {settings.REDIS_URL}")
            redis_client = redis.from_url(settings.REDIS_URL)
            redis_client.ping()
            logger.info("Redis connection established")
        except ImportError:
            logger.warning("Redis package not installed. Caching will be disabled.")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {str(e)}")
    
    # Set up Kafka connection if enabled
    if settings.KAFKA_BOOTSTRAP_SERVERS:
        try:
            from kafka import KafkaProducer
            global kafka_producer
            logger.info(f"Connecting to Kafka at {settings.KAFKA_BOOTSTRAP_SERVERS}")
            kafka_producer = KafkaProducer(
                bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS.split(","),
                value_serializer=lambda v: bytes(str(v), encoding='utf-8')
            )
            logger.info("Kafka producer initialized")
        except ImportError:
            logger.warning("Kafka package not installed. Event streaming will be disabled.")
        except Exception as e:
            logger.error(f"Failed to connect to Kafka: {str(e)}")
    
    yield
    
    # Close connections
    if redis_client:
        logger.info("Closing Redis connection")
        redis_client.close()
    
    if kafka_producer:
        logger.info("Closing Kafka producer")
        kafka_producer.close()

# Create FastAPI app
app = FastAPI(
    title="GrimOS API",
    description="GrimOS Backend API for Security, Operations, and Cognitive services",
    version="0.1.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request middleware for logging and timing
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Log the request
    logger.debug(f"Request started: {request.method} {request.url}")
    
    # Process the request
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        
        # Add processing time header
        response.headers["X-Process-Time"] = str(process_time)
        
        # Log the response
        logger.debug(
            f"Request completed: {request.method} {request.url} - "
            f"Status: {response.status_code}, Time: {process_time:.4f}s"
        )
        
        return response
    except Exception as e:
        # Log the error
        logger.error(
            f"Request failed: {request.method} {request.url} - Error: {str(e)}\n"
            f"{traceback.format_exc()}"
        )
        raise

# Exception handler for custom API exceptions
@app.exception_handler(BaseAPIException)
async def api_exception_handler(request: Request, exc: BaseAPIException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "code": exc.code},
    )

# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify that the API is running
    and connections to external services are operational.
    """
    status = "ok"
    external_services = {}
    
    # Check Redis connection
    if redis_client:
        try:
            redis_client.ping()
            external_services["redis"] = "ok"
        except Exception as e:
            external_services["redis"] = {"status": "error", "message": str(e)}
            status = "degraded"
    else:
        external_services["redis"] = "disabled"
    
    # Check Kafka connection
    if kafka_producer:
        try:
            # Check if Kafka is connected (no good way to ping)
            # This just checks if the client is initialized
            if kafka_producer.bootstrap_connected():
                external_services["kafka"] = "ok"
            else:
                external_services["kafka"] = "disconnected"
                status = "degraded"
        except Exception as e:
            external_services["kafka"] = {"status": "error", "message": str(e)}
            status = "degraded"
    else:
        external_services["kafka"] = "disabled"
    
    # Check database connection
    try:
        from app.db.session import SessionLocal
        with SessionLocal() as db:
            db.execute("SELECT 1")
        external_services["database"] = "ok"
    except Exception as e:
        external_services["database"] = {"status": "error", "message": str(e)}
        status = "error"  # Database is critical, so overall status is error
    
    return {
        "status": status,
        "environment": settings.ENVIRONMENT,
        "version": app.version,
        "services": external_services,
    }

# Include routers
app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=settings.DEBUG)