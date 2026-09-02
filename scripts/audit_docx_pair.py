#!/usr/bin/env python3
"""Compare fidelity-sensitive parts of a source and interpreted DOCX."""

import argparse
import hashlib
import sys
from zipfile import ZipFile
from lxml import etree

NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
STATIC_PARTS = (
    "word/styles.xml",
    "word/numbering.xml",
    "word/settings.xml",
    "word/fontTable.xml",
)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def document_counts(archive):
    root = etree.fromstring(archive.read("word/document.xml"))
    return {
        "paragraphs": len(root.xpath(".//w:p", namespaces=NS)),
        "tables": len(root.xpath(".//w:tbl", namespaces=NS)),
        "drawings": len(root.xpath(".//w:drawing", namespaces=NS)),
        "sections": len(root.xpath(".//w:sectPr", namespaces=NS)),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source")
    parser.add_argument("interpreted")
    args = parser.parse_args()
    failures = []

    with ZipFile(args.source) as src, ZipFile(args.interpreted) as out:
        src_media = sorted(n for n in src.namelist() if n.startswith("word/media/"))
        out_media = sorted(n for n in out.namelist() if n.startswith("word/media/"))
        media_ok = src_media == out_media and all(
            digest(src.read(n)) == digest(out.read(n)) for n in src_media
        )
        print(f"embedded_media_identical={media_ok} files={len(src_media)}")
        if not media_ok:
            failures.append("embedded media changed")

        for part in STATIC_PARTS:
            present = part in src.namelist() and part in out.namelist()
            same = present and src.read(part) == out.read(part)
            print(f"{part}_identical={same}")
            if present and not same:
                failures.append(f"{part} changed")

        a, b = document_counts(src), document_counts(out)
        for key in a:
            same = a[key] == b[key]
            print(f"{key}_same={same} source={a[key]} interpreted={b[key]}")
            if not same:
                failures.append(f"{key} count changed")

    if failures:
        print("AUDIT_RESULT=REVIEW_REQUIRED")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("AUDIT_RESULT=PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
