from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator

from app.core.constants import PIN_LENGTH, UserRole, UserStatus


class UserBase(BaseModel):
    full_name: str
    role: UserRole

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Full name is required.")
        if len(value) > 255:
            raise ValueError("Full name must not exceed 255 characters.")
        return value


class UserCreateRequest(UserBase):
    pin: str
    status: UserStatus = UserStatus.ACTIVE

    @field_validator("pin")
    @classmethod
    def validate_pin(cls, value: str) -> str:
        if not value.isdigit() or len(value) != PIN_LENGTH:
            raise ValueError(f"PIN must be exactly {PIN_LENGTH} numeric digits.")
        return value


class UserUpdateRequest(BaseModel):
    full_name: str | None = None
    role: UserRole | None = None

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, value: str | None) -> str | None:
        if value is None:
            return value

        value = value.strip()
        if not value:
            raise ValueError("Full name cannot be empty.")
        if len(value) > 255:
            raise ValueError("Full name must not exceed 255 characters.")
        return value


class UserStatusUpdateRequest(BaseModel):
    status: UserStatus


class UserPinUpdateRequest(BaseModel):
    pin: str

    @field_validator("pin")
    @classmethod
    def validate_pin(cls, value: str) -> str:
        if not value.isdigit() or len(value) != PIN_LENGTH:
            raise ValueError(f"PIN must be exactly {PIN_LENGTH} numeric digits.")
        return value


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    role: UserRole
    status: UserStatus
    last_login_at: datetime | None = None
    deactivated_at: datetime | None = None
    created_at: datetime
    updated_at: datetime


class UserListResponse(BaseModel):
    items: list[UserResponse]
    total: int