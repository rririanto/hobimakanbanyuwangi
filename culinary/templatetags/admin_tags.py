from django import template
from django.utils.safestring import mark_safe
from django.template.defaultfilters import stringfilter
from django.utils.text import normalize_newlines
from django.contrib.auth.models import User
#from django.contrib.humanize.templatetags.humanize import intcomma
#from django.template import defaultfilters
#from django.shortcuts import get_object_or_404
from django.db.models import Q
#from itertools import chain
#from operator import attrgetter
#from django.contrib.humanize.templatetags.humanize import naturaltime
import urllib, re

register = template.Library()


def remove_newlines(text):
    """
    Removes all newline characters from a block of text.
    """
    # First normalize the newlines using Django's nifty utility
    normalized_text = normalize_newlines(text)
    # Then simply remove the newlines like so.
    return mark_safe(normalized_text.replace('\n', ' '))

remove_newlines.is_safe = True
remove_newlines = stringfilter(remove_newlines)
register.filter(remove_newlines)

def remove_url(text):
    text = re.sub(r'^https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)
    return text

def remove_space(text):
    text = text.replace(' ', '+')
    return text

def remove_zero(text):
    if text % 1 == 0:
       return int(text)
    else:
       return text
        


def checktags(text):
    if text not in ['hobimakanbanyuwangi', 'banyuwangifoodies', 'instafood', 'banyuwangi', 'foodgramers', 'foodiesbanyuwangi', 'kulinerbanyuwangi', 'banyuwangikuliner', 'indofoodgram']:
       return True
    return False

register.filter('remove_zero', remove_zero)
register.filter('remove_space', remove_space)
register.filter("remove_url", remove_url)
