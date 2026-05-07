from fastapi import APIRouter

router = APIRouter(prefix="/cover-letter", tags=["cover-letter"])


@router.get("/health")
async def health_check():
    return {"status": "cover-letter-ready"}
