import feedparser
from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, ElementTree

# 1. BloggerのフィードURL
feed_url = "https://flashsoudannavi.blogspot.com/feeds/posts/default"

# 2. フィードの読み込み
feed = feedparser.parse(feed_url)

# 3. XMLのルート作成
urlset = Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

# 4. 各エントリをXMLに追加
for entry in feed.entries:
    url = SubElement(urlset, "url")
    loc = SubElement(url, "loc")
    loc.text = entry.link

    lastmod = SubElement(url, "lastmod")
    # 更新日時をISO形式に変換
    updated = entry.updated_parsed
    lastmod.text = datetime(*updated[:6]).strftime("%Y-%m-%d")

# 5. ファイルとして保存
tree = ElementTree(urlset)
tree.write("sitemap.xml", encoding="utf-8", xml_declaration=True)
