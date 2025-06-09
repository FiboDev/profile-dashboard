from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime


class UserBase(BaseModel):
    """Base user schema with common fields"""
    name: str = Field(..., min_length=1, max_length=100, description="User's full name")
    position: str = Field(..., min_length=1, max_length=100, description="User's position in the company")
    email: str = Field(..., description="User's email address")


class UserCreate(UserBase):
    """Schema for creating a new user"""
    password: str = Field(..., min_length=6, max_length=255, description="User's password")
    avatar_url: Optional[str] = Field(None, max_length=500, description="URL to user's avatar image")


class UserUpdate(BaseModel):
    """Schema for updating an existing user"""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="User's full name")
    position: Optional[str] = Field(None, min_length=1, max_length=100, description="User's position in the company")
    email: Optional[str] = Field(None, description="User's email address")
    avatar_url: Optional[str] = Field(None, max_length=500, description="URL to user's avatar image")


class UserLogin(BaseModel):
    """Schema for user login"""
    email: str = Field(..., description="User's email address")
    password: str = Field(..., min_length=1, description="User's password")


class UserResponse(UserBase):
    """Schema for user response (excludes sensitive information)"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(..., description="User's unique identifier")
    avatar_url: Optional[str] = Field(None, description="URL to user's avatar image")
    created_at: datetime = Field(..., description="When the user was created")
    updated_at: datetime = Field(..., description="When the user was last updated")


class UserSkillForProfile(BaseModel):
    """Schema for skills when shown in user profile"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(..., description="Skill's unique identifier")
    name: str = Field(..., description="Skill name")
    category: str = Field(..., description="Skill category")
    description: Optional[str] = Field(None, description="Skill description")
    level: float = Field(..., description="Skill level from 1-10")


class UserProfile(UserResponse):
    """Extended user schema for profile page with skills"""
    skills: List[UserSkillForProfile] = Field(default=[], description="User's skills for spider chart")
