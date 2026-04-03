from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, JSON, String, func, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"
    __table_args__ = (
        Index("ix_audit_logs_actor_user_id", "actor_user_id"),
        Index("ix_audit_logs_module_name", "module_name"),
        Index("ix_audit_logs_action_name", "action_name"),
        Index("ix_audit_logs_created_at", "created_at"),
        Index("ix_audit_logs_target_record", "target_record_type", "target_record_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    actor_user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
    )

    module_name: Mapped[str] = mapped_column(String(50), nullable=False)
    action_name: Mapped[str] = mapped_column(String(50), nullable=False)
    target_record_type: Mapped[str] = mapped_column(String(50), nullable=False)
    target_record_id: Mapped[int] = mapped_column(Integer, nullable=False)

    metadata_json: Mapped[dict | None] = mapped_column("metadata", JSON, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    actor: Mapped["User"] = relationship(
        "User",
        back_populates="audit_logs_created",
    )