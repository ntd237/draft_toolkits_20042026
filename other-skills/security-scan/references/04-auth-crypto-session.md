# Phase 4 — Authentication, Authorization, Session, Crypto

## Objective

Audit how the project authenticates users, authorizes actions, manages sessions, stores passwords, and uses cryptography. These categories are both high-impact (Critical/High when broken) and high-noise (false positives are common). Ground every finding in concrete code.

---

## Section A — Authentication (AuthN)

### A.1 — Password Storage

Inspect every place passwords are written or compared.

| Pattern (BAD) | Why | Severity |
|---|---|---|
| `md5(password)` | Fast, broken | Critical |
| `sha1(password)` | Fast, broken | Critical |
| `sha256(password)` (single iteration, no salt) | Fast, no work factor | High |
| `crypto.createHash('sha256').update(p).digest()` | Same as above | High |
| Comparison with `===` / `==` on hashes | Timing leak | Medium |
| Plain-text password in DB column | No comment needed | Critical |

| Pattern (GOOD) | Notes |
|---|---|
| `bcrypt.hash(p, 12+)` / `bcrypt.compare` | Cost ≥ 10, ideally 12 |
| `argon2id` with reasonable params | Preferred for new projects |
| `scrypt` with N ≥ 2^14 | Acceptable |
| `PBKDF2-HMAC-SHA256` with iterations ≥ 600,000 (per OWASP 2026 guidance) | Acceptable |
| `crypto.timingSafeEqual` for comparisons | Required |

Search for password-handling functions:

```
(?i)\b(password|passwd|pwd|hash|verify)\b
import\s+bcrypt
import\s+argon2
import\s+scrypt
crypto\.(createHash|pbkdf2)
hashlib\.(md5|sha1|sha256)\(
PasswordEncoder|BCryptPasswordEncoder
```

If you find a custom KDF (the developer wrote their own loop), classify as **High** even if it uses a strong primitive — custom crypto is presumed broken until reviewed by an expert.

### A.2 — Multi-Factor Authentication

- Is MFA available for privileged accounts? Note as Info if absent on admin-tier endpoints.
- TOTP secret length ≥ 160 bits, generated with a CSPRNG.
- Recovery codes one-time-use, hashed at rest.
- "Trust this device" tokens with reasonable expiry.

### A.3 — Account Recovery

- Reset tokens use a CSPRNG (not `Math.random`, not `rand()`, not `time()`).
- Tokens have an expiry (≤ 1 hour typical), single-use.
- Reset endpoint does not enumerate users (same response whether email exists or not).
- Old session is invalidated after password change.

### A.4 — Login Endpoint Hardening

- Generic error message for invalid credentials (no "user not found" vs "wrong password" distinction).
- Rate limiting per IP and per account (e.g., `express-rate-limit`, `flask-limiter`, `bucket4j`, framework defaults).
- Optional CAPTCHA after N failures.
- Logs login successes and failures with username and IP, without logging the password.

---

## Section B — Authorization (AuthZ)

### B.1 — Missing Authorization Checks (Broken Access Control)

This is the #1 OWASP category (A01:2021). For each route in the entry-point inventory from Phase 1:

1. Identify whether it requires authentication. If not, is that intentional (e.g., `/health`, `/login`)?
2. Identify the authorization check. Is there one? Is it enforced consistently across HTTP verbs?
3. For routes with object-level access (`/users/:id/orders/:orderId`), is there an ownership check?

#### IDOR (Insecure Direct Object Reference) Patterns

Look for handlers that use the id from the URL/body without verifying ownership:

```
# BAD
@app.get("/api/orders/{order_id}")
def get_order(order_id: int, current_user):
    return Order.objects.get(id=order_id)         # no ownership check

# GOOD
def get_order(order_id, current_user):
    return Order.objects.get(id=order_id, user=current_user)
```

```js
// BAD
app.get('/api/users/:id', auth, async (req, res) => {
  const u = await User.findById(req.params.id);
  res.json(u);
});

// GOOD
app.get('/api/users/:id', auth, async (req, res) => {
  if (req.params.id !== req.user.id && !req.user.isAdmin) return res.sendStatus(403);
  ...
});
```

Severity: **Critical** if the data is sensitive (PII, financial, health), otherwise **High**.

### B.2 — Vertical Privilege Escalation

