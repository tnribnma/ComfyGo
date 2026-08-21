import json
import os
import re
from decimal import Decimal, InvalidOperation
from typing import Any, Dict
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .payment_strategy import PaymentStrategy


class BankTransferPayment(PaymentStrategy):
    PROCESSOR_NAME = "bank_simulated"

    @staticmethod
    def _is_valid_reference(reference: str) -> bool:
        """Bank reference numbers are typically 8–20 alphanumeric chars."""
        clean = re.sub(r"\s", "", reference)
        return bool(re.match(r"^[A-Z0-9]{8,20}$", clean, re.IGNORECASE))

    def pay(self, amount: float, transaction_id: str) -> Dict[str, Any]:

        if not self._is_valid_reference(transaction_id):
            return {
                "success": False,
                "transaction_id": transaction_id,
                "message": "Invalid bank transfer reference format",
                "processor": self.PROCESSOR_NAME,
            }

        reconciliation_url = os.getenv("BANK_RECONCILIATION_URL")
        if not reconciliation_url:
            return {
                "success": False,
                "transaction_id": transaction_id,
                "message": "Bank reconciliation service is not configured",
                "processor": self.PROCESSOR_NAME,
            }

        try:
            expected_amount = Decimal(str(amount)).quantize(Decimal("0.01"))
            payload = json.dumps({
                "reference": transaction_id,
                "amount": str(expected_amount),
            }).encode("utf-8")
            headers = {"Content-Type": "application/json"}
            api_key = os.getenv("BANK_RECONCILIATION_API_KEY")
            if api_key:
                headers["Authorization"] = f"Bearer {api_key}"

            request = Request(
                reconciliation_url.rstrip("/") + "/reconcile",
                data=payload,
                headers=headers,
                method="POST",
            )
            with urlopen(request, timeout=3) as response:
                reconciliation = json.load(response)

            received_amount = Decimal(str(reconciliation["amount"])).quantize(Decimal("0.01"))
            status = str(reconciliation.get("status", "")).lower()
        except (HTTPError, URLError, OSError, ValueError, KeyError, InvalidOperation):
            return {
                "success": False,
                "transaction_id": transaction_id,
                "message": "Unable to reconcile bank transfer",
                "processor": self.PROCESSOR_NAME,
            }

        if status not in {"settled", "confirmed", "completed"} or received_amount != expected_amount:
            return {
                "success": False,
                "transaction_id": transaction_id,
                "message": "Bank transfer is not settled for the expected amount",
                "processor": self.PROCESSOR_NAME,
            }

        return {
            "success": True,
            "transaction_id": transaction_id,
            "message": "Bank transfer verified and confirmed",
            "processor": self.PROCESSOR_NAME,
            "bank_name": reconciliation.get("bank_name", "Bank transfer"),
        }

    def refund(self, transaction_id: str, amount: float) -> Dict[str, Any]:
        return {
            "success": True,
            "transaction_id": transaction_id,
            "message": f"Initiated bank refund of {amount:.2f}",
            "processor": self.PROCESSOR_NAME,
            "refund_reference": f"RFD-{transaction_id[-6:]}",
        }

    def verify(self, transaction_id: str) -> Dict[str, Any]:
        if not self._is_valid_reference(transaction_id):
            return {
                "success": False,
                "transaction_id": transaction_id,
                "message": "Reference not found",
                "processor": self.PROCESSOR_NAME,
            }
        return {
            "success": True,
            "transaction_id": transaction_id,
            "message": "Bank transfer confirmed",
            "processor": self.PROCESSOR_NAME,
            "status": "settled",
        }
