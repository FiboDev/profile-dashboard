from fastapi import APIRouter
from .v1.user import router as user_v1_router

router = APIRouter()

# Include v1 routes
router.include_router(
    user_v1_router,
    prefix="/v1/users",
    tags=["users"]
)