from fastapi import APIRouter

router = APIRouter(prefix="/linkedin", tags=["linkedin"])


@router.get("/health")
async def health_check():
    return {"status": "linkedin-ready"}
