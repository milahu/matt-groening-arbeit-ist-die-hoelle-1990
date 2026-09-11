#!/bin/sh

# 51 = front cover (clean)
# 0 = empty
# 1-48 = content
# 0 = empty
# 50 = back cover

exec ./082-print-parallel.py --pages 51,0,1-48,0,50 080-img2pdf.pdf
