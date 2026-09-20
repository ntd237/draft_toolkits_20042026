# Advanced Browser Interactions & Lifecycle Management Guide

Comprehensive technical reference covering complex user interactions, page navigation lifecycle stages, multi-level iframe traversal, asynchronous browser event management, and session state injection.

---

## 1. Page Navigation & Lifecycle Management

When navigating to a URL or triggering operations that induce page reloads, agents must recognize 4 standard lifecycle milestones:

| Lifecycle State | Playwright Specifier | Technical Definition | Recommended Usage |
|---|---|---|---|
| `commit` | `'commit'` | First response byte received from server; URL context switched. | Rarely used; fast redirect verification only. |
| `domcontentloaded` | `'domcontentloaded'` | Initial HTML document parsed (subresources like images/styles still pending). | Static pages or fast initial DOM inspection. |
| `load` | `'load'` | All HTML, stylesheets, scripts, and static media loaded. | Standard server-rendered pages without background fetching. |
| `networkidle` | `'networkidle'` | No new network requests initiated for at least 500ms. | Single-page applications (SPAs) fetching dynamic REST/GraphQL data. |

### Safe Navigation Protocol
1. Specify explicit destination URL and synchronization condition:
   ```javascript
   await page.goto(targetUrl, {
     waitUntil: 'networkidle',
     timeout: config.navigation_timeout_ms
   });
   ```
2. Verify post-navigation address to account for server-side redirects or client auth guards:
   - Check `page.url()` against the expected route pattern.

---

## 2. Robust Input & Keyboard Interactions

### Safe Input Clearing (React Synthetic Event Compatibility)
Standard `.clear()` calls frequently fail to trigger `input` or `change` synthetic events in reactive UI frameworks (React, Angular, Vue).
- **Standard Sequence:**
  1. Focus the input: `await locator.click();`
  2. Select all text and delete:
     ```javascript
     await page.keyboard.press('ControlOrMeta+A');
     await page.keyboard.press('Backspace');
     ```
  3. Sequentially type the new value with human-like delay:
     ```javascript
     await locator.pressSequentially(textValue, { delay: 30 });
     ```

### ContentEditable & Rich Text Editors
For WYSIWYG editors (Quill, TinyMCE, ProseMirror, Draft.js):
- Avoid calling `.fill()` on `div[contenteditable="true"]`.
- Click into the editor boundary to establish cursor focus, then dispatch `page.keyboard.type(content)`.

---

## 3. Advanced Mouse Gestures (Hover & Drag-and-Drop)

### Hovering Flyout / Dropdown Menus
1. Move pointer to the trigger element:
   `await triggerLocator.hover();`
2. Await full visibility and positional settlement of the flyout container:
   `await submenuLocator.waitFor({ state: 'visible', timeout: config.element_wait_timeout_ms });`
3. Dispatch click on the target submenu item.

### Drag-and-Drop Execution
Applied to kanban boards, sortable lists, and range sliders:
1. **Native API Method:**
   ```javascript
   await sourceLocator.dragTo(targetLocator);
   ```
2. **Coordinate-Stepped Simulation (Fallback when HTML5 drag API is intercepted):**
   ```javascript
   const sourceBox = await sourceLocator.boundingBox();
   const targetBox = await targetLocator.boundingBox();
   await page.mouse.move(sourceBox.x + sourceBox.width / 2, sourceBox.y + sourceBox.height / 2);
   await page.mouse.down();
   await page.mouse.move(targetBox.x + targetBox.width / 2, targetBox.y + targetBox.height / 2, { steps: 10 });
   await page.mouse.up();
   ```

---

## 4. File Upload Handling

Never attempt to click an upload button if doing so spawns a native OS file dialog, which cannot be automated via browser drivers:
1. **Targeting `<input type="file">` Elements (Visible or Hidden):**
   ```javascript
   await page.locator('input[type="file"]').setInputFiles('/absolute/path/to/evidence.png');
   ```
2. **Multiple Files Upload:**
   ```javascript
   await fileInput.setInputFiles([path1, path2]);
   ```
3. **Intercepting File Chooser Events (When input is deeply wrapped):**
   ```javascript
   const fileChooserPromise = page.waitForEvent('filechooser');
   await page.getByRole('button', { name: 'Upload Image' }).click();
   const fileChooser = await fileChooserPromise;
   await fileChooser.setFiles('/absolute/path/to/evidence.png');
   ```

---

## 5. Handling Browser Dialogs (Alert, Confirm, Prompt)

