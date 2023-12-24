import marko
import sass
from bs4 import BeautifulSoup
from pathlib import Path
import os

def generate_head() -> str:
    with open('elements/head/head.html', "r") as file:
        head_html = file.read()
        return head_html
    
    # TODO: dynamically change meta description and  title based on blog post

def generate_nav_bar_html() -> str:
    with open('elements/navbar/navbar.html', "r") as file:
        navbar_html = file.read()
        output = f"<header>{navbar_html}</header>"
        return output

def generate_nav_bar_css() -> str:
    with open('elements/navbar/navbar.css', "r") as file:
        navbar_css = file.read()
        return "\n\n/* ---Navbar--- */\n\n" + navbar_css 
    
def get_latest_mod_time(path: Path) -> float:
    latest_mod_time = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            file_mod_time = os.path.getmtime(os.path.join(root, file))
            latest_mod_time = max(latest_mod_time, file_mod_time)
    return latest_mod_time

posts_dir = Path("./posts")
dist_dir = Path("./post")
elements_dir = Path("./elements")

# Create the dist directory if it does not exist
dist_dir.mkdir(exist_ok=True)

# Get the latest modification time of the elements folder
elements_mod_time = get_latest_mod_time(elements_dir)

posts = []
for post_path in posts_dir.glob("*.md"):
    html_file_name = post_path.with_suffix('.html').name
    html_file_path = dist_dir / html_file_name
    posts.append(str(html_file_path.stem))

    # Check if the html file exists and compare modification times
    should_regenerate = not html_file_path.exists() or post_path.stat().st_mtime > html_file_path.stat().st_mtime

    # Check if any elements file is newer than the html file
    should_regenerate = should_regenerate or (html_file_path.exists() and elements_mod_time > html_file_path.stat().st_mtime)

    if should_regenerate:
        print(f"processing {post_path}")
        # Read the Markdown file and convert it to HTML
        with open(post_path, 'r', encoding='utf-8') as file:
            html_content = marko.convert(file.read())

        # Write the HTML content to the corresponding file
        with open(html_file_path, 'w', encoding='utf-8') as file:
            file.write("<!DOCTYPE html>\n")
            file.write('<html lang="en">\n')
            file.write(generate_head())
            file.write(generate_nav_bar_html())
            file.write(html_content)
            file.write("\n</html>")
        
# generate css
css = ""
with open('elements/index/index.scss', "r") as scss_file:
    scss = scss_file.read()
    css = sass.compile(string=scss)

with open('index.css', "w") as css_file:
    css_file.write(f"/* --index-- */\n\n{css}")

with open('index.css', "a") as file:
    file.write(generate_nav_bar_css())

# generate index.html, i.e add new posts
with open('elements/index/index.html', "r") as file:
    soup = BeautifulSoup(file, 'html.parser')

content_section = soup.find('section', class_='content')

post_list = soup.new_tag('ul')
for post in posts:
    link = soup.new_tag("a", href=f'post/{post}')
    link.string = post
    post_tag = soup.new_tag("li")
    post_tag.insert(0,link)
    post_list.append(post_tag)
content_section.insert(0, post_list)

with open('index.html', "w") as file:
    file.write(str(soup.prettify()))
