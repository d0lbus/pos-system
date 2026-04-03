from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.constants import AuditAction, AuditModule, UserStatus
from app.core.security import create_access_token, decode_access_token, verify_pin
from app.repositories.user_repository import UserRepository
from app.services.audit_service import AuditService


class AuthService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.user_repository = UserRepository(db)
        self.audit_service = AuditService(db)

    def _find_user_by_pin(self, pin: str):
        matched_users = []

        for user in self.user_repository.list_all_for_pin_check():
            if verify_pin(pin, user.pin_hash):
                matched_users.append(user)

        if not matched_users:
            return None

        if len(matched_users) > 1:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Duplicate PIN conflict detected. Resolve user PINs first.",
            )

        return matched_users[0]

    def login(self, pin: str) -> dict:
        user = self._find_user_by_pin(pin)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid PIN.",
            )

        if user.status != UserStatus.ACTIVE:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Inactive users cannot log in.",
            )

        user.last_login_at = datetime.now(timezone.utc)
        self.db.flush()

        self.audit_service.log_action(
            actor_user_id=user.id,
            module_name=AuditModule.AUTH.value,
            action_name=AuditAction.LOGIN.value,
            target_record_type="USER",
            target_record_id=user.id,
            metadata={
                "role": user.role.value,
                "status": user.status.value,
            },
        )

        access_token = create_access_token(
            subject=str(user.id),
            extra_claims={
                "role": user.role.value,
                "status": user.status.value,
                "full_name": user.full_name,
            },
        )

        self.db.commit()
        self.db.refresh(user)

        return {
            "access_token": access_token,
            "user": user,
        }

    def logout(self, current_user) -> dict:
        self.audit_service.log_action(
            actor_user_id=current_user.id,
            module_name=AuditModule.AUTH.value,
            action_name=AuditAction.LOGOUT.value,
            target_record_type="USER",
            target_record_id=current_user.id,
            metadata={
                "role": current_user.role.value,
            },
        )

        self.db.commit()

        return {
            "message": "Logged out successfully.",
        }

    def get_current_user_from_token(self, token: str):
        try:
            payload = decode_access_token(token)
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(exc),
            ) from exc

        subject = payload.get("sub")
        if subject is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token subject is missing.",
            )

        try:
            user_id = int(subject)
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token subject.",
            ) from exc

        user = self.user_repository.get_by_id(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found.",
            )

        if user.status != UserStatus.ACTIVE:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Inactive users cannot access protected routes.",
            )

        return user