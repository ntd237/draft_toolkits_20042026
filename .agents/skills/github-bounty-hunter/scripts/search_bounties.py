#!/usr/bin/env python3
"""
Utility script to search GitHub, Algora, and Polar for open bounty issues.
Reads operational policies from config.json to avoid hardcoded search parameters.
Enforces freshness (max age), low competition (max comments), and zero existing PRs.
"""

import os
import sys
import ssl
import json
import shutil
import argparse
import subprocess
from pathlib import Path
from datetime import datetime, timedelta, timezone
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, quote_plus

def load_config() -> dict:
    config_path = Path(__file__).resolve().parent.parent / "config.json"
    if config_path.exists():
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            sys.stderr.write(f"Warning: Could not parse config.json: {e}\n")
    return {}

def build_search_query(config: dict, language: str = None, label: str = None, task_type: str = None, max_age_days: int = None, max_comments: int = None) -> str:
    search_policy = config.get("search_policy", {})
    lbl = label or search_policy.get("primary_label", "bounty")
    parts = ["is:issue", "is:open"]
    if search_policy.get("exclude_assigned", True):
        parts.append("no:assignee")
        
    age_limit = max_age_days if max_age_days is not None else search_policy.get("max_issue_age_days", 14)
    if age_limit and age_limit > 0:
        cutoff = (datetime.now(timezone.utc) - timedelta(days=age_limit)).strftime("%Y-%m-%d")
        parts.append(f"created:>={cutoff}")
        
    cmt_limit = max_comments if max_comments is not None else search_policy.get("max_unresolved_comments", 20)
    if cmt_limit and cmt_limit > 0:
        parts.append(f"comments:<={cmt_limit}")
        
    parts.append(f'label:"{lbl}"')
    if task_type:
        parts.append(f'label:"{task_type}"')
    if language:
        parts.append(f"language:{language.lower()}")
    return " ".join(parts)

def get_ssl_context():
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except Exception:
        return ssl._create_unverified_context()

def fetch_json(url: str, headers: dict = None, timeout: int = 15):
    default_headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/json, text/plain, */*"}
    if headers:
        default_headers.update(headers)
    req = Request(url, headers=default_headers)
    for c in [get_ssl_context(), ssl._create_unverified_context()]:
        try:
            with urlopen(req, timeout=timeout, context=c) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as e:
            sys.stderr.write(f"HTTP Error {e.code} for URL {url}: {e.reason}\n")
            if e.code == 403:
                sys.stderr.write("Rate limit reached. Ensure authorization tokens are configured.\n")
            return None
        except (ssl.SSLError, URLError, Exception) as e:
            if c is not ctx:
                sys.stderr.write(f"Network error querying {url}: {e}\n")
                return None

def parse_github_items(items: list) -> list:
    results = []
    for item in items:
        repo_url = item.get("repository_url", "")
        repo_name = "/".join(repo_url.split("/")[-2:]) if repo_url else "N/A"
        results.append({
            "source": "GitHub",
            "number": item.get("number", ""),
            "title": item.get("title", "").replace("|", "-"),
            "repository": repo_name,
            "reward": "See labels/body",
            "comments": item.get("comments", 0),
            "created": item.get("created_at", "")[:10],
            "url": item.get("html_url", ""),
            "status": "open"
        })
    return results

def has_open_pr(repo_name: str, issue_number: int, token: str = None) -> bool:
    if not repo_name or repo_name == "N/A":
        return False
    url = f"https://api.github.com/repos/{repo_name}/issues/{issue_number}/timeline"
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"
    events = fetch_json(url, headers=headers, timeout=5)
    if not isinstance(events, list):
        return False
    for ev in events:
        if ev.get("event") == "cross-referenced":
            source = ev.get("source", {})
            issue = source.get("issue", {})
            if ("/pull/" in issue.get("html_url", "") or issue.get("pull_request")) and issue.get("state") == "open":
                return True
    return False

def search_github_issues(config: dict, query: str, token: str = None, limit: int = 10, exclude_prs: bool = True) -> list:
    search_policy = config.get("search_policy", {})
    endpoint = search_policy.get("github_search_endpoint", "https://api.github.com/search/issues")
    fetch_limit = min(limit * 2, 30) if exclude_prs else limit
    url = f"{endpoint}?q={quote_plus(query)}&sort=created&order=desc&per_page={fetch_limit}"
    
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"
    else:
        sys.stderr.write("Notice: GITHUB_TOKEN not set. Running unauthenticated (strict rate limits apply).\n")
        
    data = fetch_json(url, headers=headers)
    items = []
    if not data or not isinstance(data, dict):
        gh_bin = shutil.which("gh")
        if gh_bin:
            try:
                cmd = [gh_bin, "api", f"search/issues?q={quote_plus(query)}&sort=created&order=desc&per_page={fetch_limit}"]
                res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=20)
                if res.returncode == 0 and res.stdout.strip():
                    items = parse_github_items(json.loads(res.stdout).get("items", []))
            except Exception:
                pass
    else:
        items = parse_github_items(data.get("items", []))
        
    if not exclude_prs:
        return items[:limit]
        
    clean_items = []
    for item in items:
        repo, num = item.get("repository", ""), item.get("number")
        if num and repo and has_open_pr(repo, num, token):
            continue
        clean_items.append(item)
        if len(clean_items) >= limit:
            break
    return clean_items

def parse_reward_amount(reward_val) -> tuple:
    if isinstance(reward_val, (int, float)):
        return float(reward_val), f"${float(reward_val):.0f}"
    reward_str = str(reward_val) if reward_val else "Undisclosed"
    digits = "".join(ch for ch in reward_str if ch.isdigit() or ch == ".")
    try:
        return float(digits) if digits else 0, reward_str
    except ValueError:
        return 0, reward_str

def search_algora_bounties(config: dict, language: str = None, limit: int = 10, min_reward: int = 0, max_age_days: int = None, max_comments: int = None) -> list:
    search_policy = config.get("search_policy", {})
    base_url = search_policy.get("algora_bounties_api_url", "https://api.algora.io/api/bounties")
    params = {"status": "open", "limit": limit * 2}
    if language:
        params["language"] = language
    data = fetch_json(f"{base_url}?{urlencode(params)}")
    raw_items = (data.get("bounties", data.get("items", data)) if isinstance(data, dict) else data) or []
    if not isinstance(raw_items, list):
        return []
        
    cutoff = (datetime.now(timezone.utc) - timedelta(days=max_age_days)).strftime("%Y-%m-%d") if max_age_days and max_age_days > 0 else None
    results = []
    for item in raw_items:
        r_num, r_str = parse_reward_amount(item.get("reward_formatted") or item.get("amount") or item.get("reward"))
        if min_reward > 0 and 0 < r_num < min_reward:
            continue
        created_str = (item.get("created_at") or "")[:10]
        if cutoff and created_str and created_str < cutoff:
            continue
        issue = item.get("issue") or {}
        comments = issue.get("comments", 0) if isinstance(issue, dict) else 0
        if max_comments and max_comments > 0 and comments > max_comments:
            continue
        repo = (item.get("repository") or {}).get("name") or item.get("repo_name") or "N/A"
        results.append({
            "source": "Algora", "number": issue.get("number") or item.get("issue_number", "N/A"),
            "title": (issue.get("title") or item.get("title", "")).replace("|", "-"),
            "repository": repo, "reward": r_str, "comments": comments, "created": created_str,
            "url": item.get("url") or issue.get("html_url") or item.get("issue_url", ""), "status": "open"
        })
        if len(results) >= limit:
            break
    return results

def search_polar_bounties(config: dict, language: str = None, limit: int = 10, min_reward: int = 0, max_age_days: int = None, max_comments: int = None) -> list:
    search_policy = config.get("search_policy", {})
    base_url = search_policy.get("polar_bounties_api_url", "https://api.polar.sh/api/v1/issues")
    data = fetch_json(f"{base_url}?{urlencode({'is_funded': 'true', 'limit': limit * 2})}")
    raw_items = (data.get("items", data) if isinstance(data, dict) else data) or []
    if not isinstance(raw_items, list):
        return []
        
    cutoff = (datetime.now(timezone.utc) - timedelta(days=max_age_days)).strftime("%Y-%m-%d") if max_age_days and max_age_days > 0 else None
    results = []
    for item in raw_items:
        funding = item.get("funding") or {}
        pledges_sum = funding.get("pledges_sum") or {}
        reward_usd = (pledges_sum.get("amount", 0) / 100) if isinstance(pledges_sum, dict) else 0
        if min_reward > 0 and reward_usd < min_reward:
            continue
        created_str = (item.get("issue_created_at") or item.get("created_at") or "")[:10]
        if cutoff and created_str and created_str < cutoff:
            continue
        comments = item.get("comments", 0)
        if max_comments and max_comments > 0 and comments > max_comments:
            continue
        repo = (item.get("repository") or {}).get("name") or "N/A"
        results.append({
            "source": "Polar", "number": item.get("number", "N/A"),
            "title": item.get("title", "").replace("|", "-"), "repository": repo,
            "reward": f"${reward_usd:.0f}" if reward_usd > 0 else "Pledged", "comments": comments,
            "created": created_str, "url": item.get("html_url") or f"https://github.com/{repo}/issues/{item.get('number')}",
            "status": "funded" if funding else "open"
        })
        if len(results) >= limit:
            break
    return results

def main():
    parser = argparse.ArgumentParser(description="Query open-source bounty issues across GitHub, Algora, and Polar.")
    parser.add_argument("--source", "-s", choices=["all", "github", "algora", "polar"], default="all", help="Target bounty source platform")
    parser.add_argument("--language", "-l", help="Target programming language (e.g. typescript, python, go, rust)")
    parser.add_argument("--type", "-t", choices=["bug", "feature", "enhancement", "documentation"], help="Filter by issue type")
    parser.add_argument("--label", help="Target issue label for GitHub queries (default: from config.json)")
    parser.add_argument("--limit", "-n", type=int, default=10, help="Maximum number of issues to retrieve")
    parser.add_argument("--min-reward", "-m", type=int, default=0, help="Minimum reward in USD")
    parser.add_argument("--max-age", type=int, help="Maximum issue age in days (default: 14 from config)")
    parser.add_argument("--max-comments", type=int, help="Maximum unresolved comments threshold (default: 20 from config)")
    parser.add_argument("--include-prs", action="store_true", help="Include issues that already have open PRs referencing them")
    parser.add_argument("--json", action="store_true", help="Output raw JSON instead of markdown table")
    args = parser.parse_args()

    config = load_config()
    search_policy = config.get("search_policy", {})
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        try:
            res = subprocess.run("gh auth token", capture_output=True, text=True, shell=True, timeout=5)
            if res.returncode == 0:
                token = res.stdout.strip() or None
        except Exception:
            pass
    min_reward = args.min_reward or search_policy.get("min_reward_usd", 0)
    max_age = args.max_age if args.max_age is not None else search_policy.get("max_issue_age_days", 14)
    max_comments = args.max_comments if args.max_comments is not None else search_policy.get("max_unresolved_comments", 20)
    exclude_prs = not args.include_prs and search_policy.get("exclude_issues_with_open_prs", True)
    all_issues = []
    if args.source in ("all", "github"):
        gh_query = build_search_query(config, args.language, args.label, args.type, max_age, max_comments)
        gh_issues = search_github_issues(config, gh_query, token, args.limit, exclude_prs)
        all_issues.extend(gh_issues)
        
    if args.source in ("all", "algora"):
        algora_issues = search_algora_bounties(config, args.language, args.limit, min_reward, max_age, max_comments)
        all_issues.extend(algora_issues)
        
    if args.source in ("all", "polar"):
        polar_issues = search_polar_bounties(config, args.language, args.limit, min_reward, max_age, max_comments)
        all_issues.extend(polar_issues)
        
    if args.json:
        print(json.dumps(all_issues, indent=2))
        return

    if not all_issues:
        print("No open, uncontested bounty issues found matching current criteria.")
        return

    print(f"### Found {len(all_issues)} Fresh & Unresolved Bounty Candidates (Max Age: {max_age}d, Max Comments: {max_comments})\n")
    print("| Source | # | Title | Repository | Reward | Comments | Created | URL |")
    print("|---|---|---|---|---|---|---|---|")
    for item in all_issues:
        src, num = item.get("source", "N/A"), item.get("number", "N/A")
        title, repo = item.get("title", "N/A"), item.get("repository", "N/A")
        reward, comments = item.get("reward", "N/A"), item.get("comments", 0)
        created, url = item.get("created", "N/A"), item.get("url", "")
        print(f"| {src} | {num} | [{title}]({url}) | {repo} | {reward} | {comments} | {created} | [Link]({url}) |")

if __name__ == "__main__":
    main()
