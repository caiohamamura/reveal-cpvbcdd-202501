#!/usr/bin/env python3
"""Deterministic static validation for Reveal.js slide HTML files."""

from __future__ import annotations

import argparse
import glob
import re
import sys
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


CHINESE_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
LOCAL_REF_RE = re.compile(r"""(?:href|src)\s*=\s*["']([^"':#][^"']*)["']""", re.IGNORECASE)
CODE_BLOCK_SCRIPT_RE = re.compile(
    r"<code-block\b[^>]*>(?:(?!</code-block>).)*<script\b",
    re.IGNORECASE | re.DOTALL,
)
PHASE_START_RE = re.compile(r"Etapa\s+(\d+)\s*:", re.IGNORECASE)
PHASE_END_RE = re.compile(r"fim\s+Etapa\s+(\d+)", re.IGNORECASE)
REMOTE_SCHEMES = {"http", "https", "mailto", "tel", "data", "javascript"}
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}


@dataclass
class Finding:
    level: str
    file: Path
    message: str

    def render(self) -> str:
        return f"{self.level}: {self.file}: {self.message}"


class ImgAltParser(HTMLParser):
    def __init__(self, file: Path) -> None:
        super().__init__()
        self.file = file
        self.findings: list[Finding] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "img":
            return
        attr_map = {name.lower(): value for name, value in attrs}
        src = attr_map.get("src") or "(sem src)"
        alt = attr_map.get("alt")
        if alt is None or not alt.strip():
            self.findings.append(
                Finding("ERROR", self.file, f"imagem sem alt não vazio: {src}")
            )


def expand_inputs(patterns: list[str]) -> list[Path]:
    files: list[Path] = []
    for pattern in patterns:
        matches = glob.glob(pattern, recursive=True)
        if matches:
            files.extend(Path(match) for match in matches)
        else:
            files.append(Path(pattern))
    return sorted({path.resolve() for path in files})


def line_col(text: str, index: int) -> tuple[int, int]:
    line = text.count("\n", 0, index) + 1
    last_newline = text.rfind("\n", 0, index)
    col = index + 1 if last_newline == -1 else index - last_newline
    return line, col


def is_remote_ref(ref: str) -> bool:
    parsed = urlparse(ref)
    return parsed.scheme.lower() in REMOTE_SCHEMES or ref.startswith("//")


def resolve_local_ref(html_file: Path, ref: str) -> Path:
    clean_ref = ref.split("#", 1)[0].split("?", 1)[0]
    return (html_file.parent / clean_ref).resolve()


def validate_image_binary(path: Path, html_file: Path) -> list[Finding]:
    findings: list[Finding] = []
    if path.suffix.lower() not in IMAGE_EXTENSIONS:
        return findings
    if path.stat().st_size <= 1024:
        findings.append(Finding("ERROR", html_file, f"imagem local <= 1KB: {path}"))
        return findings
    if path.suffix.lower() == ".svg":
        return findings
    try:
        from PIL import Image
    except ImportError:
        findings.append(
            Finding(
                "WARN",
                html_file,
                "Pillow não instalado; validação binária de imagens raster pulada",
            )
        )
        return findings
    try:
        with Image.open(path) as image:
            image.verify()
    except Exception as exc:
        findings.append(Finding("ERROR", html_file, f"imagem inválida {path}: {exc}"))
    return findings


def validate_file(path: Path) -> list[Finding]:
    findings: list[Finding] = []
    if not path.exists():
        return [Finding("ERROR", path, "arquivo não encontrado")]
    text = path.read_text(encoding="utf-8")

    try:
        parser = HTMLParser()
        parser.feed(text)
    except Exception as exc:
        findings.append(Finding("ERROR", path, f"HTMLParser falhou: {exc}"))

    for match in CHINESE_RE.finditer(text):
        line, col = line_col(text, match.start())
        findings.append(
            Finding(
                "ERROR",
                path,
                f"caractere chinês detectado em {line}:{col}: {match.group(0)!r}",
            )
        )

    for match in CODE_BLOCK_SCRIPT_RE.finditer(text):
        line, col = line_col(text, match.start())
        findings.append(
            Finding(
                "ERROR",
                path,
                f"<script> dentro de <code-block> em {line}:{col}; use texto direto ou <textarea> quando houver < >",
            )
        )

    open_phase: tuple[str, int, int] | None = None
    for match in re.finditer(r"<!--(?P<comment>.*?)-->", text, re.DOTALL):
        comment = match.group("comment")
        start_match = PHASE_START_RE.search(comment)
        end_match = PHASE_END_RE.search(comment)
        if start_match:
            phase = start_match.group(1)
            line, col = line_col(text, match.start())
            if open_phase is not None:
                previous_phase, previous_line, previous_col = open_phase
                findings.append(
                    Finding(
                        "ERROR",
                        path,
                        f"Etapa {phase} começou em {line}:{col} antes do fim Etapa {previous_phase} aberto em {previous_line}:{previous_col}",
                    )
                )
            open_phase = (phase, line, col)
        if end_match:
            phase = end_match.group(1)
            line, col = line_col(text, match.start())
            if open_phase is None:
                findings.append(
                    Finding("ERROR", path, f"fim Etapa {phase} sem Etapa correspondente em {line}:{col}")
                )
            elif open_phase[0] != phase:
                findings.append(
                    Finding(
                        "ERROR",
                        path,
                        f"fim Etapa {phase} em {line}:{col} não corresponde à Etapa {open_phase[0]} aberta em {open_phase[1]}:{open_phase[2]}",
                    )
                )
                open_phase = None
            else:
                open_phase = None
    if open_phase is not None:
        phase, line, col = open_phase
        findings.append(
            Finding("ERROR", path, f"Etapa {phase} aberta em {line}:{col} sem comentário fim Etapa {phase}")
        )

    img_parser = ImgAltParser(path)
    img_parser.feed(text)
    findings.extend(img_parser.findings)

    missing_ref_seen: set[str] = set()
    warned_pillow = False
    for match in LOCAL_REF_RE.finditer(text):
        ref = match.group(1).strip()
        if not ref or is_remote_ref(ref):
            continue
        target = resolve_local_ref(path, ref)
        if not target.exists():
            if ref not in missing_ref_seen:
                findings.append(Finding("ERROR", path, f"referência local ausente: {ref}"))
                missing_ref_seen.add(ref)
            continue
        image_findings = validate_image_binary(target, path)
        for finding in image_findings:
            if finding.level == "WARN" and "Pillow" in finding.message:
                if warned_pillow:
                    continue
                warned_pillow = True
            findings.append(finding)

    return findings


def main() -> int:
    arg_parser = argparse.ArgumentParser(
        description="Validate Reveal.js slide HTML files deterministically."
    )
    arg_parser.add_argument("files", nargs="+", help="HTML files or glob patterns")
    args = arg_parser.parse_args()

    files = expand_inputs(args.files)
    all_findings: list[Finding] = []
    for file in files:
        all_findings.extend(validate_file(file))

    for finding in all_findings:
        print(finding.render())

    errors = [finding for finding in all_findings if finding.level == "ERROR"]
    warnings = [finding for finding in all_findings if finding.level == "WARN"]
    print(f"Checked {len(files)} file(s): {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
