from .config import Config
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
import uuid
from decimal import Decimal

class PayoutCreate(BaseModel):
    user_id: int
    amount: float
    currency: str
    idempotency_key: uuid.UUID

    @field_validator("user_id")
    def validate_ids(cls, v, field):
        if not isinstance(v, int) or v <= 0:
            raise ValueError(f"{field.name} must be a positive integer")
        return v

    @field_validator("amount")
    def validate_amount(cls, v):
        if not isinstance(v, (float, int, Decimal)) or v <= 0:
            raise ValueError("Amount must be a positive number")
        return float(v)

    @field_validator("currency")
    def validate_currency(cls, v):
        if v not in Config.VALID_CURRENCIES:
            raise ValueError(f"Invalid currency: {v}. Must be one of {Config.VALID_CURRENCIES}")
        return v


class WebhookPayloadModel(BaseModel):
    payout_id: int = Field(..., description="ID of the payout")
    new_status: str = Field(..., description="New payout status")
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique request ID")
    timestamp: int = Field(default_factory=lambda: int(datetime.utcnow().timestamp()), description="Unix timestamp of webhook")

    @field_validator("new_status")
    def validate_status(cls, v):
        if not isinstance(v, str):
            raise TypeError(f"'new_status' must be a string, got {type(v).__name__}")
        v_upper = v.upper()
        if v_upper not in Config.MOCK_PAYOUT_STATUSES:
            raise ValueError(f"Invalid payout status '{v_upper}'. Must be one of {Config.MOCK_PAYOUT_STATUSES}")
        return v_upper

    @field_validator("timestamp")
    def validate_timestamp(cls, v):
        if v <= 0:
            raise ValueError("Timestamp must be a positive integer")
        return v

class CreatePayoutResponse(BaseModel):
    payout_id: int
    user_id: int
    amount: float
    currency: str
    status: str
    idempotency_key: uuid.UUID

    @field_validator("payout_id", "user_id")
    def validate_ids(cls, v, field):
        if not isinstance(v, int) or v <= 0:
            raise ValueError(f"{field.name} must be a positive integer")
        return v

    @field_validator("amount")
    def validate_amount(cls, v):
        if not isinstance(v, (float, int, Decimal)) or v <= 0:
            raise ValueError("Amount must be a positive number")
        return float(v)

    @field_validator("currency")
    def validate_currency(cls, v):
        if v not in Config.VALID_CURRENCIES:
            raise ValueError(f"Invalid currency: {v}. Must be one of {Config.VALID_CURRENCIES}")
        return v

    @field_validator("status")
    def validate_status(cls, v):
        if not isinstance(v, str):
            raise TypeError(f"'new_status' must be a string, got {type(v).__name__}")
        v_upper = v.upper()
        if v_upper not in Config.MOCK_PAYOUT_STATUSES:
            raise ValueError(f"Invalid payout status '{v_upper}'. Must be one of {Config.MOCK_PAYOUT_STATUSES}")
        return v_upper

