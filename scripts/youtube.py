import os
import requests
from datetime import datetime, timedelta

_cache = {"data": None, "timestamp": None}
CACHE_DURATION = timedelta(hours=12)

def get_youtube_stats():
    now = datetime.now()
    if _cache["data"] and _cache["timestamp"] and now - _cache["timestamp"] < CACHE_DURATION:
        return _cache["data"]

    api_key = os.environ.get("YOUTUBE_API_KEY")
    channel_id = os.environ.get("YOUTUBE_CHANNEL_ID")

    url = "https://www.googleapis.com/youtube/v3/channels"
    params = {
        "part": "statistics",
        "id": channel_id,
        "key": api_key,
    }

    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        stats = data["items"][0]["statistics"]
        result = {
            "subscribers": int(stats.get("subscriberCount", 0)),
            "views": int(stats.get("viewCount", 0)),
            "videos": int(stats.get("videoCount", 0)),
        }

        _cache["data"] = result
        _cache["timestamp"] = now
        return result

    except (requests.RequestException, KeyError, IndexError):
        return None