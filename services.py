from models import User
from schema import UserCreate
from typing import List, Optional


class UserService:
    def __init__(self):
        self.storage = {}  # Хранилище пользователей: id -> объект User
        self.next_id = 1   # Следующий доступный ID для нового пользователя

    def create_user(self, data: UserCreate) -> User:
        # Создаём нового пользователя с текущим next_id
        user = User(id=self.next_id, name=data.name, age=data.age)
        # Сохраняем в хранилище по ключу ID
        self.storage[self.next_id] = user
        # Увеличиваем ID для следующего пользователя
        self.next_id += 1
        return user

    def get_all_users(self) -> List[User]:
        # Возвращаем список всех пользователей
        return list(self.storage.values())

    def get_user(self, user_id: int) -> Optional[User]:
        # Получаем пользователя по ID, если он существует
        return self.storage.get(user_id)

    def update_user(self, user_id: int, data: UserCreate) -> Optional[User]:
        # Ищем пользователя по ID
        user = self.storage.get(user_id)
        if user:
            # Обновляем его данные
            user.name = data.name
            user.age = data.age
        return user

    def delete_user(self, user_id: int) -> bool:
        # Удаляем пользователя по ID
        # pop удаляет элемент и возвращает его; если нет — возвращает None
        # Оператор 'is not None' проверяет, был ли элемент найден и удалён
        return self.storage.pop(user_id, None) is not None