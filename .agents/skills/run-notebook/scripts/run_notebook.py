#!/usr/bin/env python3
"""Execute a Jupyter notebook, verify cell outputs, and extract embedded PNG images.

Usage:
    python3 run_notebook.py notebook.ipynb --output-dir images/
    python3 run_notebook.py notebook.ipynb --extract-only --output-dir images/
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path


def execute_notebook(notebook_path: str, timeout: int = 300) -> tuple[bool, str]:
    """Execute the notebook via nbconvert. Returns (success, error_message)."""
    output_path = Path(tempfile.mkdtemp()) / "executed.ipynb"
    cmd = [
        sys.executable, "-m", "jupyter", "nbconvert",
        "--execute",
        "--to", "notebook",
        "--output", str(output_path),
        "--ExecutePreprocessor.timeout", str(timeout),
        "--ExecutePreprocessor.allow_errors", "True",
        notebook_path,
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 60)
        if result.returncode != 0:
            return False, f"nbconvert failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

        with open(output_path, encoding="utf-8") as f:
            nb = json.load(f)

        errors = []
        for i, cell in enumerate(nb.get("cells", [])):
            for output in cell.get("outputs", []):
                if output.get("output_type") == "error":
                    ename = output.get("ename", "Error")
                    evalue = output.get("evalue", "")
                    traceback = "".join(output.get("traceback", []))
                    errors.append(f"Cell [{i}]: {ename}: {evalue}\n{traceback}")

        if errors:
            return False, "\n\n".join(errors)
        return True, ""
    except subprocess.TimeoutExpired:
        return False, f"Notebook execution timed out after {timeout}s"
    finally:
        if output_path.exists():
            output_path.unlink()
        if output_path.parent.exists():
            try:
                output_path.parent.rmdir()
            except OSError:
                pass


def generate_image_name(source: str, text_output: str, cell_idx: int, output_idx: int) -> str:
    patterns = [
        r"sns\.(\w+)plot.*(?:x|y)=['\"](.*?)['\"]",
        r"sns\.(\w+)",
        r"plt\.(\w+)",
        r"radarboxplot",
    ]
    combined = source + text_output
    for pattern in patterns:
        m = re.search(pattern, combined, re.IGNORECASE)
        if m:
            name = m.group(0).replace("sns.", "").replace("plt.", "").replace("(", "").replace(")", "")
            name = re.sub(r"[^\w\-]", "_", name)[:60]
            return f"{name}_c{cell_idx}_{output_idx}"
    return f"cell_{cell_idx}_output_{output_idx}"


def extract_images(notebook_path: str, output_dir: str) -> list[dict]:
    with open(notebook_path, encoding="utf-8") as f:
        nb = json.load(f)

    images = []
    for i, cell in enumerate(nb.get("cells", [])):
        for j, output in enumerate(cell.get("outputs", [])):
            data = output.get("data", {})
            if "image/png" in data:
                png_data = base64.b64decode(data["image/png"])
                text_output = ""
                for prev in cell.get("outputs", [])[:j]:
                    if prev.get("output_type") == "execute_result":
                        text_output = "".join(prev.get("data", {}).get("text/plain", ""))
                cell_source = "".join(cell.get("source", ""))[:200]
                filename = f"{generate_image_name(cell_source, text_output, i, j)}.png"
                filepath = os.path.join(output_dir, filename)

                os.makedirs(output_dir, exist_ok=True)
                with open(filepath, "wb") as f_out:
                    f_out.write(png_data)

                images.append({
                    "filename": filename,
                    "filepath": filepath,
                    "size_bytes": os.path.getsize(filepath),
                    "cell_index": i,
                    "output_index": j,
                    "source_snippet": cell_source[:100],
                })
    return images


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("notebook", help="Path to the .ipynb file")
    parser.add_argument("--output-dir", default="images", help="Directory for extracted images")
    parser.add_argument("--timeout", type=int, default=300, help="Execution timeout in seconds")
    parser.add_argument("--extract-only", action="store_true", help="Only extract images, skip execution")
    parser.add_argument("--exec-only", action="store_true", help="Only execute, skip image extraction")
    args = parser.parse_args()

    if not os.path.exists(args.notebook):
        print(f"Error: Notebook not found: {args.notebook}", file=sys.stderr)
        return 1

    if not args.extract_only:
        print(f"Executing notebook: {args.notebook}")
        success, error = execute_notebook(args.notebook, args.timeout)
        if not success:
            print(f"ERROR: Notebook execution failed:\n{error}", file=sys.stderr)
            return 1
        print("Notebook executed successfully.")

    if not args.exec_only:
        print(f"Extracting images to: {args.output_dir}")
        images = extract_images(args.notebook, args.output_dir)
        if not images:
            print("No images found in notebook outputs.")
        else:
            print(f"\nExtracted {len(images)} image(s):")
            for img in images:
                status = "OK" if img["size_bytes"] > 1024 else "WARN: small file (<1KB)"
                print(f"  {img['filename']} ({img['size_bytes']} bytes) [{status}]")
            json_path = os.path.join(args.output_dir, "images_manifest.json")
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(images, f, indent=2, ensure_ascii=False)
            print(f"\nImage manifest written to: {json_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
