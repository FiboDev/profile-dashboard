from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from database.database import get_session
from ...schema.skill import SkillCreate, SkillUpdate, SkillResponse
from ...service.skill_service import SkillService
from app.core.auth import get_current_user
from app.user.schema.user import UserResponse

router = APIRouter()

@router.post("/", response_model=SkillResponse, status_code=status.HTTP_201_CREATED)
async def create_skill(
    skill_data: SkillCreate,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    """Create a new skill for the authenticated user"""
    # Users can only create skills for themselves
    if skill_data.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only create skills for yourself"
        )
    
    try:
        db_skill = await SkillService.create_skill(db, skill_data)
        return SkillResponse.model_validate(db_skill)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating skill: {str(e)}"
        )

@router.get("/", response_model=List[SkillResponse])
async def get_my_skills(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    """Get authenticated user's skills with optional category filter and pagination"""
    if category:
        skills = await SkillService.get_skills_by_category(db, category, skip=skip, limit=limit)
        # Filter to only include current user's skills
        skills = [skill for skill in skills if skill.user_id == current_user.id]
    else:
        skills = await SkillService.get_skills_by_user_id(db, current_user.id)
        # Apply pagination manually since we're filtering by user
        skills = skills[skip:skip + limit]
    
    return [SkillResponse.model_validate(skill) for skill in skills]

@router.get("/{skill_id}", response_model=SkillResponse)
async def get_skill(
    skill_id: int,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    """Get skill by ID - only own skills allowed"""
    skill = await SkillService.get_skill_by_id(db, skill_id)
    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found"
        )
    
    # Users can only access their own skills
    if skill.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own skills"
        )
    
    return SkillResponse.model_validate(skill)

@router.get("/user/{user_id}", response_model=List[SkillResponse])
async def get_user_skills(
    user_id: int,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    """Get all skills for a specific user - only own skills allowed"""
    # Users can only access their own skills
    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own skills"
        )
    
    skills = await SkillService.get_skills_by_user_id(db, user_id)
    return [SkillResponse.model_validate(skill) for skill in skills]

@router.put("/{skill_id}", response_model=SkillResponse)
async def update_skill(
    skill_id: int,
    skill_data: SkillUpdate,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    """Update skill by ID - only own skills allowed"""
    # First check if skill exists and belongs to current user
    existing_skill = await SkillService.get_skill_by_id(db, skill_id)
    if not existing_skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found"
        )
    
    if existing_skill.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own skills"
        )
    
    updated_skill = await SkillService.update_skill(db, skill_id, skill_data)
    return SkillResponse.model_validate(updated_skill)

@router.delete("/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_skill(
    skill_id: int,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    """Delete skill by ID - only own skills allowed"""
    # First check if skill exists and belongs to current user
    existing_skill = await SkillService.get_skill_by_id(db, skill_id)
    if not existing_skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found"
        )
    
    if existing_skill.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own skills"
        )
    
    await SkillService.delete_skill(db, skill_id)