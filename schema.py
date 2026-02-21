from pydantic import BaseModel, field_validator, ConfigDict
from typing import Optional


class UserCreate(BaseModel):
    name: str
    age: int

    @field_validator("age")
    def validate_age(cls, value):
        if value < 0:
            raise ValueError("Возраст не может быть отрицательным")
        if value > 150:
            raise ValueError("Возраст слишком большой")
        return value

    @field_validator("name")
    def validate_name(cls, value):
        if not value or not value.strip():
            raise ValueError("Имя не может быть пустым или состоять только из пробелов")
        if not value.isalpha():
            raise ValueError("Имя должно содержать только буквы")
        if len(value) < 2:
            raise ValueError("Имя должно быть не менее 2 символов")
        return value.strip().capitalize()


class UserUpdate(UserCreate):
    pass  # Используем те же правила валидации


class UserResponse(BaseModel):
    id: int
    name: str
    age: int

    # Обновлённая конфигурация для Pydantic V2
    model_config = ConfigDict(from_attributes=True)