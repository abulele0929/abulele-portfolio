import os
import requests
from datetime import datetime, timedelta

_cache = {"data": None, "timestamp": None}
CACHE_DURATION = timedelta(minutes=30)

def get_repos():
    now = datetime.now()
    if _cache["data"] and _cache["timestamp"] and now - _cache["timestamp"] < CACHE_DURATION:
        return _cache["data"]

    username = os.environ.get("GITHUB_USERNAME")
    token = os.environ.get("GITHUB_TOKEN")

    url = f"https://api.github.com/users/{username}/repos"
    headers = {"Authorization": f"token {token}"} if token else {}
    params = {"sort": "updated", "per_page": 100}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=5)
        response.raise_for_status()
        repos = response.json()

        cleaned = [
            {
                "name": r["name"],
                "description": r["description"] or "No description yet.",
                "url": r["html_url"],
                "language": r["language"] or "—",
                "stars": r["stargazers_count"],
                "updated": r["updated_at"][:10],
                "deployment_url": r.get("homepage"),
                "status": _get_status(r),
            }
            for r in repos
            if not r["fork"]
        ]

        _cache["data"] = cleaned
        _cache["timestamp"] = now
        return cleaned

    except requests.RequestException:
        return []

def _get_status(repo):
    if repo.get("homepage"):
        return "live"
    return "wip"