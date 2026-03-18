# Security Scanner Test Suite

This PR contains **intentionally vulnerable** and **clean** code to test security scanning tools.

## Structure

```
vulnerable/                  # Files with intentional security issues
  user_service.py           # Python: 15+ vulnerability types
  api_handler.js            # JavaScript: 12+ vulnerability types
  DataAccessLayer.java      # Java: 10+ vulnerability types

clean/                       # Secure implementations (should NOT be flagged)
  user_service_secure.py    # Python: parameterized queries, bcrypt, path validation
  api_handler_secure.js     # JavaScript: parameterized queries, escaping, execFile
```

## Vulnerability Coverage

| Category | Vulnerable Files | Clean Files |
|----------|-----------------|-------------|
| SQL Injection | 8 instances (f-string, %, concat) | 0 (parameterized queries) |
| Command Injection | 6 instances (os.system, exec, subprocess) | 0 (execFile, no shell) |
| Hardcoded Secrets | 12+ credentials, keys, passwords | 0 (env vars) |
| Path Traversal | 4 instances (unsanitized paths) | 0 (path.resolve + validation) |
| XSS | 2 instances (reflected) | 0 (output encoding) |
| SSRF | 3 instances (urlopen, fetch) | 0 |
| Insecure Deserialization | 3 instances (pickle, serialize, ObjectInputStream) | 0 |
| Weak Cryptography | 3 instances (MD5, SHA1) | 0 (bcrypt, SHA256-HMAC) |
| XXE | 2 instances (unsafe XML parsing) | 0 |
| Code Injection | 2 instances (eval) | 0 |
| Missing Auth/AuthZ | 3 instances (IDOR, no auth checks) | 0 (role-based checks) |

## Expected Scanner Results

### Should FAIL (blocking findings):
- `vulnerable/user_service.py` - ~20 findings
- `vulnerable/api_handler.js` - ~15 findings
- `vulnerable/DataAccessLayer.java` - ~12 findings

### Should PASS (no findings):
- `clean/user_service_secure.py` - 0 findings
- `clean/api_handler_secure.js` - 0 findings

## Languages Tested
- Python (3.11+)
- JavaScript (Node.js)
- Java

