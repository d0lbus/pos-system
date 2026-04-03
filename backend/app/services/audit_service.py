from typing import Any

from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog


class AuditService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def log_action(
        self,
        *,
        actor_user_id: int,
        module_name: str,
        action_name: str,
        target_record_type: str,
        target_record_id: int,
        metadata: dict[str, Any] | None = None,
    ) -> AuditLog:
        audit_log = AuditLog(
            actor_user_id=actor_user_id,
            module_name=module_name,
            action_name=action_name,
            target_record_type=target_record_type,
            target_record_id=target_record_id,
            metadata_json=metadata,
        )

        self.db.add(audit_log)
        self.db.flush()
        return audit_log