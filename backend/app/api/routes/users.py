from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps.auth import require_admin
from app.db.session import get_db
from app.schemas.user import (
    UserCreateRequest,
    UserListResponse,
    UserPinUpdateRequest,
    UserResponse,
    UserStatusUpdateRequest,
    UserUpdateRequest,
)
from app.services.user_service import UserService


router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/",
    response_model=UserListResponse,
    status_code=status.HTTP_200_OK,
)
def list_users(
    skip: int = 0,
    limit: int = 100,
    current_admin=Depends(require_admin),
    db: Session = Depends(get_db),
):
    user_service = UserService(db)
    users, total = user_service.list_users(skip=skip, limit=limit)

    return UserListResponse(
        items=users,
        total=total,
    )


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    payload: UserCreateRequest,
    current_admin=Depends(require_admin),
    db: Session = Depends(get_db),
):
    user_service = UserService(db)
    return user_service.create_user(payload, actor_user_id=current_admin.id)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
def get_user(
    user_id: int,
    current_admin=Depends(require_admin),
    db: Session = Depends(get_db),
):
    user_service = UserService(db)
    return user_service.get_user_or_404(user_id)


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
def update_user(
    user_id: int,
    payload: UserUpdateRequest,
    current_admin=Depends(require_admin),
    db: Session = Depends(get_db),
):
    user_service = UserService(db)
    return user_service.update_user(
        user_id=user_id,
        payload=payload,
        actor_user_id=current_admin.id,
    )


@router.patch(
    "/{user_id}/status",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
def update_user_status(
    user_id: int,
    payload: UserStatusUpdateRequest,
    current_admin=Depends(require_admin),
    db: Session = Depends(get_db),
):
    user_service = UserService(db)
    return user_service.update_user_status(
        user_id=user_id,
        payload=payload,
        actor_user_id=current_admin.id,
    )


@router.patch(
    "/{user_id}/pin",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
def reset_user_pin(
    user_id: int,
    payload: UserPinUpdateRequest,
    current_admin=Depends(require_admin),
    db: Session = Depends(get_db),
):
    user_service = UserService(db)
    return user_service.reset_user_pin(
        user_id=user_id,
        payload=payload,
        actor_user_id=current_admin.id,
    )