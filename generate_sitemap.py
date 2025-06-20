import feedparser
from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, ElementTree

# BloggerのフィードURL（100件まで）
feed_url = "https://flashsoudannavi.blogspot.com/feeds/posts/default?max-results=100"
feed = feedparser.parse(feed_url)

urlset = Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

for entry in feed.entries:
    url = SubElement(urlset, "url")

    loc = SubElement(url, "loc")
    loc.text = entry.link

    lastmod = SubElement(url, "lastmod")
    updated = getattr(entry, "updated_parsed", getattr(entry, "published_parsed", None))
    if updated:
        lastmod.text = datetime(*updated[:6]).strftime("%Y-%m-%d")

tree = ElementTree(urlset)
tree.write("sitemap.xml", encoding="utf-8", xml_declaration=True)
