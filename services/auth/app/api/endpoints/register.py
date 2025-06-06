"""Registration endpoints."""
from datetime import datetime
from fastapi import APIRouter, BackgroundTasks, HTTPException, status

from app.api.deps import SessionDep
from app.core.kafka import publish_user_event
from app.core.async_kafka import publish_user_event as publish_user_event_async
from app.crud.user import create_user, get_user_by_email
from app.models.user import User
from app.schemas.auth import Message, UserCreate, UserRead

router = APIRouter(tags=["registration"])


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_new_user(
    db: SessionDep,
    user_in: UserCreate,
    background_tasks: BackgroundTasks,
) -> UserRead:
    """
    Register a new user.
    
    This endpoint allows public registration of new users.
    """
    # Check if email is already registered
    user = get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    # Set default values for new users
    user_in.is_superuser = False  # Ensure no one can register as superuser
    
    # Create the user
    user = create_user(db=db, user_in=user_in)
    
    # Publish user signup event to Kafka
    user_data = UserRead(
        id=str(user.id),
        email=user.email,
        full_name=user.full_name,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
    )
    
    # Add additional metadata
    metadata = {
        "source_ip": "127.0.0.1",  # In a real app, you'd get this from the request
        "registration_timestamp": datetime.now().isoformat(),
        "client_info": "Web API"
    }
    
    # Use async Kafka producer in a background task to avoid blocking
    background_tasks.add_task(
        publish_user_event_async,
        event_type="user_registered",
        user_id=str(user.id),
        user_data=user_data,
        metadata=metadata
    )
    
    return user_data