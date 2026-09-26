# Ethical UX & Consent Design Patterns

Guidelines for auditing and eliminating deceptive patterns (dark patterns) and engineering transparent permission and consent experiences.

---

## 1. Anti-Dark Patterns Catalog

| Deceptive Pattern | Violation Signature | Ethical UX Solution |
| :--- | :--- | :--- |
| **Confirmshaming** | Emotionally manipulative opt-out copy ("No thanks, I hate saving money", "I prefer paying full price") | Neutral, respectful labels ("No, thanks", "Not now", "Dismiss"). |
| **Roach Motel** | 1-Click subscription sign-up, but cancellation requires complex multi-step forms or phone calls | Cancellation must be as frictionless as enrollment (1-2 clicks in Account Settings). |
| **Pre-selected Checkbox** | Pre-ticking checkboxes for marketing emails, recurring subscriptions, or insurance add-ons | Default to unchecked boxes (Explicit Opt-in); users actively choose to opt in. |
| **Forced Continuity** | Free trial converts to paid plan without notification or transparent reminder | Send notification 3-7 days prior to billing with a direct, 1-click cancellation link. |
| **Disguised Ads** | Advertisements disguised as system "Download", "Update", or "Next" buttons | Clearly label ads with "Sponsored" / "Advertisement" tags using distinct styling. |
| **Misdirection** | Visual asymmetry directing attention away from user intent (e.g., prominent "Stay Subscribed", faint "Cancel") | Action choices must visually balance according to the user's authentic intent. |

---

## 2. In-Context Permission & Consent UX

### 2.1. In-Context Permission Requests
- **Never blast permissions on initial app launch**: Request sensitive permissions (Camera, Location, Push Notifications, Microphone) only when the user triggers a feature requiring that capability.
- **Pre-Permission Primer Screen**:
  - Explain value proposition: "Allow camera access to scan payment QR codes."
  - Privacy commitment: State that images are processed locally and not stored without consent.
  - Symmetrical actions: Provide "Continue" (opens native OS dialog) and "Not Now".

### 2.2. Cookie & Data Consent Banners
- Consent banners must provide **"Accept All"** and **"Reject Non-Essential"** buttons with equal visual prominence and size.
- Do not block full-screen interaction solely for marketing consent (avoid modal blockades).
