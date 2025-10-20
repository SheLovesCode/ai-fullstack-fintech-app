import enum
from datetime import datetime
from sqlalchemy import Numeric, Enum as SqlAlchemyEnum, ForeignKey
from sqlalchemy import Column, Integer, String, DateTime, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    oauth_provider = Column(String, nullable=False)
    oauth_id = Column(String, nullable=False, unique=True, index=True)
    email = Column(String, nullable=True, unique=True, index=True)
    full_name = Column(String, nullable=True)
    profile_pic_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    payouts = relationship("Payout", back_populates="owner")

Index('ix_oauth_id', User.oauth_id, unique=True)


class PayoutStatus(str, enum.Enum):
    INITIATED = "INITIATED"
    PENDING = "PENDING"
    IN_TRANSIT = "IN_TRANSIT"
    AUTHORIZED = "AUTHORIZED"
    EXECUTED = "EXECUTED"
    PAID = "PAID"
    BOUNCED = "BOUNCED"
    BLOCKED = "BLOCKED"
    CANCELLED = "CANCELLED"

class Payout(Base):
    __tablename__ = "payouts"

    id = Column(Integer, primary_key=True)
    amount = Column(Numeric(18, 2), nullable=False)
    date = Column(DateTime, default=datetime.now, nullable=False)
    currency = Column(String, nullable=False)
    status = Column(SqlAlchemyEnum(PayoutStatus, native_enum=True), nullable=False, default=PayoutStatus.INITIATED)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="payouts")
    idempotency_key = Column(String, nullable=False, unique=True)