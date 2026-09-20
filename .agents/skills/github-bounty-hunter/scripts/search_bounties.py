#!/usr/bin/env python3
"""
Utility script to search GitHub for open bounty issues.
Reads operational policies from config.json to avoid hardcoded search parameters.
"""

import os
import sys
import json
import argparse
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

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
    labels = [label] if label else search_policy.get("default_labels", ["bounty"])
    
    parts = ["is:issue", "is:open"]
    if search_policy.get("exclude_assigned", True):
        parts.append("no:assignee")
        
    for lbl in labels:
        parts.append(f'label:"{lbl}"')
        
    if language:
        parts.append(f"language:{language.lower()}")
        
    return " ".join(parts)

def search_github_issues(query: str, token: str = None, limit: int = 10) -> list:
    url = f"https://api.github.com/search/issues?q={query}&sort=created&order=desc&per_page={limit}"
    headers = {
        "User-Agent": "GitHub-Bounty-Hunter-Skill/1.0",
        "Accept": "application/vnd.github.v3+json"
    }
    if token:
        headers["Authorization"] = f"token {token}"
        
    req = Request(url, headers=headers)
    try:
        with urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode("utf-8"))
            return data.get("items", [])
    except HTTPError as e:
        sys.stderr.write(f"GitHub API HTTP Error {e.code}: {e.reason}\n")
        if e.code == 403:
            sys.stderr.write("Rate limit reached. Provide a GITHUB_TOKEN to increase limits.\n")
        return []
    except URLError as e:
        sys.stderr.write(f"Network error querying GitHub API: {e.reason}\n")
        return []

def main():
    parser = argparse.ArgumentParser(description="Query open-source bounty issues on GitHub.")
    parser.add_argument("--language", "-l", help="Target programming language (e.g. typescript, python, go, rust)")
    parser.add_argument("--label", help="Target issue label (default: from config.json)")
    parser.add_argument("--limit", "-n", type=int, default=10, help="Maximum number of issues to retrieve")
    parser.add_argument("--json", action="store_true", help="Output raw JSON instead of markdown table")
    args = parser.parse_args()

    config = load_config()
    token = os.environ.get("GITHUB_TOKEN")
    query = build_search_query(config, args.language, args.label)
    
    issues = search_github_issues(query, token, args.limit)
    
    if args.json:
        print(json.dumps(issues, indent=2))
        return

    if not issues:
        print(f"No open bounty issues found for query: `{query}`")
        return

    print(f"### Found {len(issues)} Bounty Candidates (Query: `{query}`)\n")
    print("| # | Title | Repository | Comments | Created | URL |")
    print("|---|---|---|---|---|---|")
    for item in issues:
        repo_url = item.get("repository_url", "")
        repo_name = "/".join(repo_url.split("/")[-2:]) if repo_url else "N/A"
        title = item.get("title", "").replace("|", "-")
        number = item.get("number", "")
        comments = item.get("comments", 0)
        created = item.get("created_at", "")[:10]
        html_url = item.get("html_url", "")
        print(f"| {number} | [{title}]({html_url}) | {repo_name} | {comments} | {created} | [Link]({html_url}) |")

if __name__ == "__main__":
    main()
