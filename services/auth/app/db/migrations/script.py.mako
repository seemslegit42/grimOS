"""
Create the initial migration
"""
from app.core.config import settings
from app.db.session import Base
from app.models.user import RefreshToken, User  # noqa

# Create metadata
metadata = Base.metadata
