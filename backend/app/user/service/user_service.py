from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from typing import Optional, List
from ..model.user import User
from ..schema.user import UserCreate, UserUpdate, UserResponse, UserProfile
from ...skill.model.skill import Skill


class UserService:
    """Service class for User operations"""
    
    @staticmethod
    async def create_user(db: AsyncSession, user_data: UserCreate) -> User:
        """Create a new user"""
        db_user = User(
            name=user_data.name,
            position=user_data.position,
            email=user_data.email,
            password=user_data.password,
            avatar_url=user_data.avatar_url
        )
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user
    
    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
        """Get user by ID"""
        result = await db.execute(select(User).filter(User.id == user_id))
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
        """Get user by email"""
        result = await db.execute(select(User).filter(User.email == email))
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_all_users(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users with pagination"""
        result = await db.execute(select(User).offset(skip).limit(limit))
        return result.scalars().all()    
    @staticmethod
    async def update_user(db: AsyncSession, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """Update user by ID"""
        db_user = await UserService.get_user_by_id(db, user_id)
        if not db_user:
            return None

        update_data = user_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)

        await db.commit()
        await db.refresh(db_user)
        return db_user
    
    @staticmethod
    async def delete_user(db: AsyncSession, user_id: int) -> bool:
        """Delete user by ID"""
        db_user = await UserService.get_user_by_id(db, user_id)
        if not db_user:
            return False
        
        # Delete all skills associated with the user first
        await db.execute(delete(Skill).filter(Skill.user_id == user_id))
        
        await db.delete(db_user)
        await db.commit()
        return True
    
    @staticmethod
    async def authenticate_user(db: AsyncSession, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password"""
        user = await UserService.get_user_by_email(db, email)
        if user and user.password == password: 
            return user
        return None
    
    @staticmethod
    async def get_user_profile(db: AsyncSession, user_id: int) -> Optional[User]:
        """Get user profile with skills for the profile page"""
        result = await db.execute(
            select(User)
            .options(selectinload(User.skills))
            .filter(User.id == user_id)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def user_exists(db: AsyncSession, email: str) -> bool:
        """Check if user exists by email"""
        result = await db.execute(select(User).filter(User.email == email))
        return result.scalar_one_or_none() is not None
    
    @staticmethod
    async def get_user_skills_count(db: AsyncSession, user_id: int) -> int:
        """Get count of skills for a user"""
        result = await db.execute(select(Skill).filter(Skill.user_id == user_id))
        return len(result.scalars().all())
