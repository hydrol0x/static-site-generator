import marko
from pathlib import Path

posts_dir = Path("./posts")
dist_dir = Path("./dist")

# Create the dist directory if it does not exist
dist_dir.mkdir(exist_ok=True)

for post_path in posts_dir.glob("*.md"):
    html_file_name = post_path.with_suffix('.html').name
    html_file_path = dist_dir / html_file_name

    # Check if the html file exists and compare modification times
    if not html_file_path.exists() or post_path.stat().st_mtime > html_file_path.stat().st_mtime:
        print(f"processing {post_path}")
        # Read the Markdown file and convert it to HTML
        with open(post_path, 'r', encoding='utf-8') as file:
            html_content = marko.convert(file.read())

        # Write the HTML content to the corresponding file
        with open(html_file_path, 'w', encoding='utf-8') as file:
            file.write(html_content)
