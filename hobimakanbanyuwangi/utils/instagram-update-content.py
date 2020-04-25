#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
import re
import random
import string
import uuid
import simplejson
import unicodedata
import django
import sys
import os

from pathlib import Path
BASE_DIR = Path.cwd()
SCRIPT_PATH = str(BASE_DIR / Path(__file__).parents[0])
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from culinary.models import *

def key_generator(limit=10):
    uuid_set = str(uuid.uuid4().fields[-1])[:5]
    d = [random.choice(string.letters + string.digits + uuid_set)
         for x in xrange(limit)]
    key = "".join(d)
    return key


def replace_text(capt):
    capt = capt.replace("📎", "Address:")
    capt = capt.replace("⌚", "Hours:")
    capt = capt.replace("💸", "PriceInfo:")
    capt = capt.replace("🌟", "Ratings:")
    capt = capt.replace("📣", "InstagramAccount:")
    capt = capt.replace("☎️", "Telephone:")
    capt = capt.replace("📞", "Telephone:")
    capt = capt.replace("📌", "LatLang:")
    return capt


def main():
    get_data = open(f'{SCRIPT_PATH}/data/hobimakan.banyuwangi.json').read()
    data = simplejson.loads(get_data)
    sort = {
        "items": sorted(
            data["GraphImages"],
            key=lambda d: d["taken_at_timestamp"])}
    # data.reverse()
    post = []
    for i in sort["items"]:
        unique_id = i['id']
        try:
            caption = i['edge_media_to_caption']['edges'][0]['node']['text']
            cap = unicodedata.normalize('NFKD', caption)
            cap = replace_text(cap)
            name = re.search('(.*)[\n]Address:', cap)
            # some place doesn't have address but start with priceinfo
            if not name:
                name = re.search('(.*)[\n]PriceInfo:', cap)

            if name:
                try:
                    post = CulinaryPlace.objects.get(unique_id=unique_id)
                except BaseException:
                    pass

                post.description = cap
                post.save()

                addr = re.search('Address:(.*)\n', cap)
                hours = re.search('Hours:(.*)\n', cap)
                price_info = re.search('PriceInfo:(.*)\n', cap)
                ratings = re.search('Ratings:(.*)\n', cap)
                if not ratings:
                    # admin forgot to use same icons
                    capr = cap.replace("⭐", "Ratings2:")
                    capr = re.search("Ratings2:(.*)\n", capr)
                    # check if ratings is really available
                    if capr:
                        ratings = capr.group(1)

                igaccount = re.search('InstagramAccount:(.*)\n', cap)
                tlp = re.search('Telephone:(.*)\n', cap)
                lat_lang = re.search('LatLang:(.*)\n', cap)

                if addr:
                    post.address = addr.group(1).lstrip()
                    post.save()

                if hours:
                    post.hours = hours.group(1).lstrip()
                    post.save()

                if price_info:
                    post.priceinfo = price_info.group(1).lstrip()
                    post.save()

                if ratings:
                    post.ratings = ratings.group(1)
                    post.save()

                if igaccount:
                    post.igaccount = igaccount.group(1).lstrip()
                    post.save()

                if tlp:
                    post.phone = ''.join(tlp.group(1).split())
                    post.save()

                if lat_lang:
                    post.lat_lang = lat_lang.group(1).replace("+", "-")
                    post.save()

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

        except Exception as e:
            print("https://www.instagram.com/p/" + i["shortcode"])
            print(e)
            continue


if __name__ == "__main__":
    main()
