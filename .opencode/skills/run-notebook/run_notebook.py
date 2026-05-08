#!/usr/bin/env python3
"""
Execute a Jupyter notebook, verify cell outputs, and extract images.

Usage:
    python3 run_notebook.py notebook.ipynb --output-dir images/

Requires: pip install jupyter nbconvert nbformat
"""

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
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout + 60,
        )
        if result.returncode != 0:
            return False, f"nbconvert failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

        # Check for errors in cell outputs
        with open(output_path) as f:
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
        # Cleanup temp file
        if output_path.exists():
            output_path.unlink()
        if output_path.parent.exists():
            try:
                output_path.parent.rmdir()
            except OSError:
                pass


def extract_images(notebook_path: str, output_dir: str) -> list[dict]:
    """Extract PNG images from notebook outputs. Returns list of info dicts."""
    with open(notebook_path) as f:
        nb = json.load(f)

    images = []
    for i, cell in enumerate(nb.get("cells", [])):
        for j, output in enumerate(cell.get("outputs", [])):
            data = output.get("data", {})
            if "image/png" in data:
                png_data = base64.b64decode(data["image/png"])
                # Try to find a reasonable name from the output or cell metadata
                text_output = ""
                for prev_output in cell.get("outputs", [])[:j]:
                    if prev_output.get("output_type") == "execute_result":
                        # Use the plain text summary as a hint
                        text_output = "".join(prev_output.get("data", {}).get("text/plain", ""))
                cell_source = "".join(cell.get("source", ""))[:200]

                # Generate a descriptive filename
                name = generate_image_name(cell_source, text_output, i, j)
                filename = f"{name}.png"
                filepath = os.path.join(output_dir, filename)

                os.makedirs(output_dir, exist_ok=True)
                with open(filepath, "wb") as f_out:
                    f_out.write(png_data)

                file_size = os.path.getsize(filepath)
                images.append({
                    "filename": filename,
                    "filepath": filepath,
                    "size_bytes": file_size,
                    "cell_index": i,
                    "output_index": j,
                    "source_snippet": cell_source[:100],
                })

    return images


def generate_image_name(source: str, text_output: str, cell_idx: int, output_idx: int) -> str:
    """Generate a descriptive filename from cell content."""
    # Look for common plot patterns in source code
    patterns = [
        (r"sns\.(\w+)plot.*(?:x|y)=['\"](.*?)['\"]", r"\2-\1"),
        (r"sns\.(\w+)", r"\1"),
        (r"plt\.(\w+)", r"\1"),
        (r"radarboxplot", "radar"),
    ]
    combined = source + text_output
    for pattern, replacement in patterns:
        m = re.search(pattern, combined, re.IGNORECASE)
        if m:
            name = m.group(0).replace("sns.", "").replace("plt.", "").replace("(", "").replace(")", "")
            name = re.sub(r"[^\w\-]", "_", name)[:60]
            return name

    return f"cell_{cell_idx}_output_{output_idx}"


def main():
    parser = argparse.ArgumentParser(description="Execute Jupyter notebook and extract images")
    parser.add_argument("notebook", help="Path to the .ipynb file")
    parser.add_argument("--output-dir", default="images", help="Directory for extracted images")
    parser.add_argument("--timeout", type=int, default=300, help="Execution timeout in seconds")
    parser.add_argument("--extract-only", action="store_true", help="Only extract images, skip execution")
    parser.add_argument("--exec-only", action="store_true", help="Only execute, skip image extraction")

    args = parser.parse_args()

    if not os.path.exists(args.notebook):
        print(f"Error: Notebook not found: {args.notebook}", file=sys.stderr)
        sys.exit(1)

    if not args.extract_only and not args.exec_only:
        print(f"Executing notebook: {args.notebook}")
        success, error = execute_notebook(args.notebook, args.timeout)
        if not success:
            print(f"ERROR: Notebook execution failed:\n{error}", file=sys.stderr)
            sys.exit(1)
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
                print(f"    Source: cell[{img['cell_index']}], {img['source_snippet']}...")

        # Output JSON for programmatic use
        json_output = json.dumps(images, indent=2, ensure_ascii=False)
        json_path = os.path.join(args.output_dir, "images_manifest.json")
        with open(json_path, "w") as f:
            f.write(json_output)
        print(f"\nImage manifest written to: {json_path}")


if __name__ == "__main__":
    main()
