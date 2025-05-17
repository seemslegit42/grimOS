from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import User
from app.api.v1.security.auth import has_role, has_permission

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)

@router.get("/dashboard")
async def admin_dashboard(current_user: User = Depends(has_role(["admin"]))):
    """Admin dashboard - requires admin role."""
    return {
        "message": "Welcome to the admin dashboard",
        "user": {
            "id": current_user.id,
            "email": current_user.email,
            "name": f"{current_user.first_name} {current_user.last_name}"
        }
    }

@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(has_permission(["delete"]))
):
    """Delete a user - requires delete permission."""
    # Prevent self-deletion
    if str(current_user.id) == str(user_id):
        return {"message": "Cannot delete yourself"}
    
    # Find user to delete
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"message": "User not found"}
    
    # Delete user
    db.delete(user)
    db.commit()
    
    return {"message": f"User with ID {user_id} has been deleted"}
