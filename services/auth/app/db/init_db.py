"""Initialize database"""
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import get_password_hash
from app.db.session import Base, engine
from app.models.user import User


def init_db(db: Session) -> None:
    """Initialize database with default superuser if it doesn't exist"""
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    # Check if superuser already exists
    superuser = db.query(User).filter(User.email == "admin@example.com").first()
    
    if not superuser:
        # Create default superuser
        superuser = User(
            email="admin@example.com",
            hashed_password=get_password_hash("admin"),
            full_name="Default Admin",
            is_superuser=True,
        )
        db.add(superuser)
        db.commit()