- Are admin endpoints clearly separated and require an `isAdmin` / role check?
- Is the role check enforced **server-side**, not just hidden in the UI?
- Search for `isAdmin`, `role ===`, `hasRole`, `@PreAuthorize`, `@Secured`, `@RolesAllowed`. Verify each privileged route has at least one.

### B.3 — Mass Assignment

- ORM models that accept all fields from `req.body` without an allowlist (`User.create(req.body)`) → **High**.
- Look for Sequelize `bulkCreate(req.body, { ... })`, Mongoose `.set(req.body)`, Django `**request.POST`, Rails `update(params[:user])` without `permit`, ASP.NET `[Bind(...)]` missing.

---

## Section C — Session Management

### C.1 — Cookie Flags

Audit every place cookies are set:

| Flag | Required Value | Notes |
|---|---|---|
| `Secure` | `true` for prod | Cookie sent only over HTTPS |
| `HttpOnly` | `true` for session/auth cookies | Blocks JS access |
| `SameSite` | `Strict` or `Lax` | `None` requires `Secure` |
| `Domain` | not overly broad (avoid setting parent domain) | |
| `Path` | scoped narrowly | |
| `Expires` / `Max-Age` | reasonable lifetime | |

Patterns to find:

```
res.cookie\([^)]*\)
session\s*=
django.*SESSION_COOKIE_(SECURE|HTTPONLY|SAMESITE)
SESSION_COOKIE_SECURE\s*=\s*False
```

If `Secure` or `HttpOnly` is not set on a session cookie, **Medium** to **High** depending on what the cookie carries.

### C.2 — Session Lifecycle

- New session ID issued on login (prevent session fixation).
- Session destroyed on logout (server-side, not just by deleting the cookie).
- Reasonable absolute and idle timeouts.
- Session storage is server-side (Redis, DB) for sensitive apps; signed cookie for low-risk apps.

### C.3 — CSRF Protection

For state-changing endpoints that use cookie auth:
- Is there a CSRF token (`csurf`, `Django CSRF`, `Spring CsrfFilter`, `csrf_meta_tags` in Rails)?
- Is `SameSite` cookie attribute used as a defense layer?
- Is the API JSON-only with `Content-Type: application/json` enforced (a common partial defense)?

Pure JWT-bearer-token APIs without cookies do not need CSRF; note the auth model when classifying.

---

## Section D — JWT Specifics

JWT misuse is so common it deserves its own subsection.

### D.1 — Algorithm

```
jwt\.sign\([^)]*algorithm\s*:\s*["']none["']
verify(token, secret)   // missing algorithms whitelist
```

- `alg: none` accepted on verify → **Critical**.
- Verifier accepts both HS256 and RS256 with the same key (the public key is then used as an HMAC secret) → **Critical**.
- Always pin the algorithm: `jwt.verify(token, key, { algorithms: ['RS256'] })`.

### D.2 — Secret Strength

- HMAC secret < 32 random bytes / encoded as a short ASCII string → **High** (brute-forceable).
- Hardcoded HMAC secret committed to source → **Critical** (also a Phase-2 secret finding).

### D.3 — Claims

- `exp` (expiration) present and verified.
- `nbf`, `iat` validated when reasonable.
- `aud` (audience) and `iss` (issuer) checked.
- `kid` parameter validation does not allow path traversal to attacker-controlled key files.

### D.4 — Storage on the Client

- JWT in `localStorage` is a Medium finding (XSS exfiltration risk).
- JWT in `HttpOnly` `Secure` cookie is preferred.

---

## Section E — Cryptography

### E.1 — Algorithm Selection

| Use Case | BAD | OK | Strong |
|---|---|---|---|
| Symmetric encryption | DES, 3DES, RC4, Blowfish | AES-128-GCM | AES-256-GCM, ChaCha20-Poly1305 |
| Block cipher mode | ECB | CBC w/ HMAC | GCM, OCB |
| Hashing (general) | MD5, SHA-1 | SHA-256 | SHA-3, BLAKE2 |
| Password hashing | MD5/SHA family | PBKDF2 (high iter) | Argon2id, bcrypt(12+), scrypt |
| Asymmetric | RSA-1024, custom curves | RSA-2048 | RSA-3072+, Ed25519, P-256 |
| MAC | none, custom | HMAC-SHA-256 | HMAC-SHA-256 with timing-safe compare |
| Random | `Math.random`, `rand()` | OS-provided when explicit | `crypto.randomBytes`, `secrets.token_bytes`, `SecureRandom` |

