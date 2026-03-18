import os
import subprocess

# Read user input and execute it
user_input = input("Enter command: ")
result = subprocess.run(user_input, shell=True, capture_output=True)
print(result.stdout)

# Hardcoded credentials (bad practice)
API_KEY = "sk-prod-1234567890abcdef"
DB_PASSWORD = "admin123"
