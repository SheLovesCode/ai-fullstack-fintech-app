import logging

from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.db import database
from app.models import models
from app.schemas import schemas
from app.services import auth_service
from app.config.config import config

router = APIRouter(prefix="/auth", tags=["auth"])
logger = logging.getLogger(__name__)

@router.get("/login")
def login_user(request: Request):
    try:
        redirect_response = auth_service.login_google(request)
        if not redirect_response:
            logger.warning("Google login returned no redirect")
            return RedirectResponse(url="http://localhost/login/failure")
        return redirect_response
    except Exception as e:
        logger.exception(f"Failed to initiate Google login: {e}")
        return RedirectResponse(url="http://localhost/login/failure")

@router.get("/callback")
async def callback_user(request: Request, code: str, state: str, db: Session = Depends(database.get_db)):
    try:
        data = await auth_service.google_callback(request, code, state, db)
        access_token = data["access_token"]

        response = RedirectResponse(url=config.FRONTEND_SUCCESS_URL)
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            max_age=3600,
        )
        logger.info(f"Google login successful")
        return response

    except HTTPException as e:
        logger.warning(f"Google login HTTP error: {e.detail}")
        return RedirectResponse(url=config.FRONTEND_ERROR_URL)

    except Exception as e:
        logger.exception(f"Google login unexpected error: {e}")
        return RedirectResponse(url="http://localhost/login/failure")

