import httpx

from fastapi import HTTPException, status, Depends, Cookie
from sqlalchemy.orm import Session

from app.services import crud
from app.config.config import config
from app.models import models
from app.db import database

async def get_current_user(
    access_token: str = Cookie(None),
    db: Session = Depends(database.get_db),
) -> models.User:
    user_info_url = "https://www.googleapis.com/oauth2/v3/userinfo"

    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authenticated",
        )

    async with httpx.AsyncClient() as client:
        resp = await client.get(
            user_info_url,
            headers={"Authorization": f"Bearer {access_token}"},
        )

    if resp.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    userinfo = resp.json()
    user = crud.get_or_create_user(db=db, google_profile=userinfo)
    print(user)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user