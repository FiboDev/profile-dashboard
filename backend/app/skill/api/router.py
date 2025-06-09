from fastapi import APIRouter
from .v1.skill import router as skill_v1_router

router = APIRouter()

# Include v1 routes
router.include_router(
    skill_v1_router,
    prefix="/v1/skills",
    tags=["skills"]
)