#!/bin/sh

# TODO set config values
# cover_src=0663-level/049.tiff
cover_src=0663-level/051.tiff # clean

magick "$cover_src" -scale 50% -quality 50% cover.avif
