from .search import router as search_router #noqa: F401
from .health import router as health_router #noqa: F401

__all__ = ["search_router", "health_router"]