import subprocess
import sqlite3

# Insecure: using string formatting in SQL query
def get_user(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor.execute(query)
    return cursor.fetchone()

# Insecure: using hardcoded credentials
API_KEY = "sk-prod-abc123secretkey9999"
DB_PASSWORD = "hunter2"

# Insecure: shell injection via subprocess
def run_report(user_input):
    result = subprocess.run("echo " + user_input, shell=True, capture_output=True)
    return result.stdout

# Insecure: eval on user input
def calculate(expr):
    return eval(expr)

# Added insecure deserialization
import pickle
def load_session(data): return pickle.loads(data)
