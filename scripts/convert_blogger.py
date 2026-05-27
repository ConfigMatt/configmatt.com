#!/usr/bin/env python3
"""
Convert Blogger Google Takeout Atom feeds to Jekyll Markdown posts.

Usage:
    python scripts/convert_blogger.py

Reads all feed.atom files from the Blogger Export folder and writes
Jekyll-compatible .md files to _posts/.

Requires: pip install html2text beautifulsoup4 lxml
"""

import os
import re
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

try:
    import html2text
except ImportError:
    print("Installing html2text...")
    os.system("pip install html2text")
    import html2text

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("Installing beautifulsoup4...")
    os.system("pip install beautifulsoup4 lxml")
    from bs4 import BeautifulSoup

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent
EXPORT_ROOT = REPO_ROOT / "Blogger Export" / "Takeout" / "Blogger" / "Blogs"
POSTS_DIR = REPO_ROOT / "_posts"

POSTS_DIR.mkdir(exist_ok=True)

# Atom namespace map
NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "blogger": "http://schemas.google.com/blogger/2018",
}

# ---------------------------------------------------------------------------
# HTML → Markdown converter setup
# ---------------------------------------------------------------------------
h = html2text.HTML2Text()
h.ignore_links = False
h.ignore_images = False
h.body_width = 0          # Don't wrap long lines
h.protect_links = True
h.wrap_links = False


def html_to_markdown(html_content: str) -> str:
    """Convert Blogger HTML to clean Markdown."""
    # Pre-clean: strip inline style div wrappers that Blogger loves
    soup = BeautifulSoup(html_content, "lxml")

    # Replace <div class="MsoNormal" ...> with just their text content
    # (these are copy-paste artifacts from Word/Outlook)
    for div in soup.find_all("div"):
        classes = div.get("class", [])
        style = div.get("style", "")
        if "MsoNormal" in classes or "separator" not in classes:
            div.unwrap()

    # Remove <u></u> artifacts (empty underline tags from Word)
    for u in soup.find_all("u"):
        if not u.get_text(strip=True):
            u.decompose()

    cleaned_html = str(soup)
    md = h.handle(cleaned_html)

    # Post-clean: collapse runs of blank lines to max 2
    md = re.sub(r"\n{3,}", "\n\n", md)
    return md.strip()


def slugify(title: str) -> str:
    """Turn a title into a URL-safe slug."""
    slug = title.lower()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug)
    slug = re.sub(r"-+", "-", slug)
    return slug.strip("-")[:80]


def parse_date(date_str: str) -> datetime:
    """Parse an ISO 8601 date string into a datetime."""
    # e.g. "2017-06-29T22:52:00.002Z"
    date_str = date_str.replace("Z", "+00:00")
    return datetime.fromisoformat(date_str)


def write_post(title: str, published: datetime, content_html: str,
               tags: list[str], blogger_filename: str, blog_name: str,
               author: str = "Matt Atkinson") -> Path:
    """Write a single Jekyll _posts file."""
    date_str = published.strftime("%Y-%m-%d")
    slug = slugify(title)
    filename = f"{date_str}-{slug}.md"
    filepath = POSTS_DIR / filename

    # Build front matter
    tags_yaml = ""
    if tags:
        tag_list = "\n".join(f'  - "{t}"' for t in tags)
        tags_yaml = f"tags:\n{tag_list}\n"

    # Map blog name to a category
    category_map = {
        "ConfigMgr Field Notes": "ConfigMgr",
        "Adventures with MDT": "MDT",
        "Adventures in SCCM": "SCCM",
    }
    category = category_map.get(blog_name, blog_name)

    body = html_to_markdown(content_html)

    front_matter = f"""---
layout: post
title: "{title.replace('"', '\\"')}"
date: {published.strftime("%Y-%m-%d %H:%M:%S %z")}
author: {author}
categories: ["{category}"]
{tags_yaml}---

{body}
"""

    filepath.write_text(front_matter, encoding="utf-8")
    return filepath


def process_feed(atom_path: Path, blog_name: str) -> int:
    """Parse one feed.atom and write all LIVE posts. Returns post count."""
    tree = ET.parse(atom_path)
    root = tree.getroot()

    count = 0
    for entry in root.findall("atom:entry", NS):
        entry_type = entry.findtext("blogger:type", namespaces=NS)
        entry_status = entry.findtext("blogger:status", namespaces=NS)

        # Only process published posts
        if entry_type != "POST" or entry_status != "LIVE":
            continue

        title_el = entry.find("atom:title", NS)
        title = title_el.text if title_el is not None and title_el.text else "Untitled"

        content_el = entry.find("atom:content", NS)
        content_html = content_el.text if content_el is not None and content_el.text else ""

        if not content_html.strip():
            print(f"  Skipping empty post: {title}")
            continue

        published_str = entry.findtext("atom:published", namespaces=NS) or ""
        published = parse_date(published_str) if published_str else datetime.now(timezone.utc)

        author_el = entry.find("atom:author/atom:name", NS)
        author = author_el.text if author_el is not None and author_el.text else "Matt Atkinson"

        # Collect tags from <category> elements
        tags = []
        for cat in entry.findall("atom:category", NS):
            term = cat.get("term", "")
            if term:
                tags.append(term)

        blogger_filename = entry.findtext("blogger:filename", namespaces=NS) or ""

        try:
            out = write_post(title, published, content_html, tags,
                             blogger_filename, blog_name, author)
            print(f"  OK: {out.name}")
            count += 1
        except Exception as e:
            print(f"  ERROR converting '{title}': {e}")

    return count


def main():
    if not EXPORT_ROOT.exists():
        print(f"ERROR: Export folder not found at {EXPORT_ROOT}")
        print("Make sure the Blogger Takeout is in 'Blogger Export/Takeout/Blogger/Blogs/'")
        return

    total = 0
    for blog_dir in sorted(EXPORT_ROOT.iterdir()):
        if not blog_dir.is_dir():
            continue
        atom_file = blog_dir / "feed.atom"
        if not atom_file.exists():
            continue

        blog_name = blog_dir.name
        print(f"\nProcessing blog: {blog_name}")
        n = process_feed(atom_file, blog_name)
        print(f"  -> {n} posts converted")
        total += n

    print(f"\nDone! {total} posts written to {POSTS_DIR}")
    print("\nNext steps:")
    print("  1. Review the posts in _posts/ and clean up any formatting issues")
    print("  2. Download images referenced in posts and add them to assets/img/posts/")
    print("  3. Commit everything and push to GitHub to trigger a build")


if __name__ == "__main__":
    main()
