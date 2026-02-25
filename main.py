from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, Base, engine
from models import User
import schema
import services

# Создаём таблицы
#Base.metadata.create_all(bind=engine)

app = FastAPI(title="User API", version="0.1")


# Зависимость для получения сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users", response_model=schema.UserResponse, status_code=201)
def create_user(user_data: schema.UserCreate, db: Session = Depends(get_db)):
    service = services.UserService(db)
    user = service.create_user(user_data)
    return schema.UserResponse(id=user.id, name=user.name, age=user.age,email = user.email)


@app.get("/users", response_model=list[schema.UserResponse])
def get_users(db: Session = Depends(get_db)):
    service = services.UserService(db)
    users = service.get_all_users()
    return [
        schema.UserResponse(id=u.id, name=u.name, age=u.age,email =u.email)
        for u in users
    ]


@app.get("/users/{user_id}", response_model=schema.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    service = services.UserService(db)
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return schema.UserResponse(id=user.id, name=user.name, age=user.age)


@app.put("/users/{user_id}", response_model=schema.UserResponse)
def update_user(user_id: int, user_data: schema.UserUpdate, db: Session = Depends(get_db)):
    service = services.UserService(db)
    user = service.update_user(user_id, user_data)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return schema.UserResponse(id=user.id, name=user.name, age=user.age)


@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    service = services.UserService(db)
    deleted = service.delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return