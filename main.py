"""news-image-20261121 v3 entrypoint.

Copies the rendered image.png (kept alongside this file) to
$MAKEFUN_OUTPUT_DIR/entry.png. Standard library only; no network access,
no extra files written.
"""

import hashlib
import os
import shutil
import sys


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        raise SystemExit("MAKEFUN_OUTPUT_DIR is not set")
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "image.png")
    if not os.path.isfile(src):
        raise SystemExit("missing image.png next to main.py: %s" % src)
    want = _sha256(src)
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    # integrity: the copy must be byte-identical to the source
    got = _sha256(dst)
    if got != want:
        raise SystemExit("entry.png copy mismatch: %s != %s" % (got, want))
    # the output dir must contain ONLY entry.png
    names = sorted(os.listdir(out_dir))
    if names != ["entry.png"]:
        raise SystemExit("unexpected files in output dir: %r" % (names,))
    print("wrote %s sha256=%s" % (dst, got))
    return 0


if __name__ == "__main__":
    sys.exit(main())
