import logging
from fastapi import APIRouter, Depends, HTTPException

from app.models import models
from app.schemas import schemas
from app.services import user_service

router = APIRouter(prefix="/user", tags=["user"])

logger = logging.getLogger(__name__)

@router.get("/me", response_model=schemas.UserPublic)
def get_current_user_profile(current_user: models.User = Depends(user_service.get_current_user)):
    try:
        return schemas.UserPublic.from_orm(current_user)
    except HTTPException as e:
        logger.warning(f"Auth error for current user: {e.detail}")
        raise
    except Exception as e:
        logger.exception(f"Unexpected error fetching current user: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch user profile. Please try again later."
        )