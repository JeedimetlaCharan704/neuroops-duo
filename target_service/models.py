"""
Data models for OmniPay Gateway & Ledger Service.
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uuid

class PaymentRequest(BaseModel):
    user_id: str = Field(..., description="Unique customer ID")
    amount: float = Field(..., gt=0, description="Payment amount in USD")
    currency: str = Field(default="USD", description="Currency ISO code")
    payment_method: str = Field(..., description="credit_card, ach, or crypto")
    idempotency_key: Optional[str] = Field(default=None, description="Idempotency key for replay protection")

class PaymentResponse(BaseModel):
    transaction_id: str
    status: str
    amount: float
    currency: str
    processed_at: str
    region: str
    carbon_cost_gco2: float

class TransactionRecord(BaseModel):
    id: str
    user_id: str
    amount: float
    currency: str
    status: str
    timestamp: str
    metadata: Optional[dict] = None

class SystemHealth(BaseModel):
    status: str
    version: str
    region: str
    uptime_seconds: float
    carbon_intensity_gco2_kwh: float
    memory_usage_mb: float
    active_connections: int
