# app/routes/currencies.py
import logging

from fastapi import APIRouter, Depends, HTTPException, status

from app.config.config import config
from app.schemas import schemas
from app.services import user_service

router = APIRouter(prefix="/currency", tags=["currency"])

logger = logging.getLogger(__name__)

@router.get("/", response_model=schemas.CurrenciesResponse)
def get_currencies(current_user=Depends(user_service.get_current_user)):
    try:
        if current_user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated"
            )
        return {"currencies": config.VALID_CURRENCIES}
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Failed to get currencies for user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch currencies"
        )
