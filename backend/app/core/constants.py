from enum import StrEnum


PIN_LENGTH = 6


class UserRole(StrEnum):
    ADMIN = "ADMIN"
    CASHIER = "CASHIER"


class UserStatus(StrEnum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class AuditModule(StrEnum):
    AUTH = "AUTH"
    USERS = "USERS"


class AuditAction(StrEnum):
    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    ACTIVATE = "ACTIVATE"
    DEACTIVATE = "DEACTIVATE"
    RESET_PIN = "RESET_PIN"


ALLOWED_USER_ROLES = {role.value for role in UserRole}
ALLOWED_USER_STATUSES = {status.value for status in UserStatus}