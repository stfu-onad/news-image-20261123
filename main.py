"""Entry program for the news-image-20261123 bounty (v2).

Copies the pre-rendered front-page image (entry.png, shipped in this
repository) to the grader's output directory as /output/entry.png.
Standard library only; no network use; deterministic output.

v2 image: a newspaper front page for Monday 23 November 2026, built
after the full day's news was in. The hero illustration was generated
by the builder session (no text in it); all headlines, the date and
the captions were drawn with PIL/DejaVu so every word is crisp. Six
main stories (COP31 collapse, AI market sell-off, Democrats' 258-seat
House win, the Merkury sunk off Libya, the Dymer strike rescue, the
Iran-Bahrain strikes) plus a ticker with four more items.

Before copying, the program checks the shipped file is a real PNG
(magic bytes) within the 1 MiB limit, so a corrupt or oversized
image fails loudly instead of silently entering the gate.
"""

import hashlib
import os
import shutil
import struct
from pathlib import Path

OUTPUT_NAME = "entry.png"
MAX_BYTES = 1_048_576
MAX_DIM = 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def validate_png(path: Path) -> int:
    """Return the file size, raising unless path is a PNG within limits."""
    data = path.read_bytes()
    if data[:8] != PNG_MAGIC:
        raise ValueError(f"not a PNG file: {path}")
    if len(data) > MAX_BYTES:
        raise ValueError(f"image too large: {len(data)} > {MAX_BYTES} bytes")
    # IHDR: width and height are the first 8 bytes after the 8-byte
    # chunk header (length + "IHDR") at offset 16.
    width, height = struct.unpack(">II", data[16:24])
    if width > MAX_DIM or height > MAX_DIM:
        raise ValueError(f"image too big: {width}x{height} > {MAX_DIM}x{MAX_DIM}")
    return len(data)


def main() -> None:
    """Copy entry.png beside this file into the output directory."""
    here = Path(__file__).resolve().parent
    src = here / OUTPUT_NAME
    if not src.is_file():
        raise FileNotFoundError(f"missing shipped image: {src}")
    size = validate_png(src)
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, out_dir / OUTPUT_NAME)
    digest = hashlib.sha256(src.read_bytes()).hexdigest()[:16]
    print(f"wrote {out_dir / OUTPUT_NAME} ({size} bytes, sha256 {digest}...)")


if __name__ == "__main__":
    main()
