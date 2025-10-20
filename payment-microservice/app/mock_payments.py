# mock_payments-microservice
import hashlib
import hmac
import json
import logging
import random
import threading
import time
import uuid
from decimal import Decimal
from typing import Dict

import httpx
from fastapi import FastAPI

from .config import Config
from .schemas import PayoutCreate, WebhookPayloadModel, CreatePayoutResponse

app = FastAPI(title="Mock Payments Microservice")

class SafeFormatter(logging.Formatter):
    def format(self, record):
        if not hasattr(record, "correlation_id"):
            record.correlation_id = "N/A"
        return super().format(record)

class CorrelationFilter(logging.Filter):
    def filter(self, record):
        if not hasattr(record, "correlation_id") or record.correlation_id is None:
            record.correlation_id = "N/A"
        return True

logging.basicConfig(level=logging.INFO)
logging.getLogger().addFilter(CorrelationFilter())

formatter = SafeFormatter('[%(asctime)s] [%(levelname)s] [%(correlation_id)s] %(message)s')
for handler in logging.getLogger().handlers:
    handler.setFormatter(formatter)


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)

payout_store: Dict[str, dict] = {}
store_lock = threading.Lock()


def sign_payload(payload: dict, secret: str) -> (str, dict):
    payload_with_ts = payload.copy()
    payload_with_ts["timestamp"] = int(time.time())
    payload_bytes = json.dumps(payload_with_ts, sort_keys=True, separators=(',', ':')).encode('utf-8')
    signature = hmac.new(secret.encode('utf-8'), payload_bytes, hashlib.sha256).hexdigest()
    return signature, payload_with_ts


def simulate_webhook(payout_data: dict, correlation_id: str):
    delay = random.uniform(Config.WEBHOOK_DELAY_MIN, Config.WEBHOOK_DELAY_MAX)
    logging.info(f"Simulating webhook in {delay:.2f}s for payout {payout_data['payout_id']}",
                 extra={"correlation_id": correlation_id})
    time.sleep(delay)

    new_status = random.choice(Config.MOCK_PAYOUT_STATUSES)
    payload = {
        "payout_id": payout_data["payout_id"],
        "new_status": new_status,
        "request_id": correlation_id
    }

    send_webhook(payload, Config.WEBHOOK_CALLBACK_SECRET, correlation_id)


def send_webhook(payload: dict, secret: str, correlation_id: str = "N/A", attempt: int = 1):
    try:
        validated_payload = WebhookPayloadModel(**payload).model_dump()
    except Exception as e:
        logging.error(f"Invalid webhook payload for payout {payload.get('payout_id')}: {e}",
                      extra={"correlation_id": correlation_id})
        return

    signature, payload_with_ts = sign_payload(validated_payload, secret)
    headers = {"X-Mock-Signature": signature}

    try:
        logging.info(
            f"[Attempt {attempt}] Webhook sent for payout {payload['payout_id']} -> {payload_with_ts['new_status']}",
            extra={"correlation_id": correlation_id}
        )

        response = httpx.post(
            Config.MOCK_CALLBACK_URL,
            json=payload_with_ts,
            headers=headers,
            timeout=5
        )
        response.raise_for_status()
        logging.info(f"Webhook sent for payout {payload['payout_id']} -> {payload_with_ts['new_status']}",
                     extra={"correlation_id": correlation_id})

        with store_lock:
            if payload["payout_id"] in payout_store:
                payout_store[payload["payout_id"]]["status"] = payload_with_ts["new_status"]

    except (httpx.RequestError, httpx.HTTPStatusError) as e:
        if attempt <= Config.WEBHOOK_RETRY_ATTEMPTS:
            delay = (2 ** attempt) + random.uniform(0, 0.5)
            logging.warning(f"[Attempt {attempt}] Webhook failed, retrying in {delay:.2f}s: {e}",
                            extra={"correlation_id": correlation_id})
            time.sleep(delay)
            send_webhook(payload, secret, correlation_id, attempt + 1)
        else:
            logging.error(f"Webhook permanently failed after {attempt - 1} retries: {e}",
                          extra={"correlation_id": correlation_id})


@app.post("/mock/payouts", response_model=CreatePayoutResponse)
def create_payout(payout: PayoutCreate):
    correlation_id = str(uuid.uuid4())

    with store_lock:
        if payout.idempotency_key in payout_store:
            return payout_store[payout.idempotency_key]

        payout_data = {
            "payout_id": len(payout_store) + 1,
            "user_id": getattr(payout, "user_id", 1),
            "amount": payout.amount,
            "currency": payout.currency,
            "status": "PENDING",
            "idempotency_key": payout.idempotency_key,
        }
        payout_store[payout.idempotency_key] = payout_data

    threading.Thread(target=simulate_webhook, args=(payout_data, correlation_id), daemon=True).start()
    logging.info(f"Created payout {payout_data['payout_id']} for user {payout_data['user_id']}",
                 extra={"correlation_id": correlation_id})
    return payout_data