### E.2 — Patterns to Find

```
DES|3DES|RC4|Blowfish
\bECB\b
Cipher\.getInstance\(["']AES["']\)        // defaults to ECB in Java
new\s+IvParameterSpec\(.*\.getBytes\(\)\) // hardcoded IV
Math\.random
java\.util\.Random
new\s+Random\(\)        // not SecureRandom
rand\s*\(\s*\)
```

### E.3 — Key Management

- Keys stored in source → covered by Phase 2.
- Keys read from env at startup is acceptable.
- Keys read from KMS / Vault / HSM is preferred.
- Key rotation procedure documented?

### E.4 — Random Numbers

For anything security-relevant (tokens, IDs, salts, IVs, nonces), the source must be a CSPRNG:

| Language | CSPRNG | Insecure |
|---|---|---|
| Node | `crypto.randomBytes`, `crypto.randomUUID` | `Math.random` |
| Python | `secrets.token_bytes`, `os.urandom` | `random.*` (Mersenne Twister) |
| Java | `SecureRandom` | `java.util.Random`, `Math.random` |
| Go | `crypto/rand` | `math/rand` |
| .NET | `RandomNumberGenerator.Create()` | `Random` |

Misuse of non-CSPRNG for security purposes → **High**.

### E.5 — TLS

- Are HTTP servers configured with TLS in production? Look for `http.createServer` vs `https.createServer`, framework configs, reverse-proxy expectations.
- Are minimum TLS versions enforced (TLS 1.2 minimum, TLS 1.3 preferred)?
- Custom HTTP clients that disable cert verification:
  - Python: `verify=False` in `requests.get`
  - Node: `rejectUnauthorized: false` in `https.Agent`
  - Java: trust-all `X509TrustManager`
  - Go: `InsecureSkipVerify: true`
  - cURL: `--insecure` / `-k`

Each instance is **High** unless inside a clearly marked test fixture.

---

## Section F — Common Authentication Library Misconfigurations

### Express / Passport
- Sessions configured with default secret.
- `cookie-session` with weak secret.
- `secure: false` in production.

### NextAuth / Auth.js
- `NEXTAUTH_SECRET` default or empty.
- Missing CSRF protections in custom OAuth flows.

### Spring Security
- `permitAll()` on more than intended.
- CSRF disabled globally without justification.
- `httpBasic()` left on for protected endpoints.

### Django
- `SECRET_KEY` not random / committed.
- `ALLOWED_HOSTS = ['*']` in prod.
- `DEBUG = True` in prod.

### Rails / Devise
- `secret_key_base` default or committed.
- `protect_from_forgery` skipped on state-changing controllers.

### .NET
- `[AllowAnonymous]` mistakenly applied to a sensitive controller.
- `AntiforgeryToken` not validated on POST.

### OAuth / OIDC clients
- `state` parameter not used or not verified.
- `redirect_uri` not pinned to an exact value.
- Implicit flow used where authorization-code-with-PKCE is appropriate.

---

## Reporting Pattern

```
### [Critical] Use of MD5 for Password Hashing in app/auth/password.py:23
**Category**: Cryptographic Failures (OWASP A02:2021 / CWE-327)
**Evidence**:
  app/auth/password.py:23
  hashed = hashlib.md5(password.encode()).hexdigest()
**Impact**: MD5 is collision-broken and unsuitable for password storage. Offline brute-force at billions of guesses per second is feasible against any leaked DB dump.
**Remediation**:
  1. Migrate to argon2id via the `argon2-cffi` library:
     from argon2 import PasswordHasher
     ph = PasswordHasher()
     hashed = ph.hash(password)
  2. Run a one-time migration: on next login, re-hash with argon2 and store; mark old MD5 hashes with a column flag.
  3. Force a password reset for any account whose hash was never re-migrated within 90 days.
```

---

## Required Practices

- Always check for both presence of authn AND authorization on every state-changing route.
- Always verify that crypto algorithms match current OWASP guidance, not legacy advice.
- Always note when JWT algorithm is unrestricted on verify.
- Always recommend timing-safe comparison for hash equality.

## Prohibited Practices

- Do not flag `Math.random` outside a security context (e.g., random color picker is fine).
- Do not recommend custom crypto. Always recommend a battle-tested library.
- Do not flag `eval` patterns under crypto (those go in Phase 3).
