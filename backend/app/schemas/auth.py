from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator

from app.core.constants import PIN_LENGTH, UserRole, UserStatus


class AuthLoginRequest(BaseModel):
    pin: str

    @field_validator("pin")
    @classmethod
    def validate_pin(cls, value: str) -> str:
        if not value.isdigit() or len(value) != PIN_LENGTH:
            raise ValueError(f"PIN must be exactly {PIN_LENGTH} numeric digits.")
        return value


class AuthUserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    role: UserRole
    status: UserStatus
    last_login_at: datetime | None = None
    created_at: datetime
    updated_at: datetime


class AuthLoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: AuthUserResponse


class AuthLogoutResponse(BaseModel):
    message: str = "Logged out successfully."


class AuthMeResponse(BaseModel):
    user: AuthUserResponse