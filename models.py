class User:
    """Модель пользователя (аналог ORM-модели, но в памяти)"""

    def __init__(self, id: int, name: str, age: int):
        self.id = id
        self.name = name
        self.age = age