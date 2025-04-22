from abc import ABC, abstractmethod
from typing import List, Dict, Optional
import bcrypt
from datetime import datetime
from enum import Enum

class Role(Enum):
    USER = "user"
    ADMIN = "admin"

class Account:
    """Отдельная сущность для управления балансом"""
    def __init__(self, user_id: int, initial_balance: float = 0.0):
        self.user_id = user_id
        self.balance = initial_balance
        self.created_at = datetime.now()
    
    def deposit(self, amount: float):
        """Пополнение баланса"""
        if amount <= 0:
            raise ValueError("Сумма пополнения должна быть положительной")
        self.balance += amount
    
    def withdraw(self, amount: float):
        """Списание средств"""
        if amount <= 0:
            raise ValueError("Сумма списания должна быть положительной")
        if self.balance < amount:
            raise ValueError("Недостаточно средств на балансе")
        self.balance -= amount
    
    def __str__(self):
        return f"Account(user_id={self.user_id}, balance={self.balance})"

class User:
    """Сущность пользователя без ответственности за баланс"""
    def __init__(self, user_id: int, username: str, password: str, role: Role = Role.USER):
        self.user_id = user_id
        self.username = username
        self._hashed_password = self._hash_password(password)
        self.role = role
        self.created_at = datetime.now()
    
    @staticmethod
    def _hash_password(password: str) -> bytes:
        """Хеширование пароля с помощью bcrypt"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    def verify_password(self, password: str) -> bool:
        """Проверка пароля"""
        return bcrypt.checkpw(password.encode('utf-8'), self._hashed_password)
    
    def __str__(self):
        return f"User(id={self.user_id}, username={self.username}, role={self.role.value})"

class Admin(User):
    """Администратор системы"""
    def __init__(self, user_id: int, username: str, password: str):
        super().__init__(user_id, username, password, Role.ADMIN)

class MLModel(ABC):
    """Абстрактная модель машинного обучения"""
    @abstractmethod
    def predict(self, data: List[Dict]) -> List[Dict]:
        pass

class ExampleMLModel(MLModel):
    """Пример реализации ML модели"""
    def predict(self, data: List[Dict]) -> List[Dict]:
        return [{"prediction": i % 2, "confidence": 0.95} for i, _ in enumerate(data)]

class PredictionHistory:
    """Сущность для хранения истории предсказаний"""
    def __init__(self):
        self.history = []
    
    def add_prediction(self, task_id: int, user_id: int, input_data: List[Dict], result: List[Dict]):
        """Добавление записи о предсказании"""
        self.history.append({
            "task_id": task_id,
            "user_id": user_id,
            "input_data": input_data,
            "result": result,
            "timestamp": datetime.now()
        })
    
    def get_user_history(self, user_id: int) -> List[Dict]:
        """Получение истории пользователя"""
        return [record for record in self.history if record["user_id"] == user_id]

class MLTask:
    """Задача машинного обучения"""
    TASK_COST = 1.0  # Стоимость выполнения задачи
    
    def __init__(self, task_id: int, user: User, account: Account, data: List[Dict], model: MLModel):
        self.task_id = task_id
        self.user = user
        self.account = account
        self.data = data
        self.model = model
    
    def execute(self) -> List[Dict]:
        """Выполнение задачи с проверкой баланса"""
        if self.account.balance < self.TASK_COST:
            raise ValueError("Недостаточно средств для выполнения задачи")
        
        self.account.withdraw(self.TASK_COST)
        return self.model.predict(self.data)

class TransactionHistory:
    """История финансовых операций"""
    def __init__(self):
        self.transactions = []
    
    def add_transaction(self, user_id: int, account_id: int, amount: float, description: str):
        """Добавление транзакции"""
        self.transactions.append({
            "user_id": user_id,
            "account_id": account_id,
            "amount": amount,
            "description": description,
            "timestamp": datetime.now()
        })
    
    def get_user_transactions(self, user_id: int) -> List[Dict]:
        """Получение транзакций пользователя"""
        return [t for t in self.transactions if t["user_id"] == user_id]
    #   этим коментарием я проаеряю работу с GitHub