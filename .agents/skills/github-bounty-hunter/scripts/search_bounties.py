#!/usr/bin/env python3
"""
Utility script to search GitHub, Algora, and Polar for open bounty issues.
Reads operational policies from config.json to avoid hardcoded search parameters.
"""

import os
import sys
import ssl
import json
import shutil
import argparse
import subprocess
from pathlib import Path
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

def build_search_query(config: dict, language: str = None, label: str = None) -> str:
    search_policy = config.get("search_policy", {})
    lbl = label or search_policy.get("primary_label", "bounty")
    
    parts = ["is:issue", "is:open"]
    if search_policy.get("exclude_assigned", True):
        parts.append("no:assignee")
        
    parts.append(f'label:"{lbl}"')
        
    if language:
        parts.append(f"language:{language.lower()}")
        
    return " ".join(parts)

def get_ssl_context():
    # 1. Try certifi bundle if available (bypasses Windows cert store ASN1 corruption)
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except Exception:
        pass
    # 2. Try standard system context
    try:
        return ssl.create_default_context()
    except Exception:
        pass
    # 3. Fallback to unverified context
    try:
        return ssl._create_unverified_context()
    except Exception:
        return None

def fetch_json(url: str, headers: dict = None, timeout: int = 15):
    default_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*"
    }
    if headers:
        default_headers.update(headers)
    req = Request(url, headers=default_headers)
    ctx = get_ssl_context()
    
    for c in [ctx, ssl._create_unverified_context()]:
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
def search_github_via_gh_cli(query: str, limit: int = 10) -> list:
    gh_bin = shutil.which("gh")
    if not gh_bin:
        return []
    try:
        cmd = [gh_bin, "api", f"search/issues?q={quote_plus(query)}&sort=created&order=desc&per_page={limit}"]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=20)
        if result.returncode == 0 and result.stdout.strip():
            data = json.loads(result.stdout)
            return parse_github_items(data.get("items", []))
    except Exception:
        pass
    return []

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

def search_github_issues(config: dict, query: str, token: str = None, limit: int = 10) -> list:
    search_policy = config.get("search_policy", {})
    endpoint = search_policy.get("github_search_endpoint", "https://api.github.com/search/issues")
    encoded_query = quote_plus(query)
    url = f"{endpoint}?q={encoded_query}&sort=created&order=desc&per_page={limit}"
    
    headers = {
        "Accept": "application/vnd.github.v3+json"
    }
    if token:
        headers["Authorization"] = f"token {token}"
    else:
        sys.stderr.write("Notice: GITHUB_TOKEN not set. Running unauthenticated (strict rate limits apply).\n")
        
    data = fetch_json(url, headers=headers)
    if not data or not isinstance(data, dict):
        # Fallback to gh CLI if urllib encountered an environment issue
        cli_results = search_github_via_gh_cli(query, limit)
        if cli_results:
            return cli_results
        return []
    
    return parse_github_items(data.get("items", []))

def search_algora_bounties(config: dict, language: str = None, limit: int = 10, min_reward: int = 0) -> list:
    search_policy = config.get("search_policy", {})
    base_url = search_policy.get("algora_bounties_api_url", "https://api.algora.io/api/bounties")
    
    params = {"status": "open", "limit": limit}
    if language:
        params["language"] = language
    query_string = urlencode(params)
    url = f"{base_url}?{query_string}"
    
    data = fetch_json(url)
    if not data:
        return []
        
    raw_items = data.get("bounties", data.get("items", data)) if isinstance(data, dict) else data
    if not isinstance(raw_items, list):
        return []
        
    results = []
    for item in raw_items[:limit]:
        reward_val = item.get("reward_formatted") or item.get("amount") or item.get("reward")
        reward_num = 0
        if isinstance(reward_val, (int, float)):
            reward_num = float(reward_val)
            reward_str = f"${reward_num:.0f}"
        else:
            reward_str = str(reward_val) if reward_val else "Undisclosed"
            digits = "".join(ch for ch in reward_str if ch.isdigit() or ch == ".")
            if digits:
                try:
                    reward_num = float(digits)
                except ValueError:
                    reward_num = 0

        if min_reward > 0 and reward_num > 0 and reward_num < min_reward:
            continue

        issue = item.get("issue") or {}
        repo_info = item.get("repository") or {}
        repo_name = repo_info.get("name") or item.get("repo_name") or "N/A"
        
        results.append({
            "source": "Algora",
            "number": issue.get("number") or item.get("issue_number", "N/A"),
            "title": (issue.get("title") or item.get("title", "")).replace("|", "-"),
            "repository": repo_name,
            "reward": reward_str,
            "comments": issue.get("comments", 0) if isinstance(issue, dict) else 0,
            "created": (item.get("created_at") or "")[:10],
            "url": item.get("url") or issue.get("html_url") or item.get("issue_url", ""),
            "status": item.get("status", "open")
        })
    return results

def search_polar_bounties(config: dict, language: str = None, limit: int = 10, min_reward: int = 0) -> list:
    search_policy = config.get("search_policy", {})
    base_url = search_policy.get("polar_bounties_api_url", "https://api.polar.sh/api/v1/issues")
    
    params = {"is_funded": "true", "limit": limit}
    query_string = urlencode(params)
    url = f"{base_url}?{query_string}"
    
    data = fetch_json(url)
    if not data:
        return []
        
    raw_items = data.get("items", data) if isinstance(data, dict) else data
    if not isinstance(raw_items, list):
        return []
        
    results = []
    for item in raw_items[:limit]:
        funding = item.get("funding") or {}
        pledges_sum = funding.get("pledges_sum") or {}
        amount_cents = pledges_sum.get("amount", 0) if isinstance(pledges_sum, dict) else 0
        reward_usd = amount_cents / 100 if amount_cents else 0
        
        if min_reward > 0 and reward_usd < min_reward:
            continue
            
        reward_str = f"${reward_usd:.0f}" if reward_usd > 0 else "Pledged"
        repo = item.get("repository") or {}
        repo_name = repo.get("name") if isinstance(repo, dict) else "N/A"
        
        results.append({
            "source": "Polar",
            "number": item.get("number", "N/A"),
            "title": item.get("title", "").replace("|", "-"),
            "repository": repo_name,
            "reward": reward_str,
            "comments": item.get("comments", 0),
            "created": (item.get("issue_created_at") or item.get("created_at") or "")[:10],
            "url": item.get("html_url") or f"https://github.com/{repo_name}/issues/{item.get('number')}",
            "status": "funded" if funding else "open"
        })
    return results

def main():
    parser = argparse.ArgumentParser(description="Query open-source bounty issues across GitHub, Algora, and Polar.")
    parser.add_argument("--source", "-s", choices=["all", "github", "algora", "polar"], default="all", help="Target bounty source platform")
    parser.add_argument("--language", "-l", help="Target programming language (e.g. typescript, python, go, rust)")
    parser.add_argument("--label", help="Target issue label for GitHub queries (default: from config.json)")
    parser.add_argument("--limit", "-n", type=int, default=10, help="Maximum number of issues to retrieve")
    parser.add_argument("--min-reward", "-m", type=int, default=0, help="Minimum reward in USD")
    parser.add_argument("--json", action="store_true", help="Output raw JSON instead of markdown table")
    args = parser.parse_args()

    config = load_config()
    token = os.environ.get("GITHUB_TOKEN")
    min_reward = args.min_reward or config.get("search_policy", {}).get("min_reward_usd", 0)
    
    all_issues = []
    
    if args.source in ("all", "github"):
        gh_query = build_search_query(config, args.language, args.label)
        gh_issues = search_github_issues(config, gh_query, token, args.limit)
        all_issues.extend(gh_issues)
        
    if args.source in ("all", "algora"):
        algora_issues = search_algora_bounties(config, args.language, args.limit, min_reward)
        all_issues.extend(algora_issues)
        
    if args.source in ("all", "polar"):
        polar_issues = search_polar_bounties(config, args.language, args.limit, min_reward)
        all_issues.extend(polar_issues)
        
    if args.json:
        print(json.dumps(all_issues, indent=2))
        return

    if not all_issues:
        print("No open bounty issues found matching current criteria.")
        return

    print(f"### Found {len(all_issues)} Bounty Candidates\n")
    print("| Source | # | Title | Repository | Reward | Comments | Created | URL |")
    print("|---|---|---|---|---|---|---|---|")
    for item in all_issues:
        src = item.get("source", "N/A")
        num = item.get("number", "N/A")
        title = item.get("title", "N/A")
        repo = item.get("repository", "N/A")
        reward = item.get("reward", "N/A")
        comments = item.get("comments", 0)
        created = item.get("created", "N/A")
        url = item.get("url", "")
        print(f"| {src} | {num} | [{title}]({url}) | {repo} | {reward} | {comments} | {created} | [Link]({url}) |")

if __name__ == "__main__":
    main()
