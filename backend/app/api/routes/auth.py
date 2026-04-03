from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps.auth import get_current_user
from app.db.session import get_db
from app.schemas.auth import (
    AuthLoginRequest,
    AuthLoginResponse,
    AuthLogoutResponse,
    AuthMeResponse,
)
from app.services.auth_service import AuthService


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/login",
    response_model=AuthLoginResponse,
    status_code=status.HTTP_200_OK,
)
def login(
    payload: AuthLoginRequest,
    db: Session = Depends(get_db),
):
    auth_service = AuthService(db)
    result = auth_service.login(payload.pin)

    return AuthLoginResponse(
        access_token=result["access_token"],
        user=result["user"],
    )


@router.post(
    "/logout",
    response_model=AuthLogoutResponse,
    status_code=status.HTTP_200_OK,
)
def logout(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    auth_service = AuthService(db)
    result = auth_service.logout(current_user)

    return AuthLogoutResponse(**result)


@router.get(
    "/me",
    response_model=AuthMeResponse,
    status_code=status.HTTP_200_OK,
)
def me(current_user=Depends(get_current_user)):
    return AuthMeResponse(user=current_user)