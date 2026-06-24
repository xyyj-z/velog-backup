import requests
import os
import re
from datetime import datetime

USERNAME = os.environ["VELOG_USERNAME"]
API = "https://v2.velog.io/graphql"

QUERY = """
query Posts($username: String, $cursor: ID) {
  posts(username: $username, cursor: $cursor) {
    id
    title
    body
    tags
    created_at
    series { name }
  }
}
"""

def fetch_all_posts():
    posts, cursor = [], None
    while True:
        res = requests.post(API, json={
            "query": QUERY,
            "variables": {"username": USERNAME, "cursor": cursor}
        })
        batch = res.json()["data"]["posts"]
        if not batch:
            break
        posts.extend(batch)
        cursor = batch[-1]["id"]
    return posts

def slugify(title):
    return re.sub(r'[^\w\-]', '-', title).strip('-')[:80]

def save(post):
    series = post["series"]["name"] if post["series"] else "unsorted"
    folder = f"posts/{slugify(series)}"
    os.makedirs(folder, exist_ok=True)

    date = post["created_at"][:10]
    filename = f"{folder}/{date}-{slugify(post['title'])}.md"

    tags = ", ".join(post["tags"])
    content = f"""---
title: {post['title']}
date: {date}
tags: [{tags}]
---

{post['body']}
"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

for post in fetch_all_posts():
    save(post)
    print(f"saved: {post['title']}")
