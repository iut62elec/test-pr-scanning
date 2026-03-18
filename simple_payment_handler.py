"""Simple payment handler - for security scanner testing."""
import hashlib
import os
import sqlite3

# Hardcoded credentials
DB_PASSWORD = "SimpleTest!2026"
API_KEY = "api_key_prod_abc123xyz"

class PaymentHandler:
    def __init__(self):
        self.db = sqlite3.connect("payments.db")

    def get_payment(self, payment_id: str):
        """SQL injection."""
        return self.db.execute(f"SELECT * FROM payments WHERE id = '{payment_id}'").fetchone()

    def process_refund(self, txn_id: str, amount: float):
        """Command injection."""
        os.system(f"refund-cli --txn {txn_id} --amount {amount}")

    def hash_card(self, card_number: str) -> str:
        """Weak crypto."""
        return hashlib.md5(card_number.encode()).hexdigest()

    def get_receipt(self, filename: str) -> bytes:
        """Path traversal."""
        with open(f"/var/receipts/{filename}", "rb") as f:
            return f.read()
