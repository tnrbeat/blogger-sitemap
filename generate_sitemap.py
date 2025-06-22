for entry in entries:
    url = ET.SubElement(urlset, "url")

    loc = ET.SubElement(url, "loc")
    # 'alternate' のリンクを探す
    article_url = None
    for link in entry["link"]:
        if link.get("rel") == "alternate":
            article_url = link.get("href")
            break
    loc.text = article_url if article_url else entry["link"][0]["href"]

    lastmod = ET.SubElement(url, "lastmod")
    updated = entry.get("updated", {}).get("$t") or entry.get("published", {}).get("$t")
    if updated:
        lastmod.text = updated[:10]  # YYYY-MM-DD
