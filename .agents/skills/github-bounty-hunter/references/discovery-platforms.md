# Bounty Discovery & Issue Triage Guide

This reference provides technical procedures for querying and vetting paid open-source issues across GitHub, Algora, and Polar.

## 1. Querying Platforms

Operational parameters, URLs, and threshold values are defined in `config.json` under `search_policy` and `eligibility_policy`.

### GitHub Search API
Use GitHub's search API or web interface with structured qualifiers:
- **Base Query Syntax**:
  ```text
  is:issue is:open label:bounty no:assignee sort:created-desc
  ```
- **Language-Specific Filtering**:
  ```text
  is:issue is:open label:bounty language:typescript no:assignee
  ```
- **Platform-Specific Issue Markers**:
  - Algora issues: `is:issue is:open "bounty" "algora" no:assignee`
  - Polar issues: `is:issue is:open label:polar no:assignee`
- **Rate Limit & Authentication**:
  - Unauthenticated requests are throttled at 60 requests/hour (10 requests/minute for Search).
  - Configure `GITHUB_TOKEN` in the environment to unlock 5,000 requests/hour.

### Algora API & Portal
- **Endpoint**: Configured in `search_policy.algora_bounties_api_url` (`https://api.algora.io/api/bounties`)
- **Portal**: `https://console.algora.io`
- **Query Strategy**:
  - Filter `status: open`
  - Filter by target programming language (`language=typescript`)
  - Filter by minimum reward (`min_reward_usd` in `config.json`)
  - Verify organization reputation: Prioritize established open-source projects with active maintainers and recent commit history.

### Polar.sh API
- **Endpoint**: Configured in `search_policy.polar_bounties_api_url` (`https://api.polar.sh/api/v1/issues`)
- **Portal**: `https://polar.sh`
- **Pledge & Funding Inspection**:
  - Query with `is_funded=true` to isolate issues with upfront escrow funding.
  - Distinguish between **Funded** (funds deposited and held in escrow) versus **Pledged** (pledge promise by community members that may fail to clear).

---

## 2. Issue Triage & Viability Vetting Matrix

Before investing development effort, vet candidate issues across the 6-point triage matrix:

| Triage Gate | Pass Criteria | Rejection / Skip Criteria |
| :--- | :--- | :--- |
| **Assignee State** | `assignee: none` AND no active maintainer confirmation for another user. | Assigned to another user or active work ongoing in linked PR. |
| **Freshness** | Created within `max_issue_age_days` (default <= 14 days) or maintainer confirmed active. | > 30 days old with no maintainer response or stale debate. |
| **Funded Escrow Status** | Algora bot confirms bounty active; Polar pledge marked `is_funded: true` with confirmed funds. | Unfunded pledge promises, zero-dollar placeholders, or revoked bounties. |
| **Bounty Expiration** | Bounty has at least 7 days remaining before expiration or no set expiry. | Expiring within 48 hours, leaving inadequate window for review and merge. |
| **Reproduction Clarity** | Steps to reproduce (STR) are concrete, expected vs actual behavior is clear. | Vague symptom ("doesn't work"), no environment details, no logs. |
| **Scope Boundaries** | Atomic bug fix or well-defined standalone feature. | Broad architectural rewrites, ambiguous UI redesigns, moving targets. |

---

## 3. Stale & Contested Issue Safeguards

1. **Check Existing PRs**: Query `is:pr is:open <issue-id>` on GitHub to verify no pending unmerged PRs already address the issue.
2. **Comment Trail Audit**:
   - If multiple developers commented `Can I work on this?` or `/attempt` within the last 48 hours without maintainer response, flag as **contested**.
   - If maintainer explicitly assigned the issue to someone else, do not attempt to poach or duplicate work.
3. **Bounty Verification**:
   - Verify the bounty bot comment (e.g., `@algora-pbc` or `@polar-sh`) confirms the bounty is currently active and unawarded.
   - For Algora: Look for bot comment with active reward amount and `/attempt` instructions.
   - For Polar: Check Polar badge on the issue body showing funded amount.

---

## 4. Payout Eligibility & Account Pre-Flight Check

Before attempting to solve or claim any bounty, ensure the payout pipeline is viable:
1. **Stripe Express Readiness**: Both Algora and Polar disburse payouts via Stripe Express. Confirm the recipient GitHub account is linked to a verified Stripe Express account in a supported country.
2. **Platform Registration**:
   - Algora: Sign in once at `console.algora.io` using GitHub OAuth.
   - Polar: Connect GitHub account at `polar.sh`.
3. **Reward Floor**: Validate reward meets or exceeds `min_acceptable_reward_usd` in `config.json` to ensure return on invested development time.
