from sqlalchemy.orm import Session
from app.models.models import User, Product
from app.schemas.schema import UserCreate, ProductCreate, ProductUpdate


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
            db_user.email = data.email
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


class ProductService:
    def __init__(self, db: Session):
        self.db = db

    def create_product(self, data: ProductCreate) -> Product:
        db_product = Product(
            name=data.name,
            description=data.description,
            price=data.price,
            in_stock=data.in_stock
        )
        self.db.add(db_product)
        self.db.commit()
        self.db.refresh(db_product)
        return db_product

    def get_all_products(self) -> list[Product]:
        return self.db.query(Product).all()

    def get_product(self, product_id: int) -> Product | None:
        return self.db.query(Product).filter(Product.id == product_id).first()

    def update_product(self, product_id: int, data: ProductUpdate) -> Product | None:
        db_product = self.get_product(product_id)
        if db_product:
            if data.name is not None:
                db_product.name = data.name
            if data.description is not None:
                db_product.description = data.description
            if data.price is not None:
                db_product.price = data.price
            if data.in_stock is not None:
                db_product.in_stock = data.in_stock
            self.db.commit()
            self.db.refresh(db_product)
        return db_product

    def delete_product(self, product_id: int) -> bool:
        db_product = self.get_product(product_id)
        if db_product:
            self.db.delete(db_product)
            self.db.commit()
            return True
        return False
