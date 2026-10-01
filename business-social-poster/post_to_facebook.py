"""
post_to_facebook.py

Posts the next item from posts.json to a Facebook Page, using the
Graph API and a Page Access Token stored as a GitHub Actions secret
(FB_PAGE_TOKEN).

Each time it runs, it:
1. Reads posts.json (a list of posts for one business)
2. Reads progress.json to see which post was used last
3. Publishes the next post (text, or text + photo if an image_url is given)
4. Updates progress.json so the next run picks the next post

To run this for a different business, point POSTS_FILE / PROGRESS_FILE
at that business's files (see the workflow file for how this is wired up).
"""

import json
import os
import sys
import requests

GRAPH_API_VERSION = "v21.0"

# These two paths are passed in as environment variables from the
# GitHub Actions workflow, so the same script can run for any business.
POSTS_FILE = os.environ.get("POSTS_FILE", "horse-blanket-washing/posts.json")
PROGRESS_FILE = os.environ.get("PROGRESS_FILE", "horse-blanket-washing/progress.json")

PAGE_ID = os.environ.get("FB_PAGE_ID")  # the numeric Page ID
PAGE_TOKEN = os.environ.get("FB_PAGE_TOKEN")  # the Page access token (secret)


def load_json(path, default):
    if not os.path.exists(path):
        return default
    with open(path, "r") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def main():
    if not PAGE_ID or not PAGE_TOKEN:
        print("Missing FB_PAGE_ID or FB_PAGE_TOKEN environment variables.")
        sys.exit(1)

    posts = load_json(POSTS_FILE, [])
    if not posts:
        print(f"No posts found in {POSTS_FILE}. Add some posts first.")
        sys.exit(1)

    progress = load_json(PROGRESS_FILE, {"next_index": 0})
    index = progress.get("next_index", 0) % len(posts)
    post = posts[index]

    caption = post.get("caption", "")
    image_url = post.get("image_url")

    if image_url:
        # Posting a photo with a caption
        url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{PAGE_ID}/photos"
        payload = {
            "url": image_url,
            "caption": caption,
            "access_token": PAGE_TOKEN,
        }
    else:
        # Text-only post
        url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{PAGE_ID}/feed"
        payload = {
            "message": caption,
            "access_token": PAGE_TOKEN,
        }

    response = requests.post(url, data=payload)

    if response.status_code == 200:
        print(f"Posted successfully (post #{index}): {caption[:60]}...")
        progress["next_index"] = (index + 1) % len(posts)
        save_json(PROGRESS_FILE, progress)
    else:
        print(f"Facebook API error ({response.status_code}): {response.text}")
        sys.exit(1)


if __name__ == "__main__":
    main()
