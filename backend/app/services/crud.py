import logging

from typing import Tuple, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import HTTPException, status

from app.models import models
from app.schemas import schemas

logger = logging.getLogger(__name__)


def get_or_create_user(db: Session, google_profile: dict) -> models.User:
    function_name = "get_or_create_user"
    google_id = google_profile.get("sub")
    email = google_profile.get("email")
    full_name = google_profile.get("name")
    profile_pic_url = google_profile.get("picture")

    if not google_id or not email:
        logger.error("[%s] Missing google_id or email: %s", function_name, google_profile)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Google profile data")

    try:
        user = db.query(models.User).filter(models.User.oauth_id == google_id).first()
        if user:
            return user
    except SQLAlchemyError as e:
        logger.exception("[%s] DB query failed: %s", function_name, e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")

    try:
        logger.info("[%s] Creating new user with email=%s, oauth_id=%s", function_name, email, google_id)
        new_user = models.User(
            oauth_provider="google",
            oauth_id=google_id,
            email=email,
            full_name=full_name,
            profile_pic_url=profile_pic_url
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError as e:
        db.rollback()
        logger.exception("[%s] Integrity error creating user: %s", function_name, e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    except SQLAlchemyError as e:
        db.rollback()
        logger.exception("[%s] DB error creating user: %s", function_name, e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")
    except Exception as e:
        db.rollback()
        logger.exception("[%s] Unexpected error creating user: %s", function_name, e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error")


def create_payout_for_user(db: Session, payout: schemas.PayoutCreate, user_id: int) -> models.Payout:
    function_name = "create_payout_for_user"

    try:
        logger.info("[%s] Creating payout for user_id=%s: %s", function_name, user_id, payout.model_dump())
        db_payout = models.Payout(
            **payout.model_dump(),
            user_id=user_id,
            status=models.PayoutStatus.PENDING
        )
        db.add(db_payout)
        db.commit()
        db.refresh(db_payout)
        return db_payout
    except IntegrityError as e:
        db.rollback()
        logger.exception("[%s] Integrity error creating payout: %s", function_name, e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Payout already exists")
    except SQLAlchemyError as e:
        db.rollback()
        logger.exception("[%s] DB error creating payout: %s", function_name, e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")
    except Exception as e:
        db.rollback()
        logger.exception("[%s] Unexpected error creating payout: %s", function_name, e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error")


def update_payout_status(db: Session, payout_id: int, new_status: models.PayoutStatus) -> models.Payout:
    function_name = "update_payout_status"

    try:
        db_payout = db.query(models.Payout).filter(models.Payout.id == payout_id).first()
        if not db_payout:
            logger.warning("[%s] Payout not found: %d", function_name, payout_id)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payout not found")

        logger.info("[%s] Updating payout_id=%d status to %s", function_name, payout_id, new_status)
        db_payout.status = new_status
        db.add(db_payout)
        db.commit()
        db.refresh(db_payout)
        return db_payout
    except SQLAlchemyError as e:
        db.rollback()
        logger.exception("[%s] DB error updating payout %d: %s", function_name, payout_id, e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")
    except Exception as e:
        db.rollback()
        logger.exception("[%s] Unexpected error updating payout %d: %s", function_name, payout_id, e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error")


def get_payouts_by_user_paginated(db: Session, user_id: int, offset: int = 0, limit: int = 10) -> Tuple[List[models.Payout], int]:
    function_name = "get_payouts_by_user_paginated"

    try:
        logger.info("[%s] Fetching payouts for user_id=%d offset=%d limit=%d", function_name, user_id, offset, limit)
        query = db.query(models.Payout).filter(models.Payout.user_id == user_id)
        total = query.count()
        payouts = query.order_by(models.Payout.id.desc()).offset(offset).limit(limit).all()
        return payouts, total
    except SQLAlchemyError as e:
        logger.exception("[%s] DB error fetching payouts for user %d: %s", function_name, user_id, e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")
    except Exception as e:
        logger.exception("[%s] Unexpected error fetching payouts for user %d: %s", function_name, user_id, e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error")
