from fastapi import APIRouter

router = APIRouter()

@router.get("/health", tags=["health"])
def health():
    return {"status": "ok"}

@router.get("/databases_health", tags=["health"])
def databases_health():
    return {"postgres": "ok", "milvus": "ok", "minio": "ok"}