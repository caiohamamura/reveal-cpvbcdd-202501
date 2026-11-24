#!/usr/bin/env python3
"""Deterministic PPTX text, hyperlink, speaker-note, and media extractor.

Usage:
    python3 extract_pptx.py path/to/deck.pptx --media-dir ia/images/aulaNN --contact-sheet /tmp/contact.png
"""

from __future__ import annotations

import argparse
import html
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
}


def natnum(name: str) -> int:
    m = re.search(r"(\d+)", name)
    return int(m.group(1)) if m else 0


def parse_rels(z: zipfile.ZipFile, rels_path: str) -> dict[str, dict[str, str]]:
    if rels_path not in z.namelist():
        return {}
    root = ET.fromstring(z.read(rels_path))
    rels: dict[str, dict[str, str]] = {}
    for rel in root:
        rid = rel.attrib.get("Id", "")
        rels[rid] = {
            "target": rel.attrib.get("Target", ""),
            "type": rel.attrib.get("Type", ""),
            "mode": rel.attrib.get("TargetMode", ""),
        }
    return rels


def extract_paragraphs(xml_bytes: bytes) -> list[str]:
    root = ET.fromstring(xml_bytes)
    lines: list[str] = []
    for p in root.findall(".//a:p", NS):
        parts = [t.text for t in p.findall(".//a:t", NS) if t.text]
        text = html.unescape("".join(parts)).strip()
        if text:
            lines.append(text)
    return lines


def extract_slide_info(z: zipfile.ZipFile, slide_path: str) -> dict:
    num = natnum(slide_path)
    xml_bytes = z.read(slide_path)
    xml_text = xml_bytes.decode("utf-8", errors="replace")
    rels = parse_rels(z, f"ppt/slides/_rels/slide{num}.xml.rels")

    paragraphs = extract_paragraphs(xml_bytes)

    used_embeds = set(re.findall(r'r:embed="(rId\d+)"', xml_text))
    images: list[str] = []
    for rid in sorted(used_embeds, key=natnum):
        target = rels.get(rid, {}).get("target", "")
        if target.startswith("../media/"):
            images.append(target.replace("../media/", "", 1))

    used_links = set(re.findall(r'r:id="(rId\d+)"', xml_text))
    links: list[str] = []
    for rid, info in rels.items():
        if info.get("mode") == "External" and info.get("target"):
            if rid in used_links or info["target"].startswith(("http://", "https://")):
                if info["target"] not in links:
                    links.append(info["target"])

    notes: list[str] = []
    for info in rels.values():
        if "notesSlide" in info.get("type", ""):
            notes_path = "ppt/" + info["target"].lstrip("./")
            if notes_path in z.namelist():
                notes = extract_paragraphs(z.read(notes_path))

    return {
        "slide": num,
        "paragraphs": paragraphs,
        "images": images,
        "links": links,
        "notes": notes,
    }


def build_contact_sheet(image_paths: list[Path], output_path: Path, cols: int = 5, thumb_w: int = 260) -> None:
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        print("WARN: Pillow not installed; skipping contact sheet.", file=sys.stderr)
        return

    raster = [p for p in image_paths if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp"}]
    if not raster:
        return

    thumbs: list[tuple[str, Image.Image]] = []
    max_h = 160
    for path in raster:
        try:
            with Image.open(path) as im:
                im.load()
                rgb = im.convert("RGB")
                ratio = thumb_w / max(rgb.width, 1)
                new_h = max(1, min(int(rgb.height * ratio), 220))
                resized = rgb.resize((thumb_w, new_h), Image.Resampling.LANCZOS)
                max_h = max(max_h, new_h)
                thumbs.append((path.name, resized))
        except Exception as exc:
            print(f"WARN: could not thumbnail {path.name}: {exc}", file=sys.stderr)

    if not thumbs:
        return

    rows = (len(thumbs) + cols - 1) // cols
    pad = 12
    label_h = 22
    cell_w = thumb_w + pad
    cell_h = max_h + label_h + pad
    canvas = Image.new("RGB", (cols * cell_w + pad, rows * cell_h + pad), (32, 34, 44))
    draw = ImageDraw.Draw(canvas)

    for idx, (name, im) in enumerate(thumbs):
        r, c = divmod(idx, cols)
        x = pad + c * cell_w
        y = pad + r * cell_h
        draw.text((x + 2, y), name[:34], fill=(255, 220, 100))
        canvas.paste(im, (x, y + label_h))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output_path)
    print(f"Contact sheet saved: {output_path} ({len(thumbs)} images)")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pptx", type=Path, help="Path to .pptx file")
    parser.add_argument("--media-dir", type=Path, help="Optional directory to extract used media files")
    parser.add_argument("--contact-sheet", type=Path, help="Optional output PNG path for labeled thumbnail sheet")
    args = parser.parse_args()

    if not args.pptx.exists():
        print(f"ERROR: file not found: {args.pptx}", file=sys.stderr)
        return 1

    with zipfile.ZipFile(args.pptx) as z:
        slide_paths = sorted(
            [n for n in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n)],
            key=natnum,
        )
        all_used_media: set[str] = set()
        for sp in slide_paths:
            info = extract_slide_info(z, sp)
            print(f"=== SLIDE {info['slide']} ===")
            for line in info["paragraphs"]:
                print(f"  {line}")
            if info["images"]:
                print(f"  [IMAGES]: {', '.join(info['images'])}")
                all_used_media.update(info["images"])
            if info["links"]:
                print(f"  [LINKS]: {', '.join(info['links'])}")
            if info["notes"]:
                print(f"  [NOTES]: {' | '.join(info['notes'])}")

        extracted: list[Path] = []
        if args.media_dir and all_used_media:
            args.media_dir.mkdir(parents=True, exist_ok=True)
            for media_name in sorted(all_used_media, key=natnum):
                zip_member = f"ppt/media/{media_name}"
                if zip_member in z.namelist():
                    dest = args.media_dir / media_name
                    dest.write_bytes(z.read(zip_member))
                    extracted.append(dest)
            print(f"\nExtracted {len(extracted)} used media file(s) to {args.media_dir}")

        if args.contact_sheet and extracted:
            build_contact_sheet(extracted, args.contact_sheet)

    return 0


if __name__ == "__main__":
    sys.exit(main())
