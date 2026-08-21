import os
import re
from typing import Any, Dict

import stripe

from .payment_strategy import PaymentStrategy


class CardPayment(PaymentStrategy):

    PROCESSOR_NAME = "stripe"
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
        stripe.api_key = os.environ["STRIPE_SECRET_KEY"]
        try:
            charge = stripe.Charge.create(
                amount=int(amount * 100),
                currency="usd",
                source=transaction_id,
                description=f"ComfyGo payment {transaction_id}",
            )
        except stripe.error.StripeError as exc:
            return {
                "success": False,
                "transaction_id": transaction_id,
                "message": str(exc),
                "processor": self.PROCESSOR_NAME,
            }

        return {
            "success": charge.status == "succeeded",
            "transaction_id": charge.id,
            "message": f"Card payment {charge.status}",
            "processor": self.PROCESSOR_NAME,
            "card_type": charge.payment_method_details.card.brand if charge.payment_method_details else None,
        }

    def refund(self, transaction_id: str, amount: float) -> Dict[str, Any]:
        refund = stripe.Refund.create(
            charge=transaction_id,
            amount=int(amount * 100),
        )

        return {
            "success": refund.status == "succeeded",
            "transaction_id": transaction_id,
            "message": f"Refund {refund.status} via card",
            "processor": self.PROCESSOR_NAME,
            "refund_id": refund.id,
        }

    def verify(self, transaction_id: str) -> Dict[str, Any]:
        charge = stripe.Charge.retrieve(transaction_id)
        return {
            "success": charge.status == "succeeded",
            "transaction_id": transaction_id,
            "message": "Transaction verified",
            "processor": self.PROCESSOR_NAME,
            "status": charge.status,
        }
