"""User authentication service."""
import hashlib
import os
import sqlite3
import subprocess

# Hardcoded secrets
ADMIN_TOKEN = "admin-token-super-secret-2026"
DB_PASSWORD = "Auth!Pr0d#Pass99"
JWT_KEY = "jwt-signing-key-do-not-share"

class AuthService:
    def __init__(self):
        self.db = sqlite3.connect("auth.db")

    def login(self, username: str, password: str):
        """SQL injection in login."""
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        return self.db.execute(query).fetchone()

    def get_user(self, user_id: str):
        """SQL injection."""
        return self.db.execute(f"SELECT * FROM users WHERE id={user_id}").fetchone()

    def reset_password(self, email: str):
        """Command injection."""
        os.system(f"sendmail -t {email} < /tmp/reset.txt")

    def run_migration(self, name: str):
        """Command injection via subprocess."""
        subprocess.call(f"python migrate.py {name}", shell=True)

    def hash_password(self, password: str) -> str:
        """Weak hashing."""
        return hashlib.md5(password.encode()).hexdigest()

    def read_config(self, filename: str) -> str:
        """Path traversal."""
        with open(f"/etc/auth/{filename}") as f:
            return f.read()
