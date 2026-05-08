#!/usr/bin/env python3
"""
Deterministic image extractor for educational slide images.

Usage:
    # From search result URLs (one per line via stdin)
    echo "https://randomnerdtutorials.com/esp32-lora/" | python extract_images.py

    # Or pass URLs as arguments
    python extract_images.py https://randomnerdtutorials.com/esp32-lora/

Output: JSON array of validated images with score, url, alt, source, content_type, size_bytes.

Requires: pip install requests beautifulsoup4
"""

import json
import re
import sys
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
}

# --- filter patterns ---
REJECT_URL_PATTERNS = [
    r"/logo[^a-z]", r"logo-", r"-logo", r"_logo", r"logotipo",
    r"icon-", r"-icon", r"_icon", r"/icons/",
    r"avatar", r"gravatar",
    r"social", r"share", r"button", r"banner",
    r"/ad[s]?/", r"-ad-", r"tracking", r"pixel",
    r"spacer", r"loading", r"placeholder",
    r"woocommerce", r"wp-smiley", r"emoji",
    r"blank\.gif", r"blank\.png",
    r"rating-state", r"ajax-loader",
    # SVG UI elements
    r"chevron", r"arrow-", r"menu-", r"close-", r"hamburger",
]

BONUS_URL_PATTERNS = [
    (r"circuit", 30), (r"diagram", 30), (r"wiring", 30),
    (r"schematic", 30), (r"breadboard", 30), (r"project", 30),
    (r"pinout", 30), (r"connection", 20), (r"assembly", 20),
]


def safe_dim(val):
    try:
        return int(float(re.sub(r"[^\d.]", "", str(val))))
    except (ValueError, TypeError):
        return 0


def reject_url(url: str) -> bool:
    url_lower = url.lower()
    for pat in REJECT_URL_PATTERNS:
        if re.search(pat, url_lower):
            return True
    return False


def collect_candidates(soup: BeautifulSoup, base_url: str) -> list[dict]:
    """Collect image candidates in priority order, returning list of {url, alt, source_type}."""
    seen: set[str] = set()
    candidates: list[dict] = []

    def _add(url_str: str, alt: str, source_type: str):
        if not url_str or url_str.startswith("data:"):
            return
        full_url = urllib.parse.urljoin(base_url, url_str)
        full_url = full_url.split("?")[0]  # strip query params for dedup
        if full_url.lower() in seen:
            return
        seen.add(full_url.lower())
        if reject_url(full_url):
            return
        candidates.append({"url": full_url, "alt": alt, "source_type": source_type})

    # Priority 1: og:image
    og = soup.find("meta", property="og:image")
    if og and og.get("content"):
        _add(og["content"], soup.find("meta", property="og:title", content=True).get("content", "") if soup.find("meta", property="og:title", content=True) else "", "og:image")

    # Priority 2: twitter:image
    tw = soup.find("meta", attrs={"name": "twitter:image"})
    if tw and tw.get("content"):
        _add(tw["content"], "", "twitter:image")

    # Priority 3: link preload as=image
    for link in soup.find_all("link", rel=lambda v: v and "preload" in v):
        if link.get("as") == "image" and link.get("href"):
            _add(link["href"], "", "preload")

    # Priority 4: <img> inside <article> or <main>
    for container in soup.find_all(["article", "main"]) or []:
        for img in container.find_all("img", src=True):
            alt = img.get("alt", "").strip()
            w = safe_dim(img.get("width"))
            h = safe_dim(img.get("height"))
            if w and w <= 80 or h and h <= 80:
                continue
            _add(img["src"], alt, "article")

    # Priority 5: <img> inside content divs
    for cls in ["content", "entry-content", "post-content", "article-content", "page-content"]:
        div = soup.find("div", class_=cls) or soup.find("div", id=cls)
        if div:
            for img in div.find_all("img", src=True):
                alt = img.get("alt", "").strip()
                w = safe_dim(img.get("width"))
                h = safe_dim(img.get("height"))
                if w and w <= 80 or h and h <= 80:
                    continue
                _add(img["src"], alt, "content-div")

    # Priority 6: remaining <img> in body
    body = soup.find("body")
    if body:
        for img in body.find_all("img", src=True):
            alt = img.get("alt", "").strip()
            w = safe_dim(img.get("width"))
            h = safe_dim(img.get("height"))
            if w and w <= 80 or h and h <= 80:
                continue
            _add(img["src"], alt, "body")

    return candidates


