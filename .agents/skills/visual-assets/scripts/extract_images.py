#!/usr/bin/env python3
"""Deterministic image extractor and validator for educational slide assets.

Usage:
    python3 extract_images.py https://example.com/article [URL2 ...]
    echo "https://example.com/article" | python3 extract_images.py

Output: JSON array of validated images (HTTP 200, image/* MIME, >=1KB) ranked by relevance.
"""

from __future__ import annotations

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
    r"chevron", r"arrow-", r"menu-", r"close-", r"hamburger",
]

BONUS_URL_PATTERNS = [
    (r"architecture", 35), (r"diagram", 30), (r"figure", 30), (r"fig\d", 30),
    (r"pipeline", 25), (r"model", 20), (r"network", 20), (r"latent", 20),
    (r"circuit", 30), (r"wiring", 30), (r"schematic", 30),
    (r"breadboard", 30), (r"pinout", 30), (r"project", 20),
    (r"connection", 15), (r"assembly", 15),
]


def safe_dim(val) -> int:
    try:
        return int(float(re.sub(r"[^\d.]", "", str(val))))
    except (ValueError, TypeError):
        return 0


def reject_url(url: str) -> bool:
    url_lower = url.lower()
    return any(re.search(pat, url_lower) for pat in REJECT_URL_PATTERNS)


def collect_candidates(soup: BeautifulSoup, base_url: str) -> list[dict]:
    seen: set[str] = set()
    candidates: list[dict] = []

    def _add(url_str: str, alt: str, source_type: str) -> None:
        if not url_str or url_str.startswith("data:"):
            return
        full_url = urllib.parse.urljoin(base_url, url_str).split("?")[0]
        if full_url.lower() in seen or reject_url(full_url):
            return
        seen.add(full_url.lower())
        candidates.append({"url": full_url, "alt": alt, "source_type": source_type})

    og = soup.find("meta", property="og:image")
    if og and og.get("content"):
        og_title = soup.find("meta", property="og:title", content=True)
        _add(og["content"], og_title.get("content", "") if og_title else "", "og:image")

    tw = soup.find("meta", attrs={"name": "twitter:image"})
    if tw and tw.get("content"):
        _add(tw["content"], "", "twitter:image")

    for link in soup.find_all("link", rel=lambda v: v and "preload" in v):
        if link.get("as") == "image" and link.get("href"):
            _add(link["href"], "", "preload")

    def _collect_from(node, source_type: str) -> None:
        for img in node.find_all("img", src=True):
            w, h = safe_dim(img.get("width")), safe_dim(img.get("height"))
            if (w and w <= 80) or (h and h <= 80):
                continue
            _add(img["src"], img.get("alt", "").strip(), source_type)

    for container in soup.find_all(["article", "main", "figure"]) or []:
        _collect_from(container, "article")

    for cls in ["content", "entry-content", "post-content", "article-content", "page-content"]:
        div = soup.find("div", class_=cls) or soup.find("div", id=cls)
        if div:
            _collect_from(div, "content-div")

    body = soup.find("body")
    if body:
        _collect_from(body, "body")

    return candidates


def validate_image(img_entry: dict) -> dict | None:
    url = img_entry["url"]
    try:
        resp = requests.head(url, headers=HEADERS, timeout=10, allow_redirects=True)
    except requests.RequestException:
        return None

    if resp.status_code != 200:
        return None

    content_type = resp.headers.get("Content-Type", "")
    content_length = resp.headers.get("Content-Length")
    if not content_type.startswith("image/") or not content_length:
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
    elif int(content_length) < 1024:
        return None

    img_entry["content_type"] = content_type
    img_entry["size_bytes"] = int(content_length)
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

    if url.endswith((".png", ".svg")):
        score += 5
    return score


def extract_from_page(page_url: str) -> list[dict]:
    try:
        resp = requests.get(page_url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
    except requests.RequestException as exc:
        print(f"[SKIP] {page_url}: {exc}", file=sys.stderr)
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    candidates = collect_candidates(soup, page_url)

    results: list[dict] = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(validate_image, c): c for c in candidates}
        for future in as_completed(futures):
            result = future.result()
            if result:
                parsed = urllib.parse.urlparse(page_url)
                results.append({
                    "url": result["url"],
                    "alt": result["alt"],
                    "content_type": result["content_type"],
                    "size_bytes": result["size_bytes"],
                    "score": score_image(result),
                    "source_page": page_url,
                    "source_domain": parsed.netloc.replace("www.", ""),
                })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:5]


def main() -> int:
    urls = sys.argv[1:] if len(sys.argv) > 1 else [line.strip() for line in sys.stdin if line.strip()]
    if not urls:
        print("Usage: extract_images.py URL [URL...]", file=sys.stderr)
        return 1

    all_results: list[dict] = []
    seen_urls: set[str] = set()
    for page_url in urls:
        for img in extract_from_page(page_url):
            if img["url"].lower() not in seen_urls:
                seen_urls.add(img["url"].lower())
                all_results.append(img)

    all_results.sort(key=lambda x: x["score"], reverse=True)
    json.dump(all_results[:10], sys.stdout, indent=2, ensure_ascii=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
