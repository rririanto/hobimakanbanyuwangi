#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from urllib.parse import urlparse
import re
import random
import string
import uuid
import simplejson
import unicodedata
from io import StringIO
from io import BytesIO
import urllib.request
from django.core.files.uploadedfile import InMemoryUploadedFile
import urllib.parse
from urllib.parse import urljoin
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
    StringIO()
    newFile = InMemoryUploadedFile(
        file, None, namesave, mimetype, len(
            file.getbuffer()), None)
    return newFile

def main():
    get_data = open(f'{SCRIPT_PATH}/data/hobimakan.banyuwangi.json').read()
    data = simplejson.loads(get_data)
    sort = {"items": sorted(data["GraphImages"], key=lambda d: d["taken_at_timestamp"])}
    post = []
    for i in sort["items"]:
        unique_id = i['id']
        try:
            post = CulinaryPlace.objects.get(unique_id=unique_id)
        except BaseException:
            continue
       
        if post.typename == "GraphVideo":
           post.photo = grab_image(i["display_url"])
           post.save()


if __name__ == "__main__":
    main()
