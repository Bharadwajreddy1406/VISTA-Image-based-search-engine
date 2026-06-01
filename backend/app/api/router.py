from fastapi import APIRouter
from .routes import (search_router, health_router)

router = APIRouter()

router.include_router(search_router, prefix="/search", tags=["search"])
router.include_router(health_router, prefix="/health", tags=["health"])
