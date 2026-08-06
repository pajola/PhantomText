"""Dev tool: re-download the Unicode UTS#39 confusables table into this package.

Uses only the standard library (no ``requests``), so refreshing the data never
adds a runtime dependency.

    python -m phantomtext.data.refresh_homoglyphs
"""

from __future__ import annotations

import urllib.request
from pathlib import Path

URL = "https://www.unicode.org/Public/security/latest/intentional.txt"
DEST = Path(__file__).with_name("intentional.txt")


def main() -> None:
    with urllib.request.urlopen(URL) as response:
        data = response.read()
    DEST.write_bytes(data)
    print(f"Wrote {len(data)} bytes to {DEST}")


if __name__ == "__main__":
    main()
