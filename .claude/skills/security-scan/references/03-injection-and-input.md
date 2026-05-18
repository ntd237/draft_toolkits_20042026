# Phase 3 — Injection & Input Validation

## Objective

Detect insecure-input patterns that allow attacker-controlled data to reach a sensitive sink: SQL/NoSQL/command/LDAP/XPath injection, path traversal, SSRF, XSS, deserialization of untrusted data, template injection, and open redirects.

For each finding, you must show:

1. **Source**: where the user-controlled input enters the code
2. **Sink**: the dangerous function call or operation
3. **Path**: that the input reaches the sink unsanitized (at least informally — full taint analysis is out of scope, but you must describe the data flow in one sentence)

Without source–sink traceability, the finding is at most Medium and should be marked "version-based heuristic / requires manual confirmation".

---

## Common Sources (User-Controlled Input)

| Framework | Sources |
|---|---|
| Express / Fastify | `req.body`, `req.query`, `req.params`, `req.headers`, `req.cookies` |
| NestJS | `@Body()`, `@Query()`, `@Param()`, `@Headers()`, `@Req()` |
| Django | `request.GET`, `request.POST`, `request.COOKIES`, `request.headers`, URL path params |
| Flask / FastAPI | `request.args`, `request.form`, `request.json`, `request.headers`, path params |
| Spring | `@RequestParam`, `@PathVariable`, `@RequestBody`, `@RequestHeader`, `HttpServletRequest` |
| Gin (Go) | `c.Query()`, `c.Param()`, `c.PostForm()`, `c.GetHeader()`, `c.ShouldBindJSON()` |
| Rails | `params[:x]`, `request.headers`, `cookies` |
| Laravel | `$request->input()`, `$request->query()`, `request()->all()` |

CLI / desktop sources include `argv`, `os.environ` / `process.env` (when they reflect user-controlled values), file contents read at runtime.

---

## SQL Injection

### Patterns to Search

```
# String concatenation or interpolation into a query
db.query("SELECT * FROM users WHERE id = " + userId)
cursor.execute(f"SELECT * FROM users WHERE name = '{name}'")
db.exec(`UPDATE accounts SET bal = ${bal} WHERE id = ${id}`)
String.format("SELECT * FROM x WHERE y = %s", userInput)
"... WHERE col = '" + req.query.x + "'"
```

### High-precision regex (start broad, then verify by reading the line)

