from abc import ABC, abstractmethod
from typing import Any, Dict

class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float, transaction_id: str) -> Dict[str, Any]:
        ...

    @abstractmethod
    def refund(self, transaction_id: str, amount: float) -> Dict[str, Any]:
        ...

    @abstractmethod
    def verify(self, transaction_id: str) -> Dict[str, Any]:
        ...