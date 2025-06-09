from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import Optional, List
from ..model.skill import Skill
from ..schema.skill import SkillCreate, SkillUpdate, SkillResponse
from ...user.model.user import User


class SkillService:
    """Service class for Skill operations"""
    
    @staticmethod
    async def create_skill(db: AsyncSession, skill_data: SkillCreate) -> Skill:
        """Create a new skill for a user"""
        result = await db.execute(select(User).filter(User.id == skill_data.user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise ValueError(f"User with id {skill_data.user_id} not found")
        
        db_skill = Skill(
            name=skill_data.name,
            category=skill_data.category,
            description=skill_data.description,
            level=skill_data.level,
            user_id=skill_data.user_id
        )
        db.add(db_skill)
        await db.commit()
        await db.refresh(db_skill)
        return db_skill
    
    @staticmethod
    async def get_skill_by_id(db: AsyncSession, skill_id: int) -> Optional[Skill]:
        """Get skill by ID"""
        result = await db.execute(select(Skill).filter(Skill.id == skill_id))
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_skills_by_user_id(db: AsyncSession, user_id: int) -> List[Skill]:
        """Get all skills for a specific user"""
        result = await db.execute(select(Skill).filter(Skill.user_id == user_id))
        return result.scalars().all()
    
    @staticmethod
    async def get_all_skills(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Skill]:
        """Get all skills with pagination"""
        result = await db.execute(select(Skill).offset(skip).limit(limit))
        return result.scalars().all()
    
    @staticmethod
    async def get_skills_by_category(db: AsyncSession, category: str, skip: int = 0, limit: int = 100) -> List[Skill]:
        """Get skills filtered by category"""
        result = await db.execute(
            select(Skill)
            .filter(Skill.category == category)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    @staticmethod
    async def update_skill(db: AsyncSession, skill_id: int, skill_data: SkillUpdate) -> Optional[Skill]:
        """Update skill by ID"""
        db_skill = await SkillService.get_skill_by_id(db, skill_id)
        if not db_skill:
            return None
        
        update_data = skill_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_skill, field, value)
        
        await db.commit()
        await db.refresh(db_skill)
        return db_skill
    
    @staticmethod
    async def delete_skill(db: AsyncSession, skill_id: int) -> bool:
        """Delete skill by ID"""
        db_skill = await SkillService.get_skill_by_id(db, skill_id)
        if not db_skill:
            return False
        
        await db.delete(db_skill)
        await db.commit()
        return True
    
    @staticmethod
    async def delete_skills_by_user_id(db: AsyncSession, user_id: int) -> int:
        """Delete all skills for a user. Returns count of deleted skills"""
        result = await db.execute(select(Skill).filter(Skill.user_id == user_id))
        skills = result.scalars().all()
        deleted_count = len(skills)
        
        await db.execute(delete(Skill).filter(Skill.user_id == user_id))
        await db.commit()
        return deleted_count
    
    @staticmethod
    async def skill_exists_for_user(db: AsyncSession, user_id: int, skill_name: str) -> bool:
        """Check if a skill with given name already exists for a user"""
        result = await db.execute(
            select(Skill).filter(Skill.user_id == user_id, Skill.name == skill_name)
        )
        return result.scalar_one_or_none() is not None
    
    @staticmethod
    async def get_user_skills_for_profile(db: AsyncSession, user_id: int) -> List[Skill]:
        """Get user skills ordered by level"""
        result = await db.execute(
            select(Skill)
            .filter(Skill.user_id == user_id)
            .order_by(Skill.level.desc())
        )
        return result.scalars().all()