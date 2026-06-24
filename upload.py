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
    print("auth 응답:", data)
    for part in set_cookie.split(";"):
        part = part.strip()
        if part.startswith("access_token="):
            return part[len("access_token="):]
    return None

TOKEN = get_access_token()
if not TOKEN:
    print("토큰 발급 실패")
    exit(1)
print("토큰 발급 성공")

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
    return re.sub(r'[\s_-]+', '-', slug).strip('-')[:100]

def post_to_velog(data):
    res = requests.post(API, json={
        "query": WRITE_POST,
        "variables": {
            "title": data["title"],
            "body": data["body"],
            "tags": data["tags"],
            "is_markdown": True,
            "is_temp": False,
            "is_private": False,
            "url_slug": slugify(data["title"]),
            "meta": {},
        }
    }, headers={
        "Content-Type": "application/json",
        "cookie": f"refresh_token={REFRESH_TOKEN}; access_token={TOKEN}",
        "origin": "https://velog.io",
        "referer": "https://velog.io/",
    })
    if not res.text.strip():
        return {"data": {"writePost": None}}
    try:
        return res.json()
    except Exception:
        print(f"파싱 실패 - 상태코드: {res.status_code}, 응답: {repr(res.text[:200])}")
        return {"data": {"writePost": None}}


for filepath in sorted(glob.glob("posts/**/*.md", recursive=True)):
    data = parse_md(filepath)
    if not data:
        continue
    result = post_to_velog(data)
    if "errors" in result:
        print(f"실패: {data['title']} - {result['errors']}")
    elif result.get("data", {}).get("writePost"):
        print(f"완료: {data['title']}")
    else:
        print(f"null 응답: {data['title']}")
    time.sleep(1)
