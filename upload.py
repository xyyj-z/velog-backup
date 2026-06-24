import requests
import os
import glob
import re
import time

REFRESH_TOKEN = os.environ["VELOG_REFRESH_TOKEN"]
API = "https://v2.velog.io/graphql"

def get_access_token():
    res = requests.post(API, json={
        "query": "{ auth { id username } }"
    }, headers={
        "Content-Type": "application/json",
        "origin": "https://velog.io",
        "referer": "https://velog.io/",
        "cookie": f"refresh_token={REFRESH_TOKEN}"
    })
    set_cookie = res.headers.get("set-cookie", "")
    data = res.json()
    username = data["data"]["auth"]["username"]
    print(f"로그인: {username}")
    for part in set_cookie.split(";"):
        part = part.strip()
        if part.startswith("access_token="):
            return part[len("access_token="):], username
    return None, username

TOKEN, USERNAME = get_access_token()
if not TOKEN:
    print("토큰 발급 실패")
    exit(1)

HEADERS = {
    "Content-Type": "application/json",
    "cookie": f"refresh_token={REFRESH_TOKEN}; access_token={TOKEN}",
    "origin": "https://velog.io",
    "referer": "https://velog.io/",
}

def get_uploaded_titles():
    titles = set()
    cursor = None
    while True:
        variables = {"username": USERNAME}
        if cursor:
            variables["cursor"] = cursor
        res = requests.post(API, json={
            "query": """
            query Posts($username: String, $cursor: ID) {
              posts(username: $username, cursor: $cursor) {
                id
                title
              }
            }
            """,
            "variables": variables
        }, headers=HEADERS)
        batch = res.json().get("data", {}).get("posts", [])
        if not batch:
            break
        for p in batch:
            titles.add(p["title"])
        cursor = batch[-1]["id"]
    print(f"이미 업로드된 글: {len(titles)}개")
    return titles

WRITE_POST = """
mutation WritePost(
  $title: String!
  $body: String!
  $tags: [String]!
  $is_markdown: Boolean!
  $is_temp: Boolean!
  $is_private: Boolean!
  $url_slug: String!
  $meta: JSON
) {
  writePost(
    title: $title
    body: $body
    tags: $tags
    is_markdown: $is_markdown
    is_temp: $is_temp
    is_private: $is_private
    url_slug: $url_slug
    meta: $meta
  ) {
    id
    title
    url_slug
  }
}
"""

def parse_md(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if not match:
        return None
    frontmatter, body = match.group(1), match.group(2).strip()
    title = re.search(r'title: (.+)', frontmatter)
    tags = re.search(r'tags: \[(.+)\]', frontmatter)
    return {
        "title": title.group(1).strip() if title else "Untitled",
        "tags": [t.strip() for t in tags.group(1).split(',')] if tags else [],
        "body": body
    }

def slugify(title):
    slug = re.sub(r'[^\w\s-]', '', title.lower())
    return re.sub(r'[\s_-]+', '-', slug).strip('-')[:80]

def post_to_velog(data, retry=3):
    slug = slugify(data["title"]) + f"-{int(time.time()) % 10000}"
    for attempt in range(retry):
        try:
            res = requests.post(API, json={
                "query": WRITE_POST,
                "variables": {
                    "title": data["title"],
                    "body": data["body"],
                    "tags": data["tags"],
                    "is_markdown": True,
                    "is_temp": False,
                    "is_private": False,
                    "url_slug": slug,
                    "meta": {},
                }
            }, headers=HEADERS, timeout=30)

            if res.status_code == 504:
                print(f"  504 재시도 {attempt+1}/{retry}")
                time.sleep(5 * (attempt + 1))
                continue

            if not res.text.strip():
                return {"data": {"writePost": None}}

            return res.json()
        except Exception as e:
            print(f"  오류 {attempt+1}/{retry}: {e}")
            time.sleep(5)
    return {"data": {"writePost": None}}

uploaded = get_uploaded_titles()

for filepath in sorted(glob.glob("posts/**/*.md", recursive=True)):
    data = parse_md(filepath)
    if not data:
        continue
    if data["title"] in uploaded:
        print(f"스킵: {data['title']}")
        continue
    result = post_to_velog(data)
    if result.get("data", {}).get("writePost"):
        print(f"완료: {data['title']}")
    else:
        print(f"실패: {data['title']} - {result}")
    time.sleep(3)
