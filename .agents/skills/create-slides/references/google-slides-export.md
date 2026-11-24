# Exporting & Inspecting Google Slides

Use this reference when a user shares a Google Slides URL (`https://docs.google.com/presentation/d/<PRESENTATION_ID>/edit...`) as a style reference or conversion source.

## Path 1: Public / Link-Shared Decks (Fastest, No Auth Needed)

Export both PDF (for exact visual layout inspection) and PPTX (for text, links, and raw embedded media):

```bash
ID="<PRESENTATION_ID>"
curl -sL "https://docs.google.com/presentation/d/${ID}/export/pdf"  -o /tmp/slides.pdf
curl -sL "https://docs.google.com/presentation/d/${ID}/export/pptx" -o /tmp/slides.pptx

# Render every slide to PNG so you can visually study layout, overlays, and typography
mkdir -p /tmp/slide_pages
pdftoppm -png -r 120 /tmp/slides.pdf /tmp/slide_pages/slide
```

Then run `.agents/skills/convert-pptx/scripts/extract_pptx.py /tmp/slides.pptx` to extract structured text, hyperlinks, and media assets.

> Never commit downloaded source `.pdf` or `.pptx` exports or temp folders — commit only selected, renamed, optimized assets under `<course>/images/<lesson>/`.

## Path 2: Private Google Drive Decks (`gogcli`)

If the public export redirects to Google sign-in, use `gog` (installed via Linuxbrew at `/home/linuxbrew/.linuxbrew/opt/gogcli/bin/gog`):

```bash
GOG_KEYRING_PASSWORD=x /home/linuxbrew/.linuxbrew/opt/gogcli/bin/gog <command>
```

Useful commands:
```bash
# Export presentation by ID
GOG_KEYRING_PASSWORD=x gog slides export <presentationId> --format pptx
GOG_KEYRING_PASSWORD=x gog slides export <presentationId> --format pdf

# Navigate Drive folders (folder names are case-sensitive; do not pass --query to gog search)
GOG_KEYRING_PASSWORD=x gog search "foldername" -a <email> -j
GOG_KEYRING_PASSWORD=x gog ls -a <email> -j --parent <folder-id> --max 100
```

Gotchas:
- Binary is `gog`, not `gogcli`; Homebrew prefix is `/home/linuxbrew/.linuxbrew/`.
- If `gog slides list-slides/read-slide` returns `403 accessNotConfigured`, fall back to `gog slides export --format pptx/pdf` or enable Google Slides API for the OAuth project.
- If keyring reports `"integrity check failed"`, re-authenticate with `gog auth add <email> --remote --step 1 --services drive` followed by `--step 2 --auth-url '<redirect-url>'`.
