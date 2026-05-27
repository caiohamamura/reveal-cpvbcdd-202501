"""Export Plotly figures as standalone RevealD3 iframe HTML files."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Iterable


PLOTLY_CDN = "https://cdn.plot.ly/plotly-2.32.0.min.js"


def _clean_none(value: Any) -> Any:
    if isinstance(value, dict):
        return {k: _clean_none(v) for k, v in value.items() if v is not None}
    if isinstance(value, list):
        return [_clean_none(v) for v in value]
    return value


def _figure_to_dict(figure: Any) -> dict[str, Any]:
    if hasattr(figure, "to_plotly_json"):
        return _clean_none(figure.to_plotly_json())
    if isinstance(figure, dict):
        return _clean_none(figure)
    raise TypeError(f"Unsupported figure type: {type(figure)!r}")


def _normalize_figures(figures: Any) -> list[dict[str, Any]]:
    if not isinstance(figures, (list, tuple)):
        figures = [figures]
    normalized = [_figure_to_dict(fig) for fig in figures]
    if not normalized:
        raise ValueError("At least one Plotly figure is required")
    return normalized


def _ensure_trace_uids(figures: Iterable[dict[str, Any]]) -> None:
    for fig in figures:
        for index, trace in enumerate(fig.get("data", [])):
            trace.setdefault("uid", f"trace-{index}")


def export_reveald3_plotly(
    figures: Any,
    output: str | Path,
    *,
    title: str = "Plotly figure",
    plotly_cdn: str = PLOTLY_CDN,
    transition_duration: int = 900,
    background: str = "#282a36",
) -> Path:
    """Write one standalone HTML file for RevealD3.

    `figures` can be a single Plotly figure/dict or a list of figure states.
    Each state becomes one RevealD3 transition step.
    """

    output = Path(output)
    states = _normalize_figures(figures)
    _ensure_trace_uids(states)

    payload = json.dumps(states, ensure_ascii=False, separators=(",", ":"))
    title_json = json.dumps(title, ensure_ascii=False)
    cdn_json = json.dumps(plotly_cdn)
    background_json = json.dumps(background)

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">

<head>
  <meta charset="utf-8" />
  <title>{title}</title>
  <script src={cdn_json}></script>
  <style>
    html,
    body,
    #plot {{
      width: 100%;
      height: 100%;
      margin: 0;
      background: {background};
      overflow: hidden;
    }}
  </style>
</head>

<body>
  <div id="plot"></div>

  <script>
    const FIGURE_TITLE = {title_json};
    const STATES = {payload};
    const CONFIG = {{
      displayModeBar: false,
      responsive: true
    }};

    function stateAt(step) {{
      return STATES[Math.max(0, Math.min(step, STATES.length - 1))];
    }}

    function renderStep(step) {{
      const state = stateAt(step);
      return Plotly.react('plot', state.data || [], state.layout || {{}}, CONFIG);
    }}

    function animateStep(step) {{
      const state = stateAt(step);
      return Plotly.animate('plot', {{
        data: state.data || [],
        traces: (state.data || []).map((_, index) => index),
        layout: state.layout || {{}}
      }}, {{
        transition: {{
          duration: {transition_duration},
          easing: 'cubic-in-out'
        }},
        frame: {{
          duration: {transition_duration},
          redraw: true
        }},
        mode: 'immediate'
      }});
    }}

    renderStep(0);

    var _transitions = STATES.slice(1).map((_, index) => ({{
      index: index,
      transitionForward: () => animateStep(index + 1),
      transitionBackward: () => animateStep(index)
    }}));
  </script>
</body>
</html>
"""

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html, encoding="utf-8", newline="\n")
    return output


def _load_json(path: Path) -> Any:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict) and "frames" in data and "data" in data:
        return data
    return data


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="JSON file with one figure dict or a list of figure dicts")
    parser.add_argument("--output", "-o", type=Path, required=True, help="Output standalone HTML file")
    parser.add_argument("--title", default="Plotly figure", help="HTML title")
    parser.add_argument("--transition-duration", type=int, default=900, help="Transition duration in milliseconds")
    parser.add_argument("--background", default="#282a36", help="Page background color")
    args = parser.parse_args()

    export_reveald3_plotly(
        _load_json(args.input),
        args.output,
        title=args.title,
        transition_duration=args.transition_duration,
        background=args.background,
    )
    print(args.output)


if __name__ == "__main__":
    main()
