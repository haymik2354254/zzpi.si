# generate_blogs.py  (Updated - nice image names in public folder)
import os
import json
import shutil
import sys
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('templates'))
detail_template = env.get_template('blog-detail.html')

def main(mode="obfuscated"):
    print(f"🚀 Generating blog posts... (mode: {mode})")

    with open("future_blogs.json", "r", encoding="utf-8") as f:
        future_blogs = json.load(f)

    today = datetime.now().strftime("%Y-%m-%d")
    posts = []

    for blog in future_blogs:
        date = blog.get("date")
        if date > today:
            print(f"⏳ Skipping future post: {blog['title']} ({date})")
            continue

        real_slug = blog.get("real_slug")
        if not real_slug:
            real_slug = os.path.splitext(os.path.basename(blog.get("content_file", "")))[0]

        # Determine paths based on mode
        if mode == "local":
            content_path = os.path.join("content", f"{real_slug}.html")
            image_src = os.path.join("images", f"{real_slug}.jpg")
            public_image_name = f"{real_slug}.jpg"
        else:  # obfuscated mode
            content_path = os.path.join("src", blog["content_file"])
            image_src = os.path.join("src/images", blog["image"])
            public_image_name = f"{real_slug}.jpg"   # Nice name for public

        if not os.path.exists(content_path):
            print(f"⚠️ Warning: Content file not found: {content_path}")
            continue

        with open(content_path, "r", encoding="utf-8") as f:
            content = f.read()

        blog_filename = f"{real_slug}.html"
        output_path = os.path.join("blogs", blog_filename)

        # Render detail page - use nice image name
        rendered = detail_template.render(
            title=blog["title"],
            date=date,
            image=public_image_name,      # <--- Important change
            content=content,
            meta=blog.get("meta", "")
        )

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(rendered)

        # Copy image with nice name to public images/
        dest_image = os.path.join("images", public_image_name)
        if os.path.exists(image_src):
            shutil.copy2(image_src, dest_image)
            print(f"✅ Image copied as: images/{public_image_name}")
        else:
            print(f"⚠️ Missing image source: {image_src}")

        posts.append({
            "title": blog["title"],
            "date": date,
            "excerpt": blog.get("excerpt", ""),
            "image": public_image_name,      # nice name
            "url": f"blogs/{real_slug}.html",
            "meta": blog.get("meta", "")
        })

        print(f"✅ Generated: blogs/{blog_filename}")

    os.makedirs("data", exist_ok=True)
    with open("data/posts.json", "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)

    print(f"\n🎉 Generation completed in {mode} mode!")

if __name__ == "__main__":
    mode = "local" if len(sys.argv) > 1 and sys.argv[1] == "--local" else "obfuscated"
    main(mode)