# Web Element Locator Strategy & Resilient Selectors Guide

Comprehensive reference guide for agent-driven element location, establishing a resilient 6-tier hierarchy designed to eliminate brittle selector failures during structural UI refactoring or styling changes.

---

## 1. Strict Locator Hierarchy

Agents must strictly follow the descending priority order from Tier 1 to Tier 6 when locating UI elements:

```
[Tier 1: Role & Accessible Name] ──> [Tier 2: Label & Placeholder] ──> [Tier 3: Exact Text]
                 │
                 └───> [Tier 4: Test ID Attribute] ──> [Tier 5: Semantic CSS] ──> [Tier 6: Rel. XPath]
```

### Tier 1: ARIA Roles & Accessible Names (Absolute Priority)
Mirrors how assistive technologies and human users perceive and interact with elements. Highly resistant to HTML markup refactoring and CSS class modifications.
- **Buttons:** `role="button"` with accessible name:
  - Syntax: `page.getByRole('button', { name: 'Log In', exact: true })`
- **Form Controls:** `role="textbox"`, `role="checkbox"`, `role="combobox"`, `role="link"`:
  - Syntax: `page.getByRole('textbox', { name: 'Email Address' })`
  - Syntax: `page.getByRole('link', { name: 'View Cart' })`

### Tier 2: Form Labels & Placeholders
Used directly for form input controls when semantic label associations exist:
- **By Label:** Locates through associated `<label for="id">`:
  - Syntax: `page.getByLabel('Current Password')`
- **By Placeholder:** Used when an input field possesses a distinct placeholder:
  - Syntax: `page.getByPlaceholder('Enter phone number...')`

### Tier 3: Visible Text Locators
Applied to static text elements, notices, dialog headings, and badges:
- Syntax: `page.getByText('Payment Succeeded', { exact: false })`
- Rule: Avoid matching excessively long paragraphs; target unique concise text anchors.

### Tier 4: Dedicated Test Attributes (Test IDs)
Applied in complex single-page applications (SPAs) configured with testing attributes:
- Standard attributes: `data-testid`, `data-test-id`, `data-cy`, `data-test`.
- Syntax: `page.getByTestId('checkout-submit-btn')`

### Tier 5: Resilient Semantic CSS Selectors
Utilized only when Role, Label, Text, or TestID are unavailable:
- **Recommended:** Selectors combining functional tags with business or semantic attributes:
  - `form[name="login-form"] input[type="email"]`
  - `article.product-card[data-product-id="102"] button.add-to-cart`
- **Strictly Prohibited:** Selectors relying on auto-generated styling classes (e.g., Tailwind layout classes or hashed CSS Modules such as `.btn-primary.flex.items-center.css-1a2b3c`).

### Tier 6: Relative Contextual XPath (Fallback of Last Resort)
Permitted only when traversing upward in the DOM (parent node traversal) or selecting complex sibling structures not feasible via CSS:
- **Permitted (Contextual relative XPath):**
  - `//tr[td[contains(text(), "Order #104")]]//button[contains(@class, "action-download")]`
- **Strictly Prohibited (Absolute XPath):**
  - FORBIDDEN: `/html/body/div[2]/div[1]/section/div[3]/form/div[2]/input` (highly brittle to minor DOM wrapper adjustments).

---

## 2. Avoiding Dynamic IDs & Hash Pitfalls

Modern frontend frameworks (React, Vue, Angular, Emotion, Webpack) frequently generate ephemeral IDs or class names during each build:
1. **Indicators of Dynamic Selectors:**
   - Contains UUID/GUID tokens: `id="input-550e8400-e29b-41d4-a716-446655440000"`
   - Contains framework auto-increment prefixes: `id="ember1234"`, `id="rc-tabs-0-tab-home"`, `class="sc-bdVaJa bVfKqL"`
2. **Resilience Techniques:**
   - Use prefix (`^=`) or suffix (`$=`) matching against static string anchors:
     - `input[id^="user-email-"]` instead of `input[id="user-email-9871"]`
   - Bind to semantic parent containers rather than ephemeral identifiers:
     - `section.account-settings .email-field input`

---

## 3. Handling Shadow DOM & Pierceable Selectors

Applications employing Web Components (Micro-frontends, Shoelace, Lit) encapsulate their internal DOM within `#shadow-root`:
- Playwright automatically pierces open Shadow DOM roots for standard CSS and text selectors:
  - `page.locator('custom-header my-search-bar input')` seamlessly crosses the shadow boundaries of `<custom-header>` and `<my-search-bar>`.
- For closed Shadow DOM: Execute in-page JavaScript to query or dispatch events:
  ```javascript
  const el = await page.evaluateHandle(() => {
    return document.querySelector('custom-host').shadowRoot.querySelector('internal-button');
  });
  ```

---

## 4. Resolving Element Ambiguity & Strict Mode Violations

When a selector matches more than one element, modern automation engines trigger a `strict mode violation`:
1. **Container Scoping & Chaining:**
   - Scope queries to a specific parent component rather than the global page:
     ```javascript
     const dialog = page.getByRole('dialog', { name: 'Confirm Deletion' });
     const confirmBtn = dialog.getByRole('button', { name: 'Confirm' });
     ```
2. **Filtering by Child Text or State:**
   - Apply `.filter({ hasText: ... })` or `.filter({ has: ... })`:
     ```javascript
     page.getByRole('listitem').filter({ hasText: 'Pro Plan' }).getByRole('button', { name: 'Select Plan' });
     ```
3. **Positional Indexing (Restricted Use):**
   - Reserve `.first()`, `.last()`, `.nth(i)` solely for lists with deterministic business ordering (e.g., the top entry in a sorted data table).