```
(query|exec|execute|prepare|raw)\s*\(\s*["'`][^"'`]*\$\{[^}]+\}
(query|exec|execute)\s*\(\s*["'`].*\+\s*\w+\s*\+
\.format\s*\([^)]*\)
f["']\s*(SELECT|INSERT|UPDATE|DELETE)
```

### Triage

- Real string concatenation with a request-derived value reaching `.execute`/`.query` → **Critical** if it hits a request handler, **High** if internal.
- ORM with a hand-crafted raw query branch (e.g., `Model.objects.raw(...)` in Django, `knex.raw(...)`, `sequelize.query(...)`, `prisma.$queryRawUnsafe(...)`) → audit each call.
- ORM with parameterized binding (`?`, `$1`, `:name`) is safe regardless of input — note as Info if heavy raw use is mixed in.

### Remediation Example

```
# BAD (Python)
cursor.execute(f"SELECT * FROM users WHERE name = '{name}'")

# GOOD
cursor.execute("SELECT * FROM users WHERE name = %s", (name,))
```

---

## NoSQL Injection

### Mongo

- Operator injection in JSON body: a client-supplied object like `{"$ne": null}` instead of a string bypasses equality checks.
- `eval(...)`, `$where: "<JS>"` with concatenation.
- `find(JSON.parse(req.body.q))` patterns.

### DynamoDB / Firestore

- String concatenation into FilterExpression / where clauses; missing `ExpressionAttributeValues`.

### Remediation

- Coerce input types (`String(req.body.username)`) before passing to the query.
- Use schema validators (Zod, Joi, Pydantic, class-validator) at the boundary.

---

## Command Injection

### Sinks (per language)

| Language | Sinks |
|---|---|
| Node.js | `child_process.exec`, `execSync`, `child_process.spawn` with `shell: true`, backticks, `eval` |
| Python | `os.system`, `subprocess.run/Popen` with `shell=True`, `os.popen`, `commands.*` |
| Java | `Runtime.exec(String)`, `ProcessBuilder` with shell wrapper |
| Go | `exec.Command("sh", "-c", ...)` with concatenated input |
| Ruby | backticks `` `...` ``, `system("...")`, `%x{...}`, `Open3.capture2(shell)` |
| PHP | `system`, `exec`, `shell_exec`, `passthru`, `popen`, backticks |

### Patterns to Search

```
exec\s*\(\s*[`'"][^`'"]*\+
spawn\s*\([^)]*shell\s*:\s*true
system\s*\([^)]*\+
Runtime\.getRuntime\(\)\.exec\(\s*"[^"]*"\s*\+
subprocess\.(run|Popen)\([^)]*shell\s*=\s*True
```

### Triage

- Any sink receiving a user-controlled value with shell semantics → **Critical**.
- Same sink with safe arg array (e.g., `subprocess.run(["git", "log", commit_id])`) is safe **only if** `commit_id` is passed as a single argv element — verify it isn't expanded into a string first.

### Remediation Example

```
# BAD
subprocess.run(f"convert {user_path} out.png", shell=True)

# GOOD
subprocess.run(["convert", user_path, "out.png"])
# AND validate user_path against an allowlist or use shlex.quote for shell-only paths.
```

---

## Path Traversal & Arbitrary File Read/Write

### Patterns

```
open\s*\(\s*[^)]*req\.(query|params|body)
fs\.(readFile|writeFile|createReadStream)\s*\(\s*req\.
new\s+File\(\s*request\.getParameter
os\.path\.join\([^)]*request\.[^)]*\)
ioutil\.ReadFile\(.*c\.Param
```

### Sanitization Tells

Look for these defenses near the sink:
- `path.normalize` + check for `..`
- `path.resolve` + a `startsWith(rootDir)` guard
- `os.path.realpath` + `commonpath` check
- `Files.normalize().normalize()` (Java NIO) + base-path check

If the defense exists, classify as Info or Low. If the defense is missing, **High**; if the read/write is then served to the user, **Critical**.

### Remediation

```
# Pattern: resolve user-provided name within a fixed root, then verify containment
import os
SAFE_ROOT = "/var/app/uploads"
candidate = os.path.realpath(os.path.join(SAFE_ROOT, user_name))
if not candidate.startswith(SAFE_ROOT + os.sep):
    raise PermissionError("Path outside allowed directory")
```

---

## SSRF (Server-Side Request Forgery)

### Sinks

| Language | Sinks |
|---|---|
| Node | `fetch`, `axios`, `http.request`, `node-fetch`, `request`, `got`, `undici.request` |
| Python | `requests`, `httpx`, `urllib.request.urlopen`, `aiohttp.ClientSession` |
| Java | `URL.openConnection`, `HttpClient.send`, `RestTemplate`, `WebClient` |
| Go | `http.Get`, `http.Post`, `http.Client.Do` |

### Triage

- Any of the above receiving a URL whose host or path is taken from user input → **High**.
- If the response is reflected back to the user (proxy / preview / image fetch) → **Critical**.

### Defenses to Look For

- Allowlist of hosts / domains
- DNS resolution + check the resolved IP is not in private ranges (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `169.254.0.0/16` for cloud metadata, `127.0.0.0/8`, `::1`, link-local `fe80::/10`, IPv4-mapped IPv6, AWS metadata `169.254.169.254`, GCP `metadata.google.internal`, Azure `169.254.169.254`)
- Disabling redirects, or following them only to allowlisted hosts
- Disabling protocols other than `http`/`https` (no `file://`, `gopher://`, `dict://`)

If none of these are present near the sink, report SSRF.

---

## Cross-Site Scripting (XSS)

### Sinks

- React: `dangerouslySetInnerHTML` with user data
- Vue: `v-html` with user data
- Angular: bypassing `DomSanitizer` (`bypassSecurityTrustHtml`)
- jQuery: `$(el).html(user)`, `$(el).append(user)`
- Server-side templates without auto-escape: Jinja `{{ x | safe }}`, Twig `{{ x | raw }}`, Handlebars `{{{ x }}}`, EJS `<%- x %>`, Razor `@Html.Raw(x)`, Mustache triple-stash `{{{x}}}`
- Direct DOM writes: `innerHTML =`, `document.write`, `outerHTML =`, `insertAdjacentHTML`
- Express `res.send(html)` with concatenated user input
- Email/notification templates with raw user content

### Triage

- Reflected/stored data without HTML encoding → **High**.
- Inside a strict CSP that blocks inline scripts and `eval` → downgrade to **Medium** but still report (CSP is mitigation, not fix).
- Content rendered as `text/plain` or set via `.textContent` is safe.

### Stored vs. Reflected vs. DOM

If the source is a database column written by another user, label "Stored XSS". If the source is the URL/query string, label "Reflected XSS". If the flow is entirely client-side from `location` / `document.cookie` to a DOM sink, label "DOM-based XSS".

### Remediation

- Server templates: rely on auto-escape; never use `safe`/`raw`/`Html.Raw` on user-controlled data.
- React: render user content as text (`{userText}`) — safe by default; only use `dangerouslySetInnerHTML` after passing through a sanitizer (`dompurify`).
- Add or strengthen a Content-Security-Policy header.

---

## Insecure Deserialization

### Sinks

| Language | Sinks |
|---|---|
| Python | `pickle.loads`, `cPickle.loads`, `dill.loads`, `joblib.load`, `yaml.load` (without `SafeLoader`), `marshal.loads`, `shelve.open` on untrusted file |
| Java | `ObjectInputStream.readObject`, `XMLDecoder.readObject`, `Yaml.load` (SnakeYAML default), `Kryo` without registration |
| .NET | `BinaryFormatter`, `NetDataContractSerializer`, `LosFormatter`, `SoapFormatter`, `JavaScriptSerializer` with `SimpleTypeResolver`, `Json.NET` with `TypeNameHandling != None` |
| Node.js | `node-serialize`, `serialize.unserialize` of untrusted, `funcster.deepDeserialize` |
| PHP | `unserialize` on untrusted, `__wakeup`, `__destruct` gadgets |
| Ruby | `Marshal.load`, `YAML.load` with `Psych::Y` permissive |

### Triage

- Any of the above with input from a request, file upload, or message queue → **Critical** unless input is constrained to a known schema with a safe loader.
- Specifically `yaml.load(stream)` in PyYAML versions where it is unsafe → **High** to **Critical** depending on input.

### Remediation

- Replace with safe loaders: `yaml.safe_load`, `pickle` → JSON or protobuf, `BinaryFormatter` → `System.Text.Json` with strict schema.
- Restrict `TypeNameHandling` to `None` in Json.NET; never deserialize types from untrusted JSON.

---

## Server-Side Template Injection (SSTI)

### Sinks

- Jinja2: `Template(user_input).render()` or `render_template_string(user_input)`
- Twig: `Twig\Environment::createTemplate($user)`
- Freemarker, Velocity: passing user-controlled template strings to engine
- Mako: `Template(user_input).render()`
- Handlebars: `Handlebars.compile(user_input)({...})` — also XSS risk

Severity: **Critical** if reachable from a request; SSTI typically yields RCE.

---

## XXE (XML External Entity)

### Sinks (XML parsers without secure defaults)

- Java: `DocumentBuilderFactory`, `SAXParserFactory`, `TransformerFactory`, `XMLInputFactory` without disabling external entities
- Python: `lxml.etree.fromstring(...)` with `XMLParser(resolve_entities=True)` (defused since recent versions; `defusedxml` recommended)
- .NET: `XmlReader` with `DtdProcessing=Parse` and a non-null resolver
- Node: `libxmljs` with `noent: true`, `xml2js` with `explicitChildren: true` (rare for XXE itself)

### Defense Patterns

```
# Java
factory.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
factory.setFeature("http://xml.org/sax/features/external-general-entities", false);
factory.setFeature("http://xml.org/sax/features/external-parameter-entities", false);

# Python
from defusedxml import ElementTree
```

If features are not set or `defusedxml` is not used and the parser is fed user input → **High**.

---

## Open Redirect

### Patterns

```
res.redirect(req.query.next)
return redirect(request.GET['url'])
response.sendRedirect(request.getParameter("returnUrl"))
```

### Triage

- Redirect target taken directly from user → **Medium** alone, **High** if part of an OAuth / login flow (phishing risk).
- Allowlist or relative-only checks (`url.startsWith("/")`) downgrade to Info.

---

## Regex DoS (ReDoS)

Look for catastrophic-backtracking patterns in regexes that touch user input:
- Nested quantifiers: `(a+)+`, `(.*)*`, `(a|a)+`
- Overlapping alternation: `(a|aa)+`

If found in a path that processes large user input (uploads, search queries), classify as **Medium** unless the pattern blocks a security check (then **High**).

---

## Validation Layer Gaps

In addition to specific sinks, evaluate the project's input-validation discipline:

- Are request bodies validated against a schema (Zod, Joi, Pydantic, class-validator, JSON Schema, Bean Validation)?
- Are types coerced explicitly at the boundary?
- Are file uploads bounded by size, count, MIME type, and a content-sniff check?
- Is there an allowlist for redirect URLs, image hosts, CORS origins?

A project with no validation layer is **at least** Medium across the board for any reachable injection finding.

---

## Reporting Pattern

Each injection finding should look like:

```
### [High] SQL Injection in src/api/users.ts:42
**Category**: Injection (OWASP A03:2021 / CWE-89)
**Source**: req.query.search (HTTP GET parameter)
**Sink**: db.query("...") with string concatenation
**Path**: src/api/users.ts:42 → directly concatenated into the SQL string
**Evidence**:
  src/api/users.ts:42
  const sql = "SELECT * FROM users WHERE name = '" + req.query.search + "'";
  db.query(sql);
**Impact**: Attacker can read or modify arbitrary data in the `users` table; depending on DB privileges, may pivot to other tables.
**Remediation**:
  1. Use parameterized query: db.query("SELECT * FROM users WHERE name = $1", [req.query.search]);
  2. Add a Zod schema at the route boundary to bound `search` to a string of length ≤ 100.
  3. Restrict the DB user's privileges to least required.
```

---

## Required Practices

- Always link source → sink with at least an informal data-flow sentence.
- Always check for nearby defensive code before promoting to Critical.
- Always recommend a stack-specific remediation (not a generic "use parameterized queries").

## Prohibited Practices

- Do not run actual exploits or send payloads.
- Do not fabricate data flow you have not actually read in the source.
- Do not assign Critical without a request-reachable sink.
