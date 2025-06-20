name: Update Blogger Sitemap

on:
  schedule:
    - cron: '0 3 * * *'  # 毎日03:00 JST（日本時間）に実行
  workflow_dispatch:      # 手動実行も可能

jobs:
  update-sitemap:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'

      - name: Install dependencies
        run: pip install feedparser

      - name: Run sitemap generator
        run: |
          python <<EOF
          import feedparser
          from datetime import datetime
          from xml.etree.ElementTree import Element, SubElement, ElementTree

          feed_url = "https://flashsoudannavi.blogspot.com/feeds/posts/default?max-results=100"
          feed = feedparser.parse(feed_url)

          urlset = Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
          for entry in feed.entries:
              url = SubElement(urlset, "url")
              loc = SubElement(url, "loc")
              loc.text = entry.link
              lastmod = SubElement(url, "lastmod")
              if hasattr(entry, "updated_parsed"):
                  updated = entry.updated_parsed
              elif hasattr(entry, "published_parsed"):
                  updated = entry.published_parsed
              else:
                  updated = None
              if updated:
                  lastmod.text = datetime(*updated[:6]).strftime("%Y-%m-%d")

          tree = ElementTree(urlset)
          tree.write("sitemap.xml", encoding="utf-8", xml_declaration=True)
          EOF

      - name: Commit and push sitemap.xml
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git pull origin main --rebase
          git add sitemap.xml
          git commit -m "Update sitemap.xml [auto]" || echo "No changes to commit"
          git push origin main
