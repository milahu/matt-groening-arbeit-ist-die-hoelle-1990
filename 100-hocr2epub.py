#!/usr/bin/env python3

import glob
import os
import re
import shutil
import subprocess
import sys
import zipfile
import shlex
from datetime import datetime
from pathlib import Path

from _shared import (
    load_config,
    get_page_num,
)


src = Path("090-ocr")

# write EPUB file
# dst = Path(Path(__file__).stem + ".epub")

# write unpacked EPUB files to workdir
dst = Path(".")


config = load_config()


if dst != Path(".") and dst.exists():
    print(f"error: output exists: {dst}")
    sys.exit(1)


# downscale to 300 dpi
# 600 dpi -> 300 dpi: 90 MB -> 60 MB
scale = 300 / config.scan_resolution


hocr_to_epub_fxl = "hocr-to-epub-fxl"

# TODO dont commit
if 1:
    hocr_to_epub_fxl = "/home/user/src/archive-hocr-tools/bin/hocr-to-epub-fxl"

args = [
    hocr_to_epub_fxl,
    "--output", str(dst),
]

if dst == Path("."):
    args.append("--output-unpacked")


def git_modified():
    return subprocess.check_output(
        ["git", "show", "-s", "--format=%cI", "HEAD"],
        text=True,
    ).strip()


def stat_modified(path):
    ts = Path(path).stat().st_mtime
    dt = datetime.fromtimestamp(ts).astimezone()
    return dt.isoformat(timespec="seconds")


doc_modified = max(
    git_modified(),
    stat_modified(src),
)


args += [
    "--scale", str(scale),
    "--image-format", "avif",
    "--text-format", "html",
    # TODO? move these config items to 000-config.py
    "--doc-modified", doc_modified,
    "--doc-title", "Arbeit ist die Hölle",
    # "--doc-subtitle", "",
    # "--doc-subject", "",
    "--doc-date", "1990",
    "--doc-edition", "1",
    "--doc-extent", "48 pages",
    "--color-image-pages", "49-",
    "--doc-author", "Matt Groening",
    # "--doc-introducer", "",
    # "--doc-contributor", "",
    # "--doc-translator", "",
    "--doc-publisher", "Wolfgang Krüger Verlag",
    "--doc-language", "de", # german
    # "--doc-language", "en", # english
    "--doc-isbn", "9783810508294",
    "--doc-cover-image", "0663-level/049.tiff",
    "--canonical-url-base", "https://milahu.github.io/matt-groening-arbeit-ist-die-hoelle-1990/",
    "--doc-description", """
Ist Arbeit die Hölle?

"SIMPSONS"-Erfinder Matt Groening unternimmt
im zweiten Sammelband seines wegweisenden Comic-strips "LIFE IN HELL"
einen Streifzug durch die Niederungen des Arbeitslebens,
die Frustrationen des Büroalltags und das Fegefeuer des Kollegenspotts.

Vom ersten Kapitel "Ran an den Feind!"
über die Lektion "Wie man täglich acht Stunden totschlägt und trotzdem seinen Job behält"
bis hin zur Bestands-aufnahme "So so, man hat dir gekündigt"
erweist sich "ARBEIT IST DIE HÖLLE" als unverzichtbarer Ratgeber
für jeden Berufstätigen und solche die es werden wollen.

Noch ungezügelter als in "DIE SIMPSONS"
lässt Matt Groening in "LIFE IN HELL"
seinem Sinn für bissige, schwarzhumorige Alltagssatire freien Lauf.
""",
]


print(">", shlex.join(args + sys.argv[1:]) + f" {src}/*.hocr")


hocr_files = list(src.glob("*.hocr"))

hocr_files.sort()

subprocess.run(
    args + sys.argv[1:] + hocr_files,
    check=True,
)


if dst == Path("."):
    print("done ./index.xhtml")
    sys.exit(0)


print(f"done {dst}")


# extract the EPUB content files

# rm -rf $dst.unzip
unzip_dir = Path(str(dst) + ".unzip")
shutil.rmtree(unzip_dir, ignore_errors=True)
unzip_dir.mkdir()


# unzip -q ../$dst
with zipfile.ZipFile(dst) as z:
    z.extractall(unzip_dir)


print(f"done {unzip_dir}/index.html")
