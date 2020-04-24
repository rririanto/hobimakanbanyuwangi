#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
from urllib.parse import urlparse
from django.core.wsgi import get_wsgi_application
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.base'
application = get_wsgi_application()

from config.settings import base
from culinary.models import *
import sys
import re
import random
import string
import hashlib
import uuid
import simplejson
import datetime
import simplejson
import unicodedata
import requests
import unicodedata
from io import StringIO
from io import BytesIO
from PIL import Image
import urllib
from django.core.files.uploadedfile import InMemoryUploadedFile
import unicodedata
import urllib.parse
from urllib.parse import urljoin


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


def grab_image(url):
    urlsplit = urljoin(url, urlparse(url).path)
    name, ext = os.path.splitext(urlsplit)
    namesave = "%s%s" % (name, ext)
    mimetype = 'image/jpeg'
    if ext == ".mp4":
        mimetype = 'video/mp4'
    url = url
    opener = urllib.request.build_opener()
    opener.addheaders = [
        ('User-agent',
         'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20120427 Firefox/15.0a1')]
    file = BytesIO(opener.open(url).read())
    temp_save = StringIO()
    newFile = InMemoryUploadedFile(
        file, None, namesave, mimetype, len(
            file.getbuffer()), None)
    return newFile



def main():
    get_data = open('hobimakanall/hobimakan.banyuwangi.json').read()
    data = simplejson.loads(get_data)
    sort = {"items" : sorted(data["GraphImages"], key=lambda d: d["id"])}
    # data.reverse()
    post = []
    for i in sort["items"]:
        unique_id = i['shortcode']
        if unique_id == "BgtRSQolnhF":
         try:
            caption = i['edge_media_to_caption']['edges'][0]['node']['text']

            cap = unicodedata.normalize('NFKD', caption)
            cap = replace_text(cap)
            name = re.search('(.*)[\n]Address:', cap)
            print (name.group(1))
            if name:
                try:
                    post = CulinaryPlace.objects.get(unique_id=unique_id)
                except BaseException:
                    post = CulinaryPlace(
                        unique_id=unique_id,
                        name=name.group(1),
                    )
                    post.save()

                    post.description = cap
                    post.save()

                    is_video = i['is_video']
                    graph_type = i['__typename']

                    post.shortcode = i['shortcode']
                    post.typename = graph_type
                    post.save()

                    urls = None
                    watchcount = 0

                    like_count = i['edge_media_preview_like']['count']
                    comment_count = i['edge_media_to_comment']['count']
                    post.cmcount = int(comment_count)
                    post.likecount = int(like_count)
                    post.watchcount = int(watchcount)
                    post.save()

                    tags = i['tags']
                    if tags:
                        for x in tags:
                            post.tags.add(x)
                            post.save()

                    urls = i['urls']  # video
                    if is_video == "true":
                        watchcount = i['video_view_count']

                    if urls:
                        c = 0
                        for x in urls:
                            if c == 0:
                                post.photo = grab_image(x)
                                post.save()
                                c += 1
                            else:
                                unique_id = os.path.basename(x).split("_")
                                if unique_id:
                                    try:
                                        postmedia = MediaFile.objects.get(
                                            culinary_id=post, unique_id=unique_id[0])
                                    except BaseException:
                                        postmedia = MediaFile(
                                            unique_id=unique_id[0],
                                            culinary_id=post,
                                            media=grab_image(x)
                                        )
                                        postmedia.save()

                    addr = re.search('Address:(.*)\n', cap)
                    hours = re.search('Hours:(.*)\n', cap)
                    price_info = re.search('PriceInfo:(.*)\n', cap)
                    ratings = re.search('Ratings:(.*)\n', cap)
                    igaccount = re.search('InstagramAccount:(.*)\n', cap)
                    tlp = re.search('Telephone:(.*)\n', cap)
                    lat_lang = re.search('LatLang:(.*)\n', cap)

                    if addr:
                        post.address = addr.group(1)
                        post.save()

                    if hours:
                        post.hours = hours.group(1)
                        post.save()

                    if price_info:
                        post.priceinfo = price_info.group(1)
                        post.save()

                    if ratings:
                        post.ratings = ratings.group(1)
                        post.save()

                    if not ratings:
                        capr = cap.replace("⭐", "Ratings2:")
                        capr = re.search("Ratings2:(.*)\n", capr)
                        post.ratings = capr.group(1)
                        post.save()

                    if igaccount:
                        post.igaccount = igaccount.group(1)
                        post.save()

                    if tlp:
                        post.phone = tlp.group(1)
                        post.save()

                    if lat_lang:
                        post.lat_lang = lat_lang.group(1)
                        post.save()

         except Exception as e:
            print("https://www.instagram.com/p/" + i["shortcode"])
            print(e)
            continue


if __name__ == "__main__":
    main()
