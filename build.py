# build.py
import os
import json
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('templates'))
index_template = env.get_template('index-template.html')

def main(mode="obfuscated"):
    print(f"🏗️  Building index.html... (mode: {mode})")

    with open("data/posts.json", "r", encoding="utf-8") as f:
        posts = json.load(f)

    today = datetime.now().strftime("%Y-%m-%d")

    visible_posts = [p for p in posts if p["date"] <= today]
    visible_posts.sort(key=lambda x: x["date"], reverse=True)

    rendered = index_template.render(
        posts=visible_posts,
        today=today
    )

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(rendered)

    print(f"✅ index.html built successfully with {len(visible_posts)} visible posts.")

if __name__ == "__main__":
    import sys
    mode = "local" if len(sys.argv) > 1 and sys.argv[1] == "--local" else "obfuscated"
    main(mode)