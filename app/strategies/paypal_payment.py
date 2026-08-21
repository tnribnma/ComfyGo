import re
import os
from typing import Any, Dict

import paypalrestsdk as paypal

from .payment_strategy import PaymentStrategy


class PayPalPayment(PaymentStrategy):
    """Strategy for processing PayPal payments."""

    PROCESSOR_NAME = "paypal"

    @staticmethod
    def _is_valid_email(email: str) -> bool:
        pattern = r"^[\w\.\+\-]+@[\w]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))

    def pay(self, amount: float, transaction_id: str) -> Dict[str, Any]:
        paypal.configure({
            "mode": os.getenv("PAYPAL_MODE", "sandbox"),
            "client_id": os.environ["PAYPAL_CLIENT_ID"],
            "client_secret": os.environ["PAYPAL_CLIENT_SECRET"],
        })
        payment = paypal.Payment({
            "intent": "sale",
            "payer": {"payment_method": "paypal"},
            "transactions": [{
                "amount": {"total": f"{amount:.2f}", "currency": "USD"},
                "description": f"ComfyGo payment {transaction_id}",
                "invoice_number": transaction_id,
            }],
            "redirect_urls": {
                "return_url": os.getenv("PAYPAL_RETURN_URL", "http://localhost:5500/paypal/success"),
                "cancel_url": os.getenv("PAYPAL_CANCEL_URL", "http://localhost:5500/paypal/cancel"),
            },
        })

        if not payment.create():
            return {
                "success": False,
                "transaction_id": transaction_id,
                "message": str(payment.error),
                "processor": self.PROCESSOR_NAME,
            }

        return {
            "success": True,
            "transaction_id": payment.id,
            "message": "PayPal payment created successfully",
            "processor": self.PROCESSOR_NAME,
            "approval_url": next(
                (link.href for link in payment.links if link.rel == "approval_url"),
                None,
            ),
        }

    def refund(self, transaction_id: str, amount: float) -> Dict[str, Any]:
        paypal.configure({
            "mode": os.getenv("PAYPAL_MODE", "sandbox"),
            "client_id": os.environ["PAYPAL_CLIENT_ID"],
            "client_secret": os.environ["PAYPAL_CLIENT_SECRET"],
        })
        sale = paypal.Sale.find(transaction_id)
        if not sale.refund({"amount": {"total": f"{amount:.2f}", "currency": "USD"}}):
            return {
                "success": False,
                "transaction_id": transaction_id,
                "message": str(sale.error),
                "processor": self.PROCESSOR_NAME,
            }

        return {
            "success": True,
            "transaction_id": transaction_id,
            "message": f"Refunded {amount:.2f} via PayPal",
            "processor": self.PROCESSOR_NAME,
        }

    def verify(self, transaction_id: str) -> Dict[str, Any]:
        paypal.configure({
            "mode": os.getenv("PAYPAL_MODE", "sandbox"),
            "client_id": os.environ["PAYPAL_CLIENT_ID"],
            "client_secret": os.environ["PAYPAL_CLIENT_SECRET"],
        })
        payment = paypal.Payment.find(transaction_id)
        return {
            "success": payment.state == "approved",
            "transaction_id": transaction_id,
            "message": "PayPal transaction verified",
            "processor": self.PROCESSOR_NAME,
            "status": payment.state,
        }
