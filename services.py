from sqlalchemy.orm import Session
from models import User
from schema import UserCreate


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, data: UserCreate) -> User:
        db_user = User(name=data.name, age=data.age, email=data.email)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_all_users(self) -> list[User]:
        return self.db.query(User).all()

    def get_user(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def update_user(self, user_id: int, data: UserCreate) -> User | None:
        db_user = self.get_user(user_id)
        if db_user:
            db_user.name = data.name
            db_user.age = data.age
            self.db.commit()
            self.db.refresh(db_user)
        return db_user

    def delete_user(self, user_id: int) -> bool:
        db_user = self.get_user(user_id)
        if db_user:
            self.db.delete(db_user)
            self.db.commit()
            return True
        return False