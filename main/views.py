# -*- coding: utf-8 -*-
from django.core.paginator import InvalidPage, Paginator
from django.http import HttpResponse
from django.shortcuts import render

from django.db.models import Q
from culinary.models import CulinaryPlace
import re
import unicodedata
from django.db.models import Avg
import simplejson
from django.views.decorators.cache import never_cache
from django.template.loader import get_template
from hobimakanbanyuwangi.utils import scrapper
from django.core.cache import cache
import after_response


@never_cache
def sw_js(request):
    template = get_template('sw.js')
    html = template.render()
    return HttpResponse(html, content_type="application/x-javascript")


def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    return [normspace(' ', (t[0] or t[1]).strip())
            for t in findterms(query_string)]


def get_query(query_string, search_fields):
    query = None
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query


def offline(request):
    return HttpResponse("Oops lagi offline yah kaka.")


def search(request):
    data = request.GET
    keyword = data.get('q', None)
    orderby = data.get('orderby', 'terbaru')
    objects = []
    if keyword:
        keyword = unicodedata.normalize(
            'NFKD', unicode(keyword)).encode(
            'ascii', 'ignore').lower()
        entry_query = get_query(keyword, ['name'])
        entry_query2 = get_query(keyword, ['description'])
        entry_query3 = get_query(keyword, ['tags__name'])
        if orderby == "terbaru":
            objects = CulinaryPlace.objects.values(
                'id',
                'slug',
                'name',
                'photo',
                'byratings',
                'cmcount',
                'likecount').order_by('-id').filter(
                entry_query | entry_query2 | entry_query3).prefetch_related('tagged_items__tag')
        elif orderby == "rating":
            objects = CulinaryPlace.objects.values(
                'id',
                'slug',
                'name',
                'photo',
                'byratings',
                'cmcount',
                'likecount').filter(
                entry_query | entry_query2 | entry_query3).annotate(
                total=Avg('byratings'),
                totalx=Avg('likecount')).order_by(
                '-total',
                '-totalx')
        elif orderby == "populer":
            objects = CulinaryPlace.objects.values(
                'id', 'slug', 'name', 'photo', 'byratings', 'cmcount', 'likecount').filter(
                entry_query | entry_query2 | entry_query3).annotate(
                total=Avg('likecount')).order_by('-total')

    else:
        objects = CulinaryPlace.objects.values(
            'id',
            'slug',
            'name',
            'photo',
            'byratings',
            'cmcount',
            'likecount').all().order_by('-id')

    objects = objects.distinct()
    counting = objects.count()
    paginator = Paginator(objects, 24)
    if request.method == 'GET':
        if request.GET.get('page_number'):
            page_number = request.GET.get('page_number')
            try:
                page_objects = paginator.page(page_number).object_list
            except InvalidPage:
                return HttpResponse("")

            context = dict(
                page_objects=page_objects,
                terbaru=True
            )
            return render(
                request,
                'ajax/load_more_index.html',
                context)

    objects = paginator.page(1).object_list

    context = dict(
        object_list=objects,
        keyword=keyword,
        orderby=orderby,
        counting=counting,
    )

    return render(request,
                  'main/search.html',
                  context)


def hashtag(request, slug):
    qs = CulinaryPlace.objects.values(
        'id',
        'slug',
        'name',
        'photo',
        'byratings',
        'cmcount',
        'likecount').filter(
        tags__name=slug)
    tags = CulinaryPlace.tags.most_common(min_count=10)
    paginator = Paginator(qs, 9)
    if request.method == 'GET':

        if request.GET.get('page_number'):
            page_number = request.GET.get('page_number')
            try:
                page_objects = paginator.page(page_number).object_list
            except InvalidPage:
                return HttpResponse("")
            context = dict(
                page_objects=page_objects,
                terbaru=True
            )
            return render(
                request,
                'ajax/load_more_index.html',
                context)

    objects = paginator.page(1).object_list

    context = dict(
        object_list=objects,
        slug=slug,
        tags=tags,
    )

    return render(request,
                  'main/hashtag.html',
                  context)


def check_station(st):
    if st:
        return st[:96]
    else:
        return ''


def getmaps(request):
    data = []
    try:
        cache_key = "getmaps"
        cache_time = 86400
        data = cache.get(cache_key)
        if not data:
            data = CulinaryPlace.objects.filter(lat_lang__isnull=False)
        cache.set(cache_key, data, cache_time)
    except BaseException:
        data = []

    suggestions = simplejson.dumps(
        [
            {
                'type_point': i.name,
                'location_latitude': i.get_lat(),
                'location_longitude': i.get_long(),
                'map_image_url': "http://%s/hobimakanbanyuwangi%s" % (request.META.get('HTTP_HOST'),
                                                                      i.get_logo()),
                'name_point': i.name,
                'description_point': check_station(
                    i.get_caption),
                'address': i.address,
                'hours': i.get_hours(),
                'url_detail': '/kuliner/%s' % i.slug} for i in data])

    return HttpResponse(suggestions, content_type='application/json')


def sekitar(request):
    context = dict(
        sekitar=True,
    )

    return render(request,
                  'main/sekitar.html',
                  context)


def rating(request):
    qs = CulinaryPlace.objects.values(
        'id',
        'slug',
        'name',
        'photo',
        'byratings',
        'cmcount',
        'likecount').annotate(
        total=Avg('byratings'),
        totalx=Avg('likecount')).order_by(
            '-total',
        '-totalx').all()
    paginator = Paginator(qs, 9)
    if request.method == 'GET':
        if request.GET.get('page_number'):
            page_number = request.GET.get('page_number')
            try:
                page_objects = paginator.page(page_number).object_list
            except InvalidPage:
                return HttpResponse("")
            context = dict(
                page_objects=page_objects,
                terbaru=True
            )
            return render(
                request,
                'ajax/load_more_index.html',
                context)

    objects = paginator.page(1).object_list

    context = dict(
        object_list=objects,
        rating=True,
        totalqs=qs.count(),

    )

    return render(request,
                  'main/index.html',
                  context)


def popular(request):
    qs = CulinaryPlace.objects.values(
        'id',
        'slug',
        'name',
        'photo',
        'byratings',
        'cmcount',
        'likecount').all().annotate(
        total=Avg('likecount')).order_by('-total')
    paginator = Paginator(qs, 9)
    if request.method == 'GET':

        if request.GET.get('page_number'):
            page_number = request.GET.get('page_number')
            try:
                page_objects = paginator.page(page_number).object_list
            except InvalidPage:
                return HttpResponse("")
            context = dict(
                page_objects=page_objects,
                terbaru=True
            )
            return render(
                request,
                'ajax/load_more_index.html',
                context)

    objects = paginator.page(1).object_list

    context = dict(
        object_list=objects,
        popular=True,
        totalqs=qs.count(),

    )

    return render(request,
                  'main/index.html',
                  context)


def feed(request):
    qs = CulinaryPlace.objects.values(
        'id',
        'slug',
        'name',
        'photo',
        'byratings',
        'cmcount',
        'likecount').order_by('-id').all()
    paginator = Paginator(qs, 9)
    if request.method == 'GET':
        # if request.is_ajax():
        if request.GET.get('page_number'):
            page_number = request.GET.get('page_number')
            try:
                page_objects = paginator.page(page_number).object_list
            except InvalidPage:
                return HttpResponse("")
            context = dict(
                page_objects=page_objects,
                terbaru=True
            )
            return render(
                request,
                'ajax/load_more_index.html',
                context)

    objects = paginator.page(1).object_list

    context = dict(
        object_list=objects,
        terbaru=True,
        totalqs=qs.count(),
    )

    return render(request,
                  'main/index.html',
                  context)


@after_response.enable
def fetch_instagram():
    if scrapper.InstagramAll().send():
        if scrapper.ExtractorDB().send():
            return True
    else:
        return False


def andreyongz(request):
    get_data = CulinaryPlace.objects.values("name").distinct().all()
    context = dict(
        culinarys=get_data,

    )

    return render(request,
                  'main/formupdate.html',
                  context)


def getculinary(request):
    if request.GET:
        fetch_instagram.after_response()
        return HttpResponse('true')
    return HttpResponse('true')


def getrating(request):
    if request.GET:
        FetchIgRating.delay()
        return HttpResponse('true')
    return HttpResponse('true')


def detail(request, slug):
    if slug:
        get_data = CulinaryPlace.objects.get(slug=slug)
        get_related = get_data.tags.similar_objects()[:4]
        nexclude = [
            'hobimakanbanyuwangi',
            'banyuwangifoodies',
            'instafood',
            'banyuwangi',
            'foodgramers',
            'foodiesbanyuwangi',
            'kulinerbanyuwangi',
            'banyuwangikuliner',
            'indofoodgram']
        type_media = ["GraphVideo"]
        context = dict(
            object=get_data,
            related=get_related,
            nexclude=nexclude,
            type_media=type_media,

        )

    return render(request,
                  'main/detail.html',
                  context)
