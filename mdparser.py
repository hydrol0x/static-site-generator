import marko
from pathlib import Path

posts = Path("./posts")
dist = Path("./dist")

for post in posts.glob("*.md"):
    html = ""
    with open(post, 'r') as file:
        html = marko.convert(file.read())

    write_name = dist / post.with_suffix('.html').name
    with open(write_name, 'w') as file:
        file.write(html)