import urllib.request
import re
import os

def get_wikimedia_svg(commons_url):
    try:
        req = urllib.request.Request(commons_url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req).read().decode('utf-8')
        match = re.search(r'href="(https://upload\.wikimedia\.org/wikipedia/commons/[^"]+\.svg)"', html)
        if match:
            return match.group(1)
        match = re.search(r'href="(https://upload\.wikimedia\.org/wikipedia/commons/thumb/[^"]+\.png)"', html)
        if match:
            return match.group(1)
    except Exception as e:
        print(f'Failed {commons_url}: {e}')
    return None

urls = {
    'postgres': 'https://commons.wikimedia.org/wiki/File:Postgresql_elephant.svg',
    'hive': 'https://commons.wikimedia.org/wiki/File:Apache_Hive_logo.svg',
    'parquet': 'https://commons.wikimedia.org/wiki/File:Apache_Parquet_logo.svg'
}

os.makedirs('img', exist_ok=True)

for name, url in urls.items():
    svg_url = get_wikimedia_svg(url)
    print(f'{name}: {svg_url}')
    if svg_url:
        try:
            req = urllib.request.Request(svg_url, headers={'User-Agent': 'Mozilla/5.0'})
            data = urllib.request.urlopen(req).read()
            ext = 'png' if svg_url.endswith('.png') else 'svg'
            with open(f'img/{name}_logo.{ext}', 'wb') as f:
                f.write(data)
            print(f'Saved img/{name}_logo.{ext}')
        except Exception as e:
            print(f'Failed to download {svg_url}: {e}')

