# ConfigMatt Blog

Personal blog at [configmatt.com](https://configmatt.com), powered by [Jekyll](https://jekyllrb.com) with the [Chirpy](https://github.com/cotes2020/jekyll-theme-chirpy) theme, hosted on GitHub Pages.

## Local development (optional)

1. Install [Ruby 3.3+](https://rubyinstaller.org/) (Windows) or via `rbenv`/`rvm` (Mac/Linux)
2. `gem install bundler`
3. `bundle install`
4. `bundle exec jekyll serve --livereload`
5. Open `http://localhost:4000`

## Adding posts

Drop a file named `YYYY-MM-DD-your-post-title.md` in `_posts/` with this front matter:

```yaml
---
layout: post
title: "Your Post Title"
date: 2026-01-01 12:00:00 -0600
categories: [ConfigMgr]
tags: ["SCCM", "PowerShell"]
---
Your content here.
```

## Blogger import

```
pip install html2text beautifulsoup4 lxml
python scripts/convert_blogger.py
```
