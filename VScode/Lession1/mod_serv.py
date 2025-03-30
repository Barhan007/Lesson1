from abc import ABC, abstractmethod
from typing import List, Dict, Optional

# Базовый класс для пользователя
class User:
    def __init__(self, user_id: int, username: str, password: str, balance: float = 0.0, role: str = "user"):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.balance = balance
        self.role = role

    def add_balance(self, amount: float):
        """Пополнение баланса."""
        if amount > 0:
            self.balance += amount
        else:
            raise ValueError("Сумма пополнения должна быть положительной")

    def deduct_balance(self, amount: float):
        """Списание баланса."""
        if self.balance >= amount:
            self.balance -= amount
        else:
            raise ValueError("Недостаточно средств на балансе")

    def __str__(self):
        return f"User(id={self.user_id}, username={self.username}, balance={self.balance}, role={self.role})"

# Класс для администратора (наследование от User)
class Admin(User):
    def __init__(self, user_id: int, username: str, password: str):
        super().__init__(user_id, username, password, role="admin")

    def add_user_balance(self, user: User, amount: float):
        """Пополнение баланса другого пользователя."""
        user.add_balance(amount)

# Абстрактный класс для ML модели
class MLModel(ABC):
    @abstractmethod
    def predict(self, data: List[Dict]) -> List[Dict]:
        """Метод для выполнения предсказания."""
        pass

# Пример конкретной ML модели
class ExampleMLModel(MLModel):
    def predict(self, data: List[Dict]) -> List[Dict]:
        """Пример реализации предсказания."""
        # Здесь должна быть логика предсказания
        return [{"prediction": 1} for _ in data]

# Класс для задачи ML
class MLTask:
    def __init__(self, task_id: int, user: User, data: List[Dict], model: MLModel):
        self.task_id = task_id
        self.user = user
        self.data = data
        self.model = model

    def execute(self):
        """Выполнение задачи."""
        if self.user.balance >= 1.0:  # Условная стоимость задачи
            self.user.deduct_balance(1.0)
            return self.model.predict(self.data)
        else:
            raise ValueError("Недостаточно средств на балансе")

# Класс для истории транзакций
class TransactionHistory:
    def __init__(self):
        self.transactions = []

    def add_transaction(self, user: User, amount: float, description: str):
        """Добавление транзакции в историю."""
        self.transactions.append({
            "user_id": user.user_id,
            "amount": amount,
            "description": description
        })

    def get_user_transactions(self, user: User) -> List[Dict]:
        """Получение транзакций пользователя."""
        return [t for t in self.transactions if t["user_id"] == user.user_id]