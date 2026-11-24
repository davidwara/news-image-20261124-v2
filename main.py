#!/usr/bin/env python3
"""Grade-time program for news-image-20261124 v2.

Pure Python standard library only. No network, no third-party imports,
no writes into the repository directory.

Reads the pre-rendered front page (entry.png) from this program's own
directory, validates it, and copies it to $MAKEFUN_OUTPUT_DIR/entry.png
(default /output). A byte copy is fully deterministic across runs.
"""

import os
import struct
import sys

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1024 * 1024  # 1 MiB


def fail(message):
    print("error: " + message, file=sys.stderr)
    return 1


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    try:
        with open(source, "rb") as handle:
            data = handle.read()
    except OSError as exc:
        return fail("cannot read entry.png: %s" % exc)

    if len(data) > MAX_BYTES:
        return fail("entry.png is %d bytes, over the 1 MiB limit" % len(data))
    if len(data) < 8 or data[:8] != PNG_MAGIC:
        return fail("entry.png does not start with the PNG magic bytes")
    # The IEND chunk is exactly 12 bytes: zero length, "IEND", CRC.
    if len(data) < 12 or data[-12:-8] != b"\x00\x00\x00\x00" or data[-8:-4] != b"IEND":
        return fail("entry.png has no valid IEND trailer")

    # Parse the IHDR chunk: length (4) + "IHDR" (4) + width (4) +
    # height (4) + bit depth (1) + colour type (1).
    if len(data) < 29 or data[12:16] != b"IHDR":
        return fail("entry.png has no IHDR chunk where expected")
    width, height = struct.unpack(">II", data[16:24])
    bit_depth = data[24]
    colour_type = data[25]
    if (width, height) != (1024, 1024):
        return fail("entry.png is %dx%d, expected 1024x1024" % (width, height))
    if bit_depth != 8:
        return fail("entry.png bit depth is %d, expected 8" % bit_depth)
    if colour_type != 2:
        return fail("entry.png colour type is %d, expected 2 (RGB)" % colour_type)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    try:
        os.makedirs(out_dir, exist_ok=True)
        destination = os.path.join(out_dir, "entry.png")
        with open(destination, "wb") as handle:
            handle.write(data)
    except OSError as exc:
        return fail("cannot write output: %s" % exc)

    print("wrote %s (%d bytes, %dx%d RGB)" % (destination, len(data), width, height))
    return 0


if __name__ == "__main__":
    sys.exit(main())
