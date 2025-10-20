from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field, field_validator, EmailStr
from typing import List

from app.config.config import config
from app.models import models

class UserPublic(BaseModel):
    id: int
    email: EmailStr
    full_name: str | None = Field(None, max_length=255)
    profile_pic_url: str | None = Field(None, max_length=255)

    model_config = ConfigDict(from_attributes=True)

class PayoutCreate(BaseModel):
    amount: Decimal = Field(..., gt=0, le=1000000, description="Amount must be > 0 and <= 1,000,000")
    currency: str
    idempotency_key: str

    @field_validator("currency")
    def validate_currency(cls, v):
        if v not in config.VALID_CURRENCIES:
            raise ValueError(f"Invalid currency: {v}. Must be one of {config.VALID_CURRENCIES}")
        return v

class PayoutPublic(BaseModel):
    amount: Decimal = Field(..., gt=0, le=1000000, description="Amount must be > 0 and <= 1,000,000")
    currency: str
    status: models.PayoutStatus
    date: datetime

    model_config = ConfigDict(from_attributes=True)

    @field_validator("currency")
    def validate_currency(cls, v):
        if v not in config.VALID_CURRENCIES:
            raise ValueError(f"Invalid currency: {v}. Must be one of {config.VALID_CURRENCIES}")
        return v

    @field_validator("status")
    def validate_status(cls, v):
        if not isinstance(v, models.PayoutStatus):
            raise ValueError(f"Invalid status: {v}. Must be a valid PayoutStatus")
        return v

class PaginationRequest(BaseModel):
    offset: int = Field(0, ge=0, description="Offset, must be ≥ 0")
    limit: int = Field(10, ge=1, le=50, description="Items per page, 1–50")

class PaginationResponse(BaseModel):
    total: int
    current_offset: int
    has_more: bool

    class Config:
        allow_population_by_field_name = True

class PaginatedPayouts(BaseModel):
    payouts: List[PayoutPublic]
    pagination: PaginationResponse

class WebhookPayload(BaseModel):
    payout_id: int
    new_status: str
    request_id: str
    timestamp: int

    @field_validator("new_status")
    def validate_new_status(cls, v):
        try:
            models.PayoutStatus(v)
        except ValueError:
            raise ValueError(f"Invalid status: {v}. Must be one of {[status.value for status in models.PayoutStatus]}")
        return v

    @field_validator("timestamp")
    def validate_timestamp(cls, v):
        if v <= 0:
            raise ValueError("Timestamp must be a positive integer")
        return v

class CurrenciesResponse(BaseModel):
    currencies: List[str]

    @field_validator("currencies", mode="before")
    def validate_currencies(cls, v):
        if not isinstance(v, list):
            raise ValueError("currencies must be a list")
        invalid = [c for c in v if c not in config.VALID_CURRENCIES]
        if invalid:
            raise ValueError(f"Invalid currencies found: {invalid}. Must be one of {config.VALID_CURRENCIES}")
        return v
