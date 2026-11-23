"""Entry program for the news-image-20261123 bounty.

Copies the pre-rendered front-page image (entry.png, shipped in this
repository) to the grader's output directory as /output/entry.png.
Standard library only; no network use; deterministic output.

The image itself was drawn by the builder session with Pillow on this
machine and saved as entry.png; this program only copies those bytes,
so it runs in the grader's stdlib-only sandbox.
"""

import os
import shutil
from pathlib import Path

OUTPUT_NAME = "entry.png"


def main() -> None:
    """Copy entry.png beside this file into the output directory."""
    here = Path(__file__).resolve().parent
    src = here / OUTPUT_NAME
    if not src.is_file():
        raise FileNotFoundError(f"missing shipped image: {src}")
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, out_dir / OUTPUT_NAME)
    print(f"wrote {out_dir / OUTPUT_NAME} ({src.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
