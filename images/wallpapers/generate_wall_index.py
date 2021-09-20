#!/usr/bin/env python3

import glob
import sys
from json import dump
from os import path

import subprocess


def generate_thumbs(orig_file):
    head, tail = path.split(orig_file)
    ext = path.splitext(tail)[1][1:]
    cmd = f"mogrify  -format {ext} -path thumbs -thumbnail 300x300 {tail}"
    subprocess.Popen(cmd, cwd=head, shell=True)


def generate_wall_index():
    wall_list = []
    prefix = sys.argv[1]
    files = [f for f in sorted(glob.glob("*/*")) if path.isfile(f)]
    count = 0
    for file in files:
        split_p = list(path.split(file))
        file_name = split_p[-1]
        file_url = "/".join(split_p)
        split_p.insert(-1, "thumbs")  # Squeeze the thumbs folder into the path
        thumb_url = "/".join(split_p)
        if not path.isfile(thumb_url):
            generate_thumbs(file_url)

        wall_p = dict()
        wall_p["filename"] = file_name
        wall_p["url"] = prefix + file_url
        wall_p["thumb"] = prefix + thumb_url
        wall_p["creator"] = "AICP"  # Still haven't figure out how to attribute to original creators
        wall_p["name"] = f"Wallpaper {count + 1:02}"  # Else #1 is followed by # 10
        count += 1
        wall_list.append(wall_p)

    with open("wallpaper_index.json", "w", encoding="utf-8") as index_file:
        dump(wall_list, index_file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(f'usage: {sys.argv[0]} [url|https://raw.githubusercontent.com/AICP/aicp-media/master/images/wallpapers/]')
    generate_wall_index()
