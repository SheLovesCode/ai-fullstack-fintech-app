# app/routes/payouts.py
import random
import time
import httpx
import logging

from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session

from app.db import database
from app.models import models
from app.schemas import schemas
from app.services import crud, payment_service, user_service

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/payouts",
    tags=["payouts"]
)

@router.get("/", response_model=schemas.PaginatedPayouts)
def get_payouts(
    pagination: schemas.PaginationRequest = Depends(),
    current_user: models.User = Depends(user_service.get_current_user),
    db: Session = Depends(database.get_db)
):
    try:
        payouts, total = crud.get_payouts_by_user_paginated(
            db=db,
            user_id=current_user.id,
            offset=pagination.offset,
            limit=pagination.limit
        )

        has_more = pagination.offset + len(payouts) < total

        return schemas.PaginatedPayouts(
            payouts=payouts,
            pagination=schemas.PaginationResponse(
                total=total,
                current_offset=pagination.offset,
                has_more=has_more
            )
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Failed to get payouts for user {current_user.id}: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch payouts. Please try again later."
        )


@router.post("/", response_model=schemas.PayoutPublic)
def create_payout(
    payout: schemas.PayoutCreate,
    background_tasks: BackgroundTasks,
    current_user: models.User = Depends(user_service.get_current_user),
    db: Session = Depends(database.get_db)
):
    try:
        new_payout = crud.create_payout_for_user(
            db=db,
            payout=payout,
            user_id=current_user.id
        )

        mock_request_data = {
            "user_id": current_user.id,
            "amount": payout.amount,
            "currency": payout.currency,
            "idempotency_key": new_payout.idempotency_key
        }

        background_tasks.add_task(payment_service.send_payout_to_mock_service, mock_request_data)

        return new_payout
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Failed to create payout for user {current_user.id}: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to create payout. Please try again later."
        )