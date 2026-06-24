import os
import re
import markdown

POSTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "content", "posts")

def _parse_post(filename):
    path = os.path.join(POSTS_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read()

    match = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.DOTALL)
    if not match:
        return None

    frontmatter_raw, body = match.groups()
    meta = {}
    for line in frontmatter_raw.strip().split("\n"):
        key, _, value = line.partition(":")
        meta[key.strip()] = value.strip()

    slug = filename.replace(".md", "")

    word_count = len(body.split())
    read_time = max(1, round(word_count / 200))

    return {
        "slug": slug,
        "title": meta.get("title", "Untitled"),
        "date": meta.get("date", ""),
        "html": markdown.markdown(body.strip()),
        "excerpt": body.strip().split("\n\n")[0][:160],
        "read_time": read_time,
    }

def get_all_posts():
    if not os.path.exists(POSTS_DIR):
        return []

    posts = []
    for filename in os.listdir(POSTS_DIR):
        if filename.endswith(".md"):
            post = _parse_post(filename)
            if post:
                posts.append(post)

    return sorted(posts, key=lambda p: p["date"], reverse=True)

def get_post_by_slug(slug):
    filename = f"{slug}.md"
    if not os.path.exists(os.path.join(POSTS_DIR, filename)):
        return None
    return _parse_post(filename)