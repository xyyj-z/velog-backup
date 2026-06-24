import requests
import os
import glob
import re

TOKEN = os.environ["VELOG_TOKEN"]
API = "https://v2.velog.io/graphql"
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

WRITE_POST = """
mutation WritePost($input: WritePostInput!) {
  writePost(input: $input) {
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
        "variables": {"input": {
            "title": data["title"],
            "body": data["body"],
            "tags": data["tags"],
            "is_markdown": True,
            "is_temp": False,
            "url_slug": slugify(data["title"]),
        }}
    }, headers=HEADERS)
    return res.json()

for filepath in sorted(glob.glob("posts/**/*.md", recursive=True)):
    data = parse_md(filepath)
    if not data:
        continue
    result = post_to_velog(data)
    if "errors" in result:
        print(f"실패: {data['title']} - {result['errors']}")
    else:
        print(f"완료: {data['title']}")
