from fastapi import FastAPI, HTTPException
from schema import UserCreate, UserResponse
from services import UserService

app = FastAPI(title="User API", version="0.1")

# Создаём экземпляр сервиса
service = UserService()


@app.post("/users", response_model=UserResponse, status_code=201)
def create_user(user_data: UserCreate):
    """Создать нового пользователя"""
    user = service.create_user(user_data)
    return UserResponse(id=user.id, name=user.name, age=user.age)


@app.get("/users", response_model=list[UserResponse])
def get_users():
    """Получить список всех пользователей"""
    return [
        UserResponse(id=u.id, name=u.name, age=u.age)
        for u in service.get_all_users()
    ]


@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    """Получить пользователя по ID"""
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return UserResponse(id=user.id, name=user.name, age=user.age)


@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_data: UserCreate):
    """Обновить данные пользователя"""
    user = service.update_user(user_id, user_data)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return UserResponse(id=user.id, name=user.name, age=user.age)


@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int):
    """Удалить пользователя по ID"""
    deleted = service.delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return  # 204 No Content