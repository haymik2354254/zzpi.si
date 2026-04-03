import os
import json

print("=== Current working directory ===")
print(os.getcwd())
print("\n=== Files in root ===")
print(os.listdir('.'))

print("\n=== Does 'content' folder exist? ===")
if os.path.exists('content'):
    print("Yes")
    files = sorted(os.listdir('content'))
    print(f"Files found in content/ ({len(files)} files):")
    for f in files:
        print("   " + f)
else:
    print("No - content folder is missing!")

print("\n=== Checking against future_blogs.json ===")
with open('future_blogs.json', 'r', encoding='utf-8') as f:
    blogs = json.load(f)

for i, blog in enumerate(blogs, 1):
    expected = blog['content_file']
    if os.path.exists(expected):
        print(f"✅ {i:2d}. Found: {expected}")
    else:
        print(f"❌ {i:2d}. NOT FOUND: {expected}")