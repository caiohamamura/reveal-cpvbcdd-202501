# TOOLS.md - Environment-Specific Notes

_(Environment and toolchain notes for this repository go here.)_

## Python Environment

- **Environment name:** `opencode` (managed via micromamba)
- **Key packages:** python=3.11, jupyter, nbconvert, numpy, pandas, plotly, scipy, scikit-learn

## Local Development

- Serve slides locally: `python3 -m http.server 8000`
- Validate HTML: see `AGENTS.md` → Course Development Commands

## Build / Deploy

- GitHub Pages deployment is configured in `.github/workflows/static.yml`
- No build step required for Reveal.js slides (static HTML)
