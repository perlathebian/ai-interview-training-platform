from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate


class AuthService:
    def get_user_by_email(self, db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email).first()

    def create_user(self, db: Session, user_data: UserCreate, password_hash: str) -> User:
        user = User(
            email=user_data.email,
            password_hash=password_hash,
            specialty=user_data.specialty,
            level=user_data.level,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user


auth_service = AuthService()