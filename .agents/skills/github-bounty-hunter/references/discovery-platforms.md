# Bounty Discovery & Issue Triage Guide

This reference provides technical procedures for querying and vetting paid open-source issues across GitHub, Algora, and Polar.

## 1. Querying Platforms

### GitHub Search API
Use GitHub's search API or web interface with structured qualifiers. Parameters are defined in `config.json` under `search_policy`:
- **Query syntax**:
  ```text
  is:issue is:open label:bounty no:assignee sort:created-desc
  ```
- **Language-specific filtering**:
  ```text
  is:issue is:open label:bounty language:typescript no:assignee
  ```
- **Bot-specific queries**:
  - Algora issues: `is:issue is:open "bounty" "algora" no:assignee`
  - Polar issues: `is:issue is:open label:polar no:assignee`

### Algora API & Portal
- **Endpoint**: `https://api.algora.io/api/bounties` (or console search at `https://console.algora.io`)
- **Filters**:
  - Status: `open`
  - Min/Max reward: Check reward currency (`USD`) and amount.
  - Organization reputation: Prioritize established open-source projects with active maintainers.

### Polar.sh API
- **Endpoint**: `https://api.polar.sh/api/v1/issues`
- **Pledge inspection**: Confirm total pledge amount and funding status before investing time.

---

## 2. Issue Triage & Viability Vetting Matrix

Before investing development effort, vet the issue using the following 4-point triage matrix:

| Triage Gate | Pass Criteria | Rejection / Skip Criteria |
| :--- | :--- | :--- |
| **Assignee State** | `assignee: none` AND no active maintainer confirmation for another user. | Assigned to another user or active work ongoing in linked PR. |
| **Freshness** | Created within `max_issue_age_days` (default <= 14 days) or maintainer confirmed active. | > 30 days old with no maintainer response or stale debate. |
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
