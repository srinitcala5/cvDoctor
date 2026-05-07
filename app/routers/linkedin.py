from fastapi import APIRouter, Depends

from app.models.linkedin import LinkedInOptimizeRequest, LinkedInOptimizeResponse
from app.services.linkedin import optimise_linkedin
from app.utils.auth import get_current_user

router = APIRouter(prefix="/linkedin", tags=["linkedin"])


@router.post("/optimise", response_model=LinkedInOptimizeResponse)
def optimise_linkedin_profile(
    body: LinkedInOptimizeRequest,
    _user: dict = Depends(get_current_user),
):
    return optimise_linkedin(body.headline, body.about, body.experience)
