from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, Base, engine
from app.schemas import schema
from app.services import services

# Создаём таблицы
Base.metadata.create_all(bind=engine)

app = FastAPI(title="User API", version="0.1")


# Зависимость для получения сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user_service(db: Session = Depends(get_db)) -> services.UserService:
    return services.UserService(db)


def get_product_service(db: Session = Depends(get_db)) -> services.ProductService:
    return services.ProductService(db)


# ============== User Endpoints ==============

@app.post("/users", response_model=schema.UserResponse, status_code=201)
def create_user(
    user_data: schema.UserCreate,
    service: services.UserService = Depends(get_user_service)
):
    user = service.create_user(user_data)
    return schema.UserResponse.model_validate(user)


@app.get("/users", response_model=list[schema.UserResponse])
def get_users(service: services.UserService = Depends(get_user_service)):
    users = service.get_all_users()
    return [schema.UserResponse.model_validate(u) for u in users]


@app.get("/users/{user_id}", response_model=schema.UserResponse)
def get_user(user_id: int, service: services.UserService = Depends(get_user_service)):
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return schema.UserResponse.model_validate(user)


@app.put("/users/{user_id}", response_model=schema.UserResponse)
def update_user(
    user_id: int,
    user_data: schema.UserUpdate,
    service: services.UserService = Depends(get_user_service)
):
    user = service.update_user(user_id, user_data)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return schema.UserResponse.model_validate(user)


@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int, service: services.UserService = Depends(get_user_service)):
    deleted = service.delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Пользователь не найден")


# ============== Product Endpoints ==============

@app.post("/products", response_model=schema.ProductResponse, status_code=201)
def create_product(
    product_data: schema.ProductCreate,
    service: services.ProductService = Depends(get_product_service)
):
    product = service.create_product(product_data)
    return schema.ProductResponse.model_validate(product)


@app.get("/products", response_model=list[schema.ProductResponse])
def get_products(service: services.ProductService = Depends(get_product_service)):
    products = service.get_all_products()
    return [schema.ProductResponse.model_validate(p) for p in products]


@app.get("/products/{product_id}", response_model=schema.ProductResponse)
def get_product(product_id: int, service: services.ProductService = Depends(get_product_service)):
    product = service.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return schema.ProductResponse.model_validate(product)


@app.put("/products/{product_id}", response_model=schema.ProductResponse)
def update_product(
    product_id: int,
    product_data: schema.ProductUpdate,
    service: services.ProductService = Depends(get_product_service)
):
    product = service.update_product(product_id, product_data)
    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return schema.ProductResponse.model_validate(product)


@app.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: int, service: services.ProductService = Depends(get_product_service)):
    deleted = service.delete_product(product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Товар не найден")
