"""User management service - CLEAN CODE (secure implementation).

This file demonstrates secure coding practices. A security scanner
should NOT flag any issues in this file.
"""
import hashlib
import hmac
import os
import secrets
from pathlib import Path
from typing import Optional

import bcrypt


# Configuration loaded from environment variables (not hardcoded)
DATABASE_URL = os.environ.get("DATABASE_URL", "")
SECRET_KEY = os.environ.get("SECRET_KEY", "")


class SecureUserService:
    """User service with proper security controls."""

    def __init__(self, db_connection):
        self.db = db_connection

    def get_user(self, user_id: int) -> Optional[dict]:
        """Parameterized query prevents SQL injection."""
        cursor = self.db.execute(
            "SELECT id, name, email FROM users WHERE id = ?",
            (user_id,),
        )
        row = cursor.fetchone()
        return dict(row) if row else None

    def search_users(self, name: str) -> list[dict]:
        """Parameterized query with LIKE."""
        cursor = self.db.execute(
            "SELECT id, name, email FROM users WHERE name LIKE ?",
            (f"%{name}%",),
        )
        return [dict(row) for row in cursor.fetchall()]

    def authenticate(self, username: str, password: str) -> Optional[dict]:
        """Secure authentication with parameterized query and bcrypt."""
        cursor = self.db.execute(
            "SELECT id, username, password_hash FROM users WHERE username = ?",
            (username,),
        )
        user = cursor.fetchone()
        if not user:
            return None

        if bcrypt.checkpw(password.encode(), user["password_hash"].encode()):
            return {"id": user["id"], "username": user["username"]}
        return None

    def create_user(self, username: str, password: str, email: str) -> int:
        """Secure user creation with bcrypt password hashing."""
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        cursor = self.db.execute(
            "INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)",
            (username, password_hash, email),
        )
        self.db.commit()
        return cursor.lastrowid

    def delete_user(self, requester_id: int, target_user_id: int) -> bool:
        """Delete with authorization check."""
        requester = self.get_user(requester_id)
        if not requester or not requester.get("is_admin"):
            raise PermissionError("Only admins can delete users")

        self.db.execute("DELETE FROM users WHERE id = ?", (target_user_id,))
        self.db.commit()
        return True


def hash_password(password: str) -> str:
    """Secure password hashing with bcrypt."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed: str) -> bool:
    """Secure password verification."""
    return bcrypt.checkpw(password.encode(), hashed.encode())


def generate_token() -> str:
    """Cryptographically secure token generation."""
    return secrets.token_urlsafe(32)


def get_avatar(user_id: int, uploads_dir: str = "/uploads/avatars") -> Optional[bytes]:
    """Safe file access with path validation."""
    base = Path(uploads_dir).resolve()
    avatar_path = (base / f"{user_id}.png").resolve()

    # Prevent path traversal
    if not str(avatar_path).startswith(str(base)):
        raise ValueError("Invalid avatar path")

    if not avatar_path.exists():
        return None

    return avatar_path.read_bytes()


def verify_webhook_signature(payload: bytes, signature: str, secret: str) -> bool:
    """HMAC signature verification for webhooks."""
    expected = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


def add(a: int, b: int) -> int:
    """Simple utility function."""
    return a + b


def format_username(name: str) -> str:
    """String formatting without security implications."""
    return name.strip().lower()

