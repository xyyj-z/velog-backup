import requests
import os
import glob
import re

REFRESH_TOKEN = os.environ["VELOG_REFRESH_TOKEN"]
API = "https://v2.velog.io/graphql"

def get_access_token():
    res = requests.post(API, json={
        "query": "{ restoreToken { accessToken } }"
    }, headers={
        "Content-Type": "application/json",
        "cookie": f"refresh_token={REFRESH_TOKEN}"
    })
    data = res.json()
    token = data.get("data", {}).get("restoreToken", {}).get("accessToken")
    if not token:
        print("토큰 갱신 실패:", data)
        exit(1)
    return token


TOKEN = get_access_token()
print("토큰 발급 성공")

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "cookie": f"access_token={TOKEN}"
}

WRITE_POST = """
mutation WritePost(
  $title: String!
  $body: String!
  $tags: [String]!
  $is_markdown: Boolean!
  $is_temp: Boolean!
  $is_private: Boolean!
  $url_slug: String!
) {
  writePost(
    title: $title
    body: $body
    tags: $tags
    is_markdown: $is_markdown
    is_temp: $is_temp
    is_private: $is_private
    url_slug: $url_slug
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
        }
    }, headers=HEADERS)
    return res.json()

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
        print(f"인증 실패 또는 null 응답: {data['title']} - {result}")
