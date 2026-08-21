from typing import Dict, Type

from .payment_strategy import PaymentStrategy
from .card_payment import CardPayment
from .paypal_payment import PayPalPayment
from .bank_transfer_payment import BankTransferPayment
from ..core.exceptions import ValidationError


class PaymentFactory:
    _registry: Dict[str, Type[PaymentStrategy]] = {
        "card":           CardPayment,
        "paypal":         PayPalPayment,
        "bank_transfer":  BankTransferPayment,
    }

    @classmethod
    def create(cls, method: str) -> PaymentStrategy:
        strategy_cls = cls._registry.get(method)
        if strategy_cls is None:
            raise ValidationError(
                f"Unsupported payment method: '{method}'",
                detail=f"Supported methods: {list(cls._registry.keys())}",
            )
        return strategy_cls()

    @classmethod
    def register(cls, method: str, strategy: Type[PaymentStrategy]) -> None:
     
        if not issubclass(strategy, PaymentStrategy):
            raise TypeError(f"{strategy} must inherit from PaymentStrategy")
        cls._registry[method] = strategy

    @classmethod
    def supported_methods(cls) -> list:
        """Return list of all registered payment method keys."""
        return list(cls._registry.keys())