import marko
import sass
from bs4 import BeautifulSoup
from pathlib import Path
import os


def generate_head() -> str:
    with open("elements/head/head.html", "r") as file:
        head_html = file.read()
        return head_html


def generate_nav_bar_html() -> str:
    with open("elements/navbar/navbar.html", "r") as file:
        navbar_html = file.read()
        output = f"<header>{navbar_html}</header>"
        return output


def generate_footer_html() -> str:
    with open("elements/footer/footer.html", "r") as file:
        html = file.read()
        output = f"{html}"
        return output


def generate_nav_bar_css() -> str:
    with open("elements/navbar/navbar.css", "r") as file:
        navbar_css = file.read()
        return "\n\n/* ---Navbar--- */\n\n" + navbar_css


def generate_footer_css() -> str:
    with open("elements/footer/footer.css", "r") as file:
        css = file.read()
        return "\n\n/* ---Footer--- */\n\n" + css


posts_dir = Path("./posts")
dist_dir = Path("./post")
elements_dir = Path("./elements")

# Create the dist directory if it does not exist
dist_dir.mkdir(exist_ok=True)

posts = []
for post_path in posts_dir.glob("*.md"):
    html_file_name = post_path.with_suffix(".html").name
    html_file_path = dist_dir / html_file_name
    posts.append(str(html_file_path.stem))

    print(f"processing {post_path}")
    # Read the Markdown file and convert it to HTML
    with open(post_path, "r", encoding="utf-8") as file:
        html_content = marko.convert(file.read())

    # Write the HTML content to the corresponding file
    with open(html_file_path, "w", encoding="utf-8") as file:
        file.write("<!DOCTYPE html>\n")
        file.write('<html lang="en">\n')
        file.write(generate_head())
        file.write(generate_nav_bar_html())
        file.write(html_content)
        file.write(generate_footer_html())
        file.write("\n</html>")

# generate css
css = ""
with open("elements/index/index.scss", "r") as scss_file:
    scss = scss_file.read()
    css = sass.compile(string=scss)

with open("index.css", "w") as css_file:
    css_file.write(f"/* --index-- */\n\n{css}")

with open("index.css", "a") as file:
    file.write(generate_nav_bar_css())
    file.write(generate_footer_css())

# generate index.html, i.e add new posts
with open("elements/index/index.html", "r") as file:
    soup = BeautifulSoup(file, "html.parser")

content_section = soup.find("section", class_="content")

post_list = soup.new_tag("ul")
for post in posts:
    link = soup.new_tag("a", href=f"post/{post}")
    link.string = post
    post_tag = soup.new_tag("li")
    post_tag.insert(0, link)
    post_list.append(post_tag)
content_section.insert(0, post_list)

with open("elements/navbar/navbar.html", "r") as file:
    navbar_soup = BeautifulSoup(file, "html.parser")
with open("elements/footer/footer.html", "r") as file:
    footer_soup = BeautifulSoup(file, "html.parser")

html_tag = soup.find("html")
html_tag.append(footer_soup)
html_tag.insert(2, navbar_soup)

with open("index.html", "w") as file:
    file.write(str(soup.prettify()))
