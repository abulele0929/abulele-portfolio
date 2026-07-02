"""Wire live GitHub data into the static build.

On every build this plugin enriches a curated list of featured projects with
live repository data (stars, language, last push, homepage) and appends any
other public repositories that are not already featured. Every network call is
best-effort: if GitHub is unreachable the site still builds from the curated
data alone, so the Projects page is never empty.

The results are exposed to templates as the all-caps settings
``FEATURED_PROJECTS`` and ``GITHUB_REPOS``.
"""

import os

import requests
from pelican import signals

API = "https://api.github.com"
TIMEOUT = 8

# Curated, hand-written source of truth. ``repo`` (``owner/name``) is optional;
# when present the card is enriched with live data from the GitHub API.
FEATURED_PROJECTS = [
    {
        "name": "Waypoint",
        "status": "in progress",
        "description": (
            "A personal workflow ecosystem where different agents handle "
            "different tasks and brief me each morning on what needs doing "
            "that day. Docs-first by design, so the plan is written before "
            "the code."
        ),
        "tags": ["Python", "Markdown", "Agents"],
        "repo": None,
        "journal": "/project-journey-waypoint.html",
    },
    {
        "name": "Study & Coding Tracker",
        "status": "in progress",
        "description": (
            "A Python CLI for tracking study and coding sessions. A small "
            "tool with a big purpose: learning user input, data handling, "
            "and error handling by building something I actually use."
        ),
        "tags": ["Python", "CLI"],
        "repo": None,
        "journal": "/from-the-pitch-to-the-keyboard.html",
    },
    {
        "name": "This Portfolio",
        "status": "shipping",
        "description": (
            "A Pelican static site built with Markdown, Jinja2 templates, "
            "and vanilla CSS. Hand-built theme, dark mode, and a habit of "
            "learning in public."
        ),
        "tags": ["Pelican", "Jinja2", "CSS"],
        "repo": "abulele0929/abulele-portfolio",
        "journal": "/building-this-portfolio-while-learning.html",
    },
]


def _headers():
    token = os.environ.get("GITHUB_TOKEN")
    return {"Authorization": f"token {token}"} if token else {}


def _get(url, **params):
    try:
        r = requests.get(url, headers=_headers(), params=params, timeout=TIMEOUT)
        if r.status_code == 200:
            return r.json()
    except requests.RequestException:
        pass
    return None


def _clean(repo):
    return {
        "name": repo["name"],
        "description": repo.get("description") or "No description yet.",
        "url": repo["html_url"],
        "language": repo.get("language") or "",
        "stars": repo.get("stargazers_count", 0),
        "updated": (repo.get("pushed_at") or "")[:10],
        "live": repo.get("homepage") or None,
    }


def _enrich(project):
    """Return a copy of a featured project merged with live repo data."""
    card = dict(project)
    card.setdefault("url", None)
    card.setdefault("live", None)
    card.setdefault("stars", None)
    card.setdefault("language", None)
    card.setdefault("updated", None)

    repo = project.get("repo")
    if not repo:
        return card

    data = _get(f"{API}/repos/{repo}")
    if not data:
        return card

    info = _clean(data)
    card["url"] = info["url"]
    card["live"] = info["live"]
    card["stars"] = info["stars"]
    card["language"] = info["language"]
    card["updated"] = info["updated"]
    if not project.get("description"):
        card["description"] = info["description"]
    return card


def _extra_repos(username, featured_names, limit=6):
    """Public, non-fork repos not already featured, newest first."""
    data = _get(f"{API}/users/{username}/repos", sort="updated", per_page=100)
    if not isinstance(data, list):
        return []

    repos = []
    for repo in data:
        if repo.get("fork"):
            continue
        if repo["name"].lower() in featured_names:
            continue
        repos.append(_clean(repo))

    repos.sort(key=lambda r: r["updated"], reverse=True)
    return repos[:limit]


def fetch_projects(pelican):
    settings = pelican.settings
    username = settings.get("GITHUB_USERNAME") or os.environ.get("GITHUB_USERNAME")

    featured = [_enrich(p) for p in FEATURED_PROJECTS]

    extra = []
    if username:
        featured_names = {p["name"].lower() for p in FEATURED_PROJECTS}
        featured_names |= {
            p["repo"].split("/")[-1].lower()
            for p in FEATURED_PROJECTS
            if p.get("repo")
        }
        extra = _extra_repos(username, featured_names)

    settings["FEATURED_PROJECTS"] = featured
    settings["GITHUB_REPOS"] = extra


def register():
    signals.initialized.connect(fetch_projects)
