"""User management service - VULNERABLE CODE (intentional for testing)."""
import hashlib
import os
import pickle
import sqlite3
import subprocess
import xml.etree.ElementTree as ET
from urllib.request import urlopen


# ============================================================
# VULNERABILITY: Hardcoded credentials
# Expected: Scanner should flag these as critical/high severity
# ============================================================
DATABASE_HOST = "prod-db.internal.company.com"
DATABASE_USER = "app_admin"
DATABASE_PASSWORD = "P@ssw0rd!Pr0duction2026"
API_SECRET_KEY = "sk_prod_a1b2c3d4e5f6g7h8i9j0k1l2m3n4"
JWT_SIGNING_KEY = "jwt-signing-key-never-commit-this-to-git"
ENCRYPTION_KEY = "aes256-encryption-key-12345678901234"

CONNECTION_STRING = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:5432/users"


class UserService:
    def __init__(self):
        self.db = sqlite3.connect("users.db")

    # ============================================================
    # VULNERABILITY: SQL Injection (multiple variants)
    # Expected: Scanner should flag each as critical
    # ============================================================

    def get_user(self, user_id: str):
        """SQL injection via f-string interpolation."""
        query = f"SELECT * FROM users WHERE id = '{user_id}'"
        return self.db.execute(query).fetchone()

    def search_users(self, name: str):
        """SQL injection via % string formatting."""
        sql = "SELECT * FROM users WHERE name LIKE '%%%s%%'" % name
        return self.db.execute(sql).fetchall()

    def authenticate(self, username: str, password: str):
        """SQL injection in authentication - allows auth bypass."""
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        return self.db.execute(query).fetchone()

    def delete_user(self, user_id: str):
        """SQL injection + missing authorization check (IDOR)."""
        self.db.execute(f"DELETE FROM users WHERE id = '{user_id}'")
        self.db.commit()


    # ============================================================
    # VULNERABILITY: Command Injection
    # Expected: Scanner should flag as critical
    # ============================================================

    def send_notification(self, email: str, message: str):
        """Command injection via os.system."""
        os.system(f"echo '{message}' | sendmail {email}")

    def generate_report(self, report_name: str):
        """Command injection via subprocess with shell=True."""
        subprocess.call(f"python generate_report.py --name {report_name}", shell=True)

    def backup_user_data(self, user_id: str):
        """Command injection via subprocess.Popen."""
        subprocess.Popen(f"mysqldump users --where=\"id={user_id}\" > /tmp/backup.sql", shell=True)


    # ============================================================
    # VULNERABILITY: Insecure Deserialization
    # Expected: Scanner should flag as high
    # ============================================================

    def import_user_data(self, data: bytes):
        """Insecure pickle deserialization."""
        return pickle.loads(data)


    # ============================================================
    # VULNERABILITY: Weak Cryptography
    # Expected: Scanner should flag as high/medium
    # ============================================================

    def hash_password(self, password: str) -> str:
        """MD5 is cryptographically broken for password hashing."""
        return hashlib.md5(password.encode()).hexdigest()

    def hash_token(self, token: str) -> str:
        """SHA1 is deprecated for security purposes."""
        return hashlib.sha1(token.encode()).hexdigest()


    # ============================================================
    # VULNERABILITY: Path Traversal
    # Expected: Scanner should flag as high
    # ============================================================

    def get_avatar(self, filename: str) -> bytes:
        """Path traversal - no sanitization of filename."""
        with open(f"/uploads/avatars/{filename}", "rb") as f:
            return f.read()

    def read_config(self, config_name: str) -> str:
        """Path traversal in config reading."""
        with open(f"/etc/app/{config_name}") as f:
            return f.read()


    # ============================================================
    # VULNERABILITY: SSRF
    # Expected: Scanner should flag as high
    # ============================================================

    def verify_website(self, url: str):
        """SSRF - fetches arbitrary URLs from user input."""
        return urlopen(url).read()

    def fetch_profile_image(self, image_url: str):
        """SSRF via user-controlled URL."""
        return urlopen(image_url).read()


    # ============================================================
    # VULNERABILITY: XXE (XML External Entity)
    # Expected: Scanner should flag as high
    # ============================================================

    def parse_user_xml(self, xml_data: str):
        """Unsafe XML parsing vulnerable to XXE."""
        tree = ET.fromstring(xml_data)
        return {
            "name": tree.find("name").text,
            "email": tree.find("email").text,
        }


    # ============================================================
    # VULNERABILITY: Code Injection
    # Expected: Scanner should flag as critical
    # ============================================================

    def render_template(self, template: str, data: dict) -> str:
        """eval-based template rendering - code injection."""
        return eval(f"f'{template}'")

    def calculate_discount(self, formula: str) -> float:
        """eval on user input - arbitrary code execution."""
        return eval(formula)

