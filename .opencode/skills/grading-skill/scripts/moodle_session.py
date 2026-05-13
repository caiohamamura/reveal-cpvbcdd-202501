"""Shared Moodle session helper. Reads MOODLE_TOKEN from .env file."""
import os
import requests
from pathlib import Path

def _find_env():
    """Walk up from current dir to find .env file."""
    d = Path.cwd()
    while d != d.parent:
        env_file = d / ".env"
        if env_file.exists():
            return env_file
        d = d.parent
    return None

def _load_env():
    env_file = _find_env()
    if not env_file:
        return
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, val = line.partition("=")
                if key not in os.environ:
                    os.environ[key] = val

_load_env()

BASE = os.environ.get("MOODLE_BASE", "https://ead.cpv.ifsp.edu.br")
TOKEN = os.environ.get("MOODLE_TOKEN", "")

if not TOKEN:
    import sys
    print("ERROR: MOODLE_TOKEN not set in .env file", file=sys.stderr)

def get_session():
    """Return a requests.Session with Moodle auth cookie."""
    s = requests.Session()
    s.headers.update({
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/142.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "pt-BR,pt;q=0.5",
    })
    s.cookies.set("MoodleSession", TOKEN, domain="ead.cpv.ifsp.edu.br")
    return s
