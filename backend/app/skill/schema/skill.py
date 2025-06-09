from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class SkillBase(BaseModel):
    """Base skill schema with common fields"""
    name: str = Field(..., min_length=1, max_length=100, description="Skill name")
    category: str = Field(..., min_length=1, max_length=100, description="Skill category (e.g., programming, database, framework)")
    description: Optional[str] = Field(None, max_length=500, description="Skill description")
    level: float = Field(..., ge=1.0, le=10.0, description="Skill level from 1-10 for spider chart")


class SkillCreate(SkillBase):
    """Schema for creating a new skill"""
    user_id: int = Field(..., description="ID of the user this skill belongs to")


class SkillUpdate(BaseModel):
    """Schema for updating an existing skill"""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Skill name")
    category: Optional[str] = Field(None, min_length=1, max_length=100, description="Skill category")
    description: Optional[str] = Field(None, max_length=500, description="Skill description")
    level: Optional[float] = Field(None, ge=1.0, le=10.0, description="Skill level from 1-10")


class SkillResponse(SkillBase):
    """Schema for skill response"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(..., description="Skill's unique identifier")
    user_id: int = Field(..., description="ID of the user this skill belongs to")
    created_at: datetime = Field(..., description="When the skill was created")
    updated_at: datetime = Field(..., description="When the skill was last updated")