def validate_image(img_entry: dict) -> dict | None:
    """HEAD request to check status, mimetype, size. Returns enriched entry or None."""
    url = img_entry["url"]
    try:
        resp = requests.head(url, headers=HEADERS, timeout=10, allow_redirects=True)
    except requests.RequestException:
        return None

    if resp.status_code != 200:
        return None

    content_type = resp.headers.get("Content-Type", "")
    content_length = resp.headers.get("Content-Length")
    if not content_type or not content_length:
        try:
            resp2 = requests.get(url, headers=HEADERS, timeout=10, stream=True)
            if resp2.status_code != 200:
                return None
            ct = resp2.headers.get("Content-Type", "")
            if not ct.startswith("image/"):
                return None
            content_type = ct
            size = 0
            for chunk in resp2.iter_content(chunk_size=8192):
                size += len(chunk)
                if size >= 1024:
                    break
            resp2.close()
            if size < 1024:
                return None
            content_length = str(size)
        except requests.RequestException:
            return None
    else:
        cl = int(content_length)
        if cl < 1024:
            return None

    img_entry["content_type"] = content_type
    img_entry["size_bytes"] = int(content_length) if content_length else None
    return img_entry


def score_image(img_entry: dict) -> int:
    score = 0
    url = img_entry["url"].lower()
    st = img_entry["source_type"]

    if st in ("og:image", "twitter:image"):
        score += 100
    elif st in ("article", "content-div"):
        score += 50

    for pat, pts in BONUS_URL_PATTERNS:
        if re.search(pat, url):
            score += pts

    if url.endswith(".png"):
        score += 5

    return score


def extract_from_page(page_url: str) -> list[dict]:
    """Fetch page, extract and validate images, return sorted list."""
    try:
        resp = requests.get(page_url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"[SKIP] {page_url}: {e}", file=sys.stderr)
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    candidates = collect_candidates(soup, page_url)

    results: list[dict] = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(validate_image, c): c for c in candidates}
        for future in as_completed(futures):
            result = future.result()
            if result:
                result["score"] = score_image(result)
                result["source_page"] = page_url
                # Extract domain for attribution
                parsed = urllib.parse.urlparse(page_url)
                result["source_domain"] = parsed.netloc.replace("www.", "")
                # Keep only needed fields, drop source_type
                results.append({
                    "url": result["url"],
                    "alt": result["alt"],
                    "content_type": result["content_type"],
                    "size_bytes": result["size_bytes"],
                    "score": result["score"],
                    "source_page": result["source_page"],
                    "source_domain": result["source_domain"],
                })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:5]  # top 5


def main():
    urls: list[str] = []
    if len(sys.argv) > 1:
        urls = sys.argv[1:]
    else:
        urls = [line.strip() for line in sys.stdin if line.strip()]

    if not urls:
        print("Usage: extract_images.py URL [URL...]", file=sys.stderr)
        sys.exit(1)

    all_results: list[dict] = []
    seen_urls: set[str] = set()

    for page_url in urls:
        images = extract_from_page(page_url)
        for img in images:
            if img["url"].lower() not in seen_urls:
                seen_urls.add(img["url"].lower())
                all_results.append(img)

    # Sort by score across all pages
    all_results.sort(key=lambda x: x["score"], reverse=True)

    json.dump(all_results[:10], sys.stdout, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
