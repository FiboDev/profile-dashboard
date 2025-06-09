"""
Authentication utilities for simple session-based auth
"""
from fastapi import Request, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.user.model.user import User
from app.user.service.user_service import UserService
from database.database import get_session

class AuthService:
    """Simple session-based authentication service"""
    
    @staticmethod
    def login_user(request: Request, user: User) -> None:
        """Login user by storing user_id in session"""
        request.session["user_id"] = user.id
        request.session["user_email"] = user.email
    
    @staticmethod
    def logout_user(request: Request) -> None:
        """Logout user by clearing session"""
        request.session.clear()
    
    @staticmethod
    def get_current_user_id(request: Request) -> Optional[int]:
        """Get current user ID from session"""
        return request.session.get("user_id")
    
    @staticmethod
    def is_authenticated(request: Request) -> bool:
        """Check if user is authenticated"""
        return "user_id" in request.session

async def get_current_user(
    request: Request,
    db: AsyncSession = Depends(get_session)
) -> User:
    """Dependency to get current authenticated user"""
    user_id = AuthService.get_current_user_id(request)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated. Please login first."
        )
    
    user = await UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User session invalid. Please login again."
        )
    
    return user

async def get_current_user_optional(
    request: Request,
    db: AsyncSession = Depends(get_session)
) -> Optional[User]:
    """Optional dependency to get current user without raising error"""
    user_id = AuthService.get_current_user_id(request)
    if not user_id:
        return None
    
    return await UserService.get_user_by_id(db, user_id)
