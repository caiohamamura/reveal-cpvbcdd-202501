#!/usr/bin/env python3
"""
Moodle client via scraping HTTP.
Uso: python moodle_client.py <endpoint> [course_id]
"""
import sys
import requests
from bs4 import BeautifulSoup

BASE = "https://ead.cpv.ifsp.edu.br"
COOKIE = "57p6nf782p1epirj7nv0ahgpip"

def get_session():
    s = requests.Session()
    s.headers.update({
        "User-Agent": "Mozilla/5.0 (compatible; MoodleBot/1.0)",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    })
    s.cookies.set("MoodleSession", COOKIE, domain="ead.cpv.ifsp.edu.br")
    return s

def fetch(path):
    s = get_session()
    r = s.get(f"{BASE}{path}")
    if r.status_code != 200:
        print(f"Erro HTTP {r.status_code}: {r.url}")
        return None
    if "login" in r.url.lower():
        print("AVISO: Sessão expirou ou não logou - redirecionado para login")
    return BeautifulSoup(r.text, "html.parser")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python moodle_client.py <path>")
        print("Exemplo: python moodle_client.py /my/")
        sys.exit(1)

    path = sys.argv[1]
    soup = fetch(path)
    if soup:
        print(f"=== {path} ===")
        print(soup.title.string if soup.title else "Sem título")
        # Para debug: mostrar primeiros links
        for a in soup.select('a')[:10]:
            href = a.get('href', '')
            text = a.get_text(strip=True)[:50]
            if href:
                print(f"  {text} -> {href}")
