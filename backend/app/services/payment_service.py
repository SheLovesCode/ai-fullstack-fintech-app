import time
import hmac
import hashlib
import json
import logging
import httpx

from typing import Dict, Optional, Tuple
from decimal import Decimal

from app.config.config import config
from app.services import crud


logger = logging.getLogger("payment_service")
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] [%(message)s]')

timestamp_retry_store: Dict[str, int] = {}


def send_payout_to_mock_service(payout_data: Dict) -> Optional[Dict]:
    try:
        json_payload = {
            k: float(v) if isinstance(v, Decimal) else v
            for k, v in payout_data.items()
        }

        response = httpx.post(
            f"{config.MOCK_PAYMENTS_URL}/mock/payouts",
            json=json_payload,
            timeout=5
        )
        response.raise_for_status()
        logger.info(
            f"Payout sent to mock service: {response.json()}",
            extra={"correlation_id": payout_data.get("idempotency_key")}
        )
        return response.json()
    except httpx.RequestError as e:
        logger.error(f"[MockService] Request failed: {e}")
        return None
    except httpx.HTTPStatusError as e:
        logger.error(f"[MockService] HTTP error: {e}")
        return None



def verify_webhook(payload: dict, signature: str) -> bool:
    timestamp = payload.get("timestamp")
    if not timestamp or abs(int(time.time()) - timestamp) > config.MAX_WEBHOOK_AGE:
        logger.warning(f"Webhook timestamp invalid or too old: {timestamp}")
        return False

    payload_bytes = json.dumps(payload, sort_keys=True, separators=(',', ':')).encode('utf-8')
    expected_sig = hmac.new(config.MOCK_PAYMENTS_CALLBACK_SECRET.encode(), payload_bytes, hashlib.sha256).hexdigest()
    valid = hmac.compare_digest(signature, expected_sig)
    if not valid:
        logger.warning("Webhook signature invalid")
    return valid

def verify_webhook_extended(payload: Dict[str, any], signature: str) -> Tuple[bool, bool]:
    timestamp = payload.get("timestamp")
    is_timestamp_old = False

    if not timestamp:
        is_timestamp_old = True
    elif abs(int(time.time()) - int(timestamp)) > config.MAX_WEBHOOK_AGE:
        is_timestamp_old = True

    payload_bytes = json.dumps(payload, sort_keys=True, separators=(',', ':')).encode('utf-8')
    expected_sig = hmac.new(config.MOCK_PAYMENTS_CALLBACK_SECRET.encode(), payload_bytes, hashlib.sha256).hexdigest()
    is_signature_valid = hmac.compare_digest(signature, expected_sig)

    return is_signature_valid, is_timestamp_old


def request_webhook_resend(payout_id: int, correlation_id: str) -> bool:
    key = f"{correlation_id}:{payout_id}"
    retries = timestamp_retry_store.get(key, 0)

    if retries >= config.MAX_TIMESTAMP_RETRIES:
        logger.warning(
            f"Max retries reached for payout {payout_id} with correlation {correlation_id}. Not requesting again.",
            extra={"correlation_id": correlation_id}
        )
        return False

    timestamp_retry_store[key] = retries + 1

    try:
        response = httpx.post(
            f"{config.MOCK_PAYMENTS_URL}/mock/resend",
            json={"payout_id": payout_id, "request_id": correlation_id},
            timeout=5
        )
        response.raise_for_status()
        logger.info(
            f"Requested resend for payout {payout_id} (attempt {retries + 1})",
            extra={"correlation_id": correlation_id}
        )
        return True

    except httpx.RequestError as e:
        logger.error(
            f"Request failed while attempting webhook resend for payout {payout_id}: {e}",
            extra={"correlation_id": correlation_id}
        )
    except httpx.HTTPStatusError as e:
        logger.error(
            f"HTTP error when requesting webhook resend for payout {payout_id}: {e}",
            extra={"correlation_id": correlation_id}
        )

    return False


