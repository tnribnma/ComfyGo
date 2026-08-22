import re
import random
from typing import Any, Dict

from .payment_strategy import PaymentStrategy

class CardPayment(PaymentStrategy):
    PROCESSOR_NAME = "stripe_simulated"

    @staticmethod
    def _passes_luhn(card_number: str) -> bool:
        digits = [int(d) for d in re.sub(r"\D", "", card_number)]
        if len(digits) < 13:
            return False
        checksum = 0
        parity = len(digits) % 2
        for i, d in enumerate(digits):
            if i % 2 == parity:
                d *= 2
                if d > 9:
                    d -= 9
            checksum += d
        return checksum % 10 == 0

    @staticmethod
    def _detect_card_type(card_number: str) -> str:
        clean = re.sub(r"\D", "", card_number)
        if clean.startswith("4"):
            return "visa"
        if clean[:2] in ("51", "52", "53", "54", "55") or 2221 <= int(clean[:4]) <= 2720:
            return "mastercard"
        if clean.startswith(("34", "37")):
            return "amex"
        return "unknown"

    def pay(self, amount: float, transaction_id: str) -> Dict[str, Any]:
        success = random.random() > 0.05

        if not success:
            return {
                "success": False,
                "transaction_id": transaction_id,
                "message": "Card declined by issuing bank",
                "processor": self.PROCESSOR_NAME,
            }

        return {
            "success": True,
            "transaction_id": transaction_id,
            "message": "Card payment processed successfully",
            "processor": self.PROCESSOR_NAME,
            "card_type": self._detect_card_type(transaction_id),  # demo only
        }

    def refund(self, transaction_id: str, amount: float) -> Dict[str, Any]:
        return {
            "success": True,
            "transaction_id": transaction_id,
            "message": f"Refunded {amount:.2f} via card",
            "processor": self.PROCESSOR_NAME,
        }

    def verify(self, transaction_id: str) -> Dict[str, Any]:
        return {
            "success": True,
            "transaction_id": transaction_id,
            "message": "Transaction verified",
            "processor": self.PROCESSOR_NAME,
            "status": "succeeded",
        }