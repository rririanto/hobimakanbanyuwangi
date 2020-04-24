#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
import simplejson
import django
import sys

from pathlib import Path
BASE_DIR = Path.cwd()
SCRIPT_PATH = str(BASE_DIR / Path(__file__).parents[0])
sys.path.append(str(BASE_DIR))
django.setup()
from culinary.models import *


def main():
    get_data = open(f'{SCRIPT_PATH}/data/hobimakan.banyuwangi.json').read()
    data = simplejson.loads(get_data)
    sort = {"items": sorted(data["GraphImages"], key=lambda d: d["id"])}
    post = []
    for i in sort["items"]:
        unique_id = i['id']
        try:
            post = CulinaryPlace.objects.get(unique_id=unique_id)
        except BaseException:
            continue

        watchcount = 0
        is_video = i.get("is_video", False)
        like_count = i['edge_media_preview_like']['count']
        comment_count = i['edge_media_to_comment']['count']
        post.cmcount = int(comment_count)
        post.likecount = int(like_count)
        if is_video:
            watchcount = i['video_view_count']
        post.watchcount = int(watchcount)
        post.save()


if __name__ == "__main__":
    main()
