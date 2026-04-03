from collections.abc import Sequence

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, user_id: int) -> User | None:
        statement = select(User).where(User.id == user_id)
        return self.db.scalar(statement)

    def list_users(self, skip: int = 0, limit: int = 100) -> Sequence[User]:
        statement = (
            select(User)
            .order_by(User.created_at.desc(), User.id.desc())
            .offset(skip)
            .limit(limit)
        )
        return self.db.scalars(statement).all()

    def count_users(self) -> int:
        statement = select(func.count(User.id))
        return self.db.scalar(statement) or 0

    def list_all_for_pin_check(self, exclude_user_id: int | None = None) -> Sequence[User]:
        statement = select(User)

        if exclude_user_id is not None:
            statement = statement.where(User.id != exclude_user_id)

        statement = statement.order_by(User.id.asc())
        return self.db.scalars(statement).all()

    def create(self, user: User) -> User:
        self.db.add(user)
        self.db.flush()
        return user

    def save(self, user: User) -> User:
        self.db.add(user)
        self.db.flush()
        return user