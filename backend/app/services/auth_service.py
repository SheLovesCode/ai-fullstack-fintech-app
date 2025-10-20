# app/service/auth_service.py
import base64
import hashlib
import os
import secrets
import urllib.parse

import httpx
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.services import crud
from app.config.config import config
from app.models import models

security = HTTPBearer()

def generate_pkce():
    code_verifier = base64.urlsafe_b64encode(os.urandom(64)).decode("utf-8").rstrip("=")
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode("utf-8")).digest()
    ).decode("utf-8").rstrip("=")
    return code_verifier, code_challenge


def login_google(request: Request):
    state = secrets.token_urlsafe(16)
    nonce = secrets.token_urlsafe(16)
    code_verifier, code_challenge = generate_pkce()

    request.session["state"] = state
    request.session["code_verifier"] = code_verifier

    params = {
        "client_id": config.GOOGLE_CLIENT_ID,
        "response_type": "code",
        "scope": "openid email profile",
        "redirect_uri": config.REDIRECT_URI,
        "state": state,
        "nonce": nonce,
        "code_challenge": code_challenge,
        "code_challenge_method": config.CODE_CHALLENGE,
        "access_type": "offline",
        "prompt": "consent",
    }

    url = config.GOOGLE_ACCOUNTS_BASE_URL + urllib.parse.urlencode(params)
    print(config.REDIRECT_URI)
    return RedirectResponse(url)


async def google_callback(
    request: Request,
    code: str,
    state: str,
    db: Session,
):
    session_state = request.session.get("state") if hasattr(request, "session") else None
    if state != session_state:
        raise HTTPException(status_code=400, detail="Invalid state parameter")

    code_verifier = request.session.get("code_verifier") if hasattr(request, "session") else None
    token_url = config.GOOGLE_AUTH_BASE_URL + "/token"
    user_info_url = "https://www.googleapis.com/oauth2/v3/userinfo"
    data = {
        "client_id": config.GOOGLE_CLIENT_ID,
        "client_secret": config.GOOGLE_CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": config.REDIRECT_URI,
        "code_verifier": code_verifier,
    }

    async with httpx.AsyncClient() as client:
        token_response = await client.post(token_url, data=data)
        token_json = token_response.json()

    if "error" in token_json:
        raise HTTPException(status_code=400, detail=token_json["error"])

    headers = {"Authorization": f"Bearer {token_json['access_token']}"}
    async with httpx.AsyncClient() as client:
        userinfo_response = await client.get(user_info_url, headers=headers)
        userinfo = userinfo_response.json()

    crud.get_or_create_user(db=db, google_profile=userinfo)

    return {
            "access_token": token_json["access_token"],
            "token_type": "Bearer"
        }
