import uuid
import logging

from fastapi import APIRouter, Header, HTTPException, Depends
from sqlalchemy.orm import Session

from app.db import database
from app.models import models
from app.schemas import schemas
from app.services import crud, payment_service


router = APIRouter(
    prefix="/webhooks",
    tags=["webhooks"]
)

logger = logging.getLogger("webhooks")
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] [%(correlation_id)s] %(message)s'
)

@router.post("/payments")
async def handle_payment_webhook(
    payload: schemas.WebhookPayload,
    x_mock_signature: str = Header(..., alias="X-Mock-Signature"),
    db: Session = Depends(database.get_db)
):
    correlation_id = payload.request_id or str(uuid.uuid4())

    try:
        valid_signature, old_timestamp = payment_service.verify_webhook_extended(
            payload=payload.model_dump(),
            signature=x_mock_signature
        )

        if not valid_signature:
            logger.error(
                f"Rejected webhook for payout {payload.payout_id} due to INVALID signature",
                extra={"correlation_id": correlation_id}
            )
            raise HTTPException(status_code=400, detail="Invalid signature")

        if old_timestamp:
            logger.warning(
                f"Webhook for payout {payload.payout_id} has OLD timestamp, requesting resend",
                extra={"correlation_id": correlation_id}
            )
            payment_service.request_webhook_resend(payload.payout_id, correlation_id)
            return {"message": "Webhook too old, requested resend"}

        try:
            status_enum = models.PayoutStatus[payload.new_status]
        except KeyError:
            logger.error(
                f"Invalid payout status received: {payload.new_status}",
                extra={"correlation_id": correlation_id}
            )
            raise HTTPException(status_code=400, detail=f"Invalid status value: {payload.new_status}")

        updated_payout = crud.update_payout_status(db=db, payout_id=payload.payout_id, new_status=status_enum)

        if not updated_payout:
            logger.warning(
                f"Payout not found for ID {payload.payout_id}",
                extra={"correlation_id": correlation_id}
            )
            raise HTTPException(status_code=404, detail=f"Payout with id {payload.payout_id} not found")

        logger.info(
            f"Payout {payload.payout_id} status updated to {payload.new_status}",
            extra={"correlation_id": correlation_id}
        )
        return {"message": "Payout status updated successfully"}

    except HTTPException:
        raise
    except Exception as e:
        logger.exception(
            f"Unexpected error handling webhook for payout {payload.payout_id}: {e}",
            extra={"correlation_id": correlation_id}
        )
        raise HTTPException(
            status_code=500,
            detail="Failed to process webhook. Please try again later."
        )
