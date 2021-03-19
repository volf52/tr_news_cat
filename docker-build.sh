#!/usr/bin/env bash

find . -regex '^.*\(__pycache__\|\.py[co]\)$' -delete # Remove __pycache__ etc
tar -cf dirs.tar news_cat/ artifacts/ metrics/
docker build -t newscat .
rm dirs.tar