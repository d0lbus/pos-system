from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Enum, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.constants import UserRole, UserStatus

from app.db.base_class import Base


def enum_values(enum_cls):
    return [member.value for member in enum_cls]


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    full_name: Mapped[str] = mapped_column(String(255), nullable=False)

    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, native_enum=False, values_callable=enum_values),
        nullable=False,
    )

    pin_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    status: Mapped[UserStatus] = mapped_column(
        Enum(UserStatus, native_enum=False, values_callable=enum_values),
        nullable=False,
        default=UserStatus.ACTIVE,
        server_default=UserStatus.ACTIVE.value,
    )

    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    deactivated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    audit_logs_created: Mapped[list["AuditLog"]] = relationship(
        "AuditLog",
        back_populates="actor",
        passive_deletes=True,
    )