import feedparser
from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, ElementTree

# 1. フィードURL（最大500件取得）
feed_url = "https://flashsoudannavi.blogspot.com/feeds/posts/default?max-results=500"

# 2. フィードの読み込み
feed = feedparser.parse(feed_url)

# 3. XMLのルート要素を作成
urlset = Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

# 4. 各記事エントリをループしてsitemapに追加
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

# 5. ファイルとして出力
tree = ElementTree(urlset)
tree.write("sitemap.xml", encoding="utf-8", xml_declaration=True)
