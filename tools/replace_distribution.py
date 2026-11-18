#!/usr/bin/env python3
"""Replace the Distribution file inside a flat macOS installer package (.pkg).

A flat .pkg is a xar archive. This script rewrites only the table of contents
and appends the new Distribution data to the heap, so the ~580 MB driver
payload is copied byte for byte and never recompressed. It works on Linux or
macOS with only the Python standard library.

Usage:
    python3 tools/replace_distribution.py IN.pkg Distribution OUT.pkg

On a Mac you can do the same thing with Apple's tools instead:
    pkgutil --expand IN.pkg expanded
    cp Distribution expanded/Distribution
    pkgutil --flatten expanded OUT.pkg
"""
import bz2
import hashlib
import shutil
import struct
import sys
import xml.etree.ElementTree as ET
import zlib

HEADER = struct.Struct(">4sHHQQI")


def main(src, dist_path, dst):
    with open(src, "rb") as f:
        magic, hsize, ver, clen, ulen, cksum_alg = HEADER.unpack(f.read(HEADER.size))
        if magic != b"xar!":
            sys.exit(f"{src} is not a flat package (xar archive)")
        if cksum_alg != 1:
            sys.exit("only SHA-1 table-of-contents checksums are supported")
        f.seek(hsize)
        toc = ET.fromstring(zlib.decompress(f.read(clen)))
        heap_start = hsize + clen
        f.seek(0, 2)
        heap_len = f.tell() - heap_start

    root = toc.find("toc")
    if root.find("signature") is not None or root.find("x-signature") is not None:
        sys.exit("package is signed; replacing Distribution would invalidate it")

    dist_entry = next(
        (e for e in root.findall("file") if e.findtext("name") == "Distribution"), None
    )
    if dist_entry is None:
        sys.exit("no top-level Distribution file found")

    raw = open(dist_path, "rb").read()
    packed = bz2.compress(raw)
    data = dist_entry.find("data")
    data.find("length").text = str(len(packed))
    data.find("offset").text = str(heap_len)
    data.find("size").text = str(len(raw))
    data.find("encoding").set("style", "application/x-bzip2")
    data.find("extracted-checksum").text = hashlib.sha1(raw).hexdigest()
    data.find("extracted-checksum").set("style", "sha1")
    data.find("archived-checksum").text = hashlib.sha1(packed).hexdigest()
    data.find("archived-checksum").set("style", "sha1")
    # Drop stale extended attributes (quarantine/provenance) from the old file.
    for ea in dist_entry.findall("ea"):
        dist_entry.remove(ea)

    ck = root.find("checksum")
    ck_off, ck_size = int(ck.findtext("offset")), int(ck.findtext("size"))

    toc_xml = b'<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(toc)
    toc_z = zlib.compress(toc_xml, 9)
    toc_sha = hashlib.sha1(toc_z).digest()
    assert len(toc_sha) == ck_size

    with open(src, "rb") as fin, open(dst, "wb") as fout:
        fout.write(HEADER.pack(b"xar!", hsize, ver, len(toc_z), len(toc_xml), 1))
        fout.write(b"\0" * (hsize - HEADER.size))
        fout.write(toc_z)
        fin.seek(heap_start)
        fout.write(fin.read(ck_off))
        fout.write(toc_sha)
        fin.seek(heap_start + ck_off + ck_size)
        shutil.copyfileobj(fin, fout, 16 * 1024 * 1024)
        fout.write(packed)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    main(*sys.argv[1:])