Unregistered dialogs are automatically dismissed by the automation engine or can freeze the execution loop:
- **Rule:** Always register the dialog listener *before* initiating the action that triggers it:
  ```javascript
  page.once('dialog', async dialog => {
    console.log(`Intercepted dialog [${dialog.type()}]: ${dialog.message()}`);
    if (dialog.type() === 'prompt') {
      await dialog.accept('Required input value');
    } else {
      await dialog.accept(); // or dialog.dismiss() based on context
    }
  });
  await triggerButton.click();
  ```

---

## 6. Multi-Tab & Popup Management

When clicking links with `target="_blank"` or controls opening secondary windows:
```javascript
// Register page event listener on browser context
const newPagePromise = context.waitForEvent('page');
await page.getByRole('link', { name: 'View Invoice PDF' }).click();
const newPage = await newPagePromise;

// Await completion of the new tab lifecycle
await newPage.waitForLoadState('domcontentloaded');
console.log(`New Tab Title: ${await newPage.title()}`);

// Execute necessary actions on child page...
// Clean up child tab to conserve memory:
await newPage.close();
```

---

## 7. Frame & iFrame Traversal

Elements encapsulated within `<iframe>` elements cannot be queried directly from the root document:
1. **Targeting Frames via `frameLocator`:**
   ```javascript
   const paymentFrame = page.frameLocator('iframe#stripe-payment-element');
   await paymentFrame.getByRole('textbox', { name: 'Card number' }).fill('424242424242');
   ```
2. **Nested Frame Traversal:**
   ```javascript
   const outerFrame = page.frameLocator('iframe.parent-frame');
   const innerFrame = outerFrame.frameLocator('iframe.child-frame');
   await innerFrame.getByRole('button', { name: 'Confirm' }).click();
   ```
3. **Cross-Origin Frames:**
   - Verify frame load completion before attempting child element queries.

---

## 8. Session Injection & Storage State Management

To bypass redundant authentication flows, test role-based access control, or inject diagnostic test tokens:
1. **Cookie & Custom Header Injection:**
   ```javascript
   await context.addCookies([{
     name: 'session_token',
     value: 'mock_authenticated_jwt_xyz',
     domain: '.example.com',
     path: '/',
     httpOnly: true,
     secure: true
   }]);
   await context.setExtraHTTPHeaders({
     'X-Automation-Session': 'debug-mode-active',
     'Authorization': 'Bearer test_service_account_token'
   });
   ```
2. **Injecting Web Storage (LocalStorage / SessionStorage):**
   ```javascript
   await page.addInitScript(() => {
     window.localStorage.setItem('auth_user', JSON.stringify({ id: 99, role: 'qa_engineer' }));
     window.sessionStorage.setItem('feature_flags', JSON.stringify({ new_checkout_v2: true }));
   });
   ```

---

## 9. Custom HTML Modals & Backdrop Handling

Unlike native browser dialogs (`window.alert`), modern web applications render custom modal overlays (`<dialog>` or `div.modal` with a semi-transparent backdrop):
1. **Dismissal via Escape Key:**
   ```javascript
   await page.keyboard.press('Escape');
   await modalContainer.waitFor({ state: 'hidden', timeout: config.element_wait_timeout_ms });
   ```
2. **Backdrop Click Dismissal:**
   ```javascript
   // Click outside the modal content on the backdrop wrapper
   const backdrop = page.locator('.modal-backdrop, .overlay-scrim');
   await backdrop.click({ position: { x: 10, y: 10 } });
   ```
3. **Trapping Focus Inside `<dialog>`:**
   - Query close button explicitly: `page.getByRole('dialog').getByRole('button', { name: 'Close' }).click()`.

---

## 10. File Download Interception & Verification

To verify reporting exports, CSV downloads, or PDF invoices:
```javascript
const downloadPromise = page.waitForEvent('download', { timeout: config.action_timeout_ms });
await page.getByRole('button', { name: 'Export Report' }).click();
const download = await downloadPromise;

// Persist file into downloads directory from config.md
const savePath = `${config.downloads_dir}/${download.suggestedFilename()}`;
await download.saveAs(savePath);

// Validate export integrity
const failure = await download.failure();
if (failure) throw new Error(`Download failed: ${failure}`);
console.log(`Successfully downloaded: ${download.suggestedFilename()} to ${savePath}`);
```

---

## 11. Virtual Scrolling & Lazy-Loading Triggering

Single-page applications often employ `IntersectionObserver` or virtualized lists, rendering DOM nodes only when they intersect the viewport:
```javascript
async function scrollToRevealElement(locator, maxScrollSteps = 10) {
  let step = 0;
  while (step < maxScrollSteps) {
    if (await locator.isVisible()) return;
    await page.mouse.wheel(0, 400); // Scroll down 400px
    await page.waitForTimeout(config.animation_settle_timeout_ms);
    step++;
  }
  throw new Error(`Element failed to appear after ${maxScrollSteps} scroll iterations`);
}
```
