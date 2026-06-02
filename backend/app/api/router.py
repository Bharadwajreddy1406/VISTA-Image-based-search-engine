from fastapi import APIRouter
from .routes import (search_router, health_router)

router = APIRouter()

router.include_router(search_router, prefix="/images", tags=["images search"])
router.include_router(health_router, prefix="/health", tags=["health"])
