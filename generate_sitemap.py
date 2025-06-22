import requests
import xml.etree.ElementTree as ET
from datetime import datetime

FEED_URL = "https://flashsoudannavi.blogspot.com/feeds/posts/default?alt=json&max-results=100"

response = requests.get(FEED_URL)
response.raise_for_status()
data = response.json()

urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

entries = data.get("feed", {}).get("entry", [])

for entry in entries:
    url = ET.SubElement(urlset, "url")

    loc = ET.SubElement(url, "loc")
    loc.text = entry["link"][0]["href"]

    lastmod = ET.SubElement(url, "lastmod")
    updated = entry.get("updated", {}).get("$t") or entry.get("published", {}).get("$t")
    if updated:
        lastmod.text = updated[:10]  # YYYY-MM-DD

tree = ET.ElementTree(urlset)
tree.write("sitemap.xml", encoding="utf-8", xml_declaration=True)
