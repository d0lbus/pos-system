from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.constants import (
    AuditAction,
    AuditModule,
    UserStatus,
)
from app.core.security import hash_pin, verify_pin
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import (
    UserCreateRequest,
    UserPinUpdateRequest,
    UserStatusUpdateRequest,
    UserUpdateRequest,
)
from app.services.audit_service import AuditService


class UserService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.user_repository = UserRepository(db)
        self.audit_service = AuditService(db)

    def list_users(self, skip: int = 0, limit: int = 100) -> tuple[list[User], int]:
        users = list(self.user_repository.list_users(skip=skip, limit=limit))
        total = self.user_repository.count_users()
        return users, total

    def get_user_or_404(self, user_id: int) -> User:
        user = self.user_repository.get_by_id(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found.",
            )
        return user

    def _ensure_pin_is_unique(self, pin: str, exclude_user_id: int | None = None) -> None:
        for existing_user in self.user_repository.list_all_for_pin_check(
            exclude_user_id=exclude_user_id
        ):
            if verify_pin(pin, existing_user.pin_hash):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="PIN is already in use by another user.",
                )

    def create_user(self, payload: UserCreateRequest, actor_user_id: int) -> User:
        self._ensure_pin_is_unique(payload.pin)

        deactivated_at = None
        if payload.status == UserStatus.INACTIVE:
            deactivated_at = datetime.now(timezone.utc)

        user = User(
            full_name=payload.full_name,
            role=payload.role,
            pin_hash=hash_pin(payload.pin),
            status=payload.status,
            deactivated_at=deactivated_at,
        )

        self.user_repository.create(user)

        self.audit_service.log_action(
            actor_user_id=actor_user_id,
            module_name=AuditModule.USERS.value,
            action_name=AuditAction.CREATE.value,
            target_record_type="USER",
            target_record_id=user.id,
            metadata={
                "full_name": user.full_name,
                "role": user.role.value,
                "status": user.status.value,
            },
        )

        self.db.commit()
        self.db.refresh(user)
        return user

    def update_user(
        self,
        user_id: int,
        payload: UserUpdateRequest,
        actor_user_id: int,
    ) -> User:
        user = self.get_user_or_404(user_id)

        changes: dict[str, dict[str, str]] = {}

        if payload.full_name is not None and payload.full_name != user.full_name:
            changes["full_name"] = {
                "old": user.full_name,
                "new": payload.full_name,
            }
            user.full_name = payload.full_name

        if payload.role is not None and payload.role != user.role:
            changes["role"] = {
                "old": user.role.value,
                "new": payload.role.value,
            }
            user.role = payload.role

        if not changes:
            return user

        self.user_repository.save(user)

        self.audit_service.log_action(
            actor_user_id=actor_user_id,
            module_name=AuditModule.USERS.value,
            action_name=AuditAction.UPDATE.value,
            target_record_type="USER",
            target_record_id=user.id,
            metadata={
                "changes": changes,
            },
        )

        self.db.commit()
        self.db.refresh(user)
        return user

    def update_user_status(
        self,
        user_id: int,
        payload: UserStatusUpdateRequest,
        actor_user_id: int,
    ) -> User:
        user = self.get_user_or_404(user_id)

        if user.status == payload.status:
            return user

        previous_status = user.status

        user.status = payload.status
        if payload.status == UserStatus.INACTIVE:
            user.deactivated_at = datetime.now(timezone.utc)
            action_name = AuditAction.DEACTIVATE.value
        else:
            user.deactivated_at = None
            action_name = AuditAction.ACTIVATE.value

        self.user_repository.save(user)

        self.audit_service.log_action(
            actor_user_id=actor_user_id,
            module_name=AuditModule.USERS.value,
            action_name=action_name,
            target_record_type="USER",
            target_record_id=user.id,
            metadata={
                "old_status": previous_status.value,
                "new_status": user.status.value,
            },
        )

        self.db.commit()
        self.db.refresh(user)
        return user

    def reset_user_pin(
        self,
        user_id: int,
        payload: UserPinUpdateRequest,
        actor_user_id: int,
    ) -> User:
        user = self.get_user_or_404(user_id)

        self._ensure_pin_is_unique(payload.pin, exclude_user_id=user.id)

        user.pin_hash = hash_pin(payload.pin)
        self.user_repository.save(user)

        self.audit_service.log_action(
            actor_user_id=actor_user_id,
            module_name=AuditModule.USERS.value,
            action_name=AuditAction.RESET_PIN.value,
            target_record_type="USER",
            target_record_id=user.id,
            metadata={
                "full_name": user.full_name,
            },
        )

        self.db.commit()
        self.db.refresh(user)
        return user