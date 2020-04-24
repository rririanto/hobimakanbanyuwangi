# -*- coding: utf-8 -*-
import datetime
from datetime import timedelta
from django.db import models
from django.template import defaultfilters
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.db.models import Sum
from django.conf import settings
from os.path import splitext
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase
from django.utils.functional import cached_property
import re, os

class Hashtag(TaggedItemBase):
    content_object = models.ForeignKey('CulinaryPlace', on_delete=models.CASCADE)

class GetOrNoneManager(models.Manager):
    """Adds get_or_none method to objects
    """

    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None

        
class CulinaryPlace(models.Model):
    unique_id = models.CharField(max_length=200, blank=True, null=True)
    name = models.CharField(max_length=350, blank=True, null=True)
    slug = models.CharField(max_length=400, blank=True, null=True, unique=True)
    
    cmcount = models.IntegerField(default=0)
    likecount = models.IntegerField(default=0)
    watchcount = models.IntegerField(default=0)


    description = models.TextField(blank=True, null=True)
    address = models.TextField(max_length=500, blank=True, null=True)
        
    ratings = models.CharField(max_length=200, blank=True, null=True)
    
    byratings = models.FloatField(default=0.0)
    bypopular = models.FloatField(default=0.0)

    hours = models.CharField(max_length=300, blank=True, null=True)
    
    lat_lang = models.CharField("lat long", max_length=150, blank=True, null=True)

    phone = models.CharField(max_length=300, blank=True, null=True)
    igaccount = models.CharField(max_length=200, blank=True, null=True) 
      
    shortcode = models.CharField(max_length=20, blank=True, null=True)
    typename = models.CharField(max_length=20, blank=True, null=True)

    verified = models.BooleanField(default=False)
    priceinfo = models.CharField(max_length=300, blank=True, null=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    tags = TaggableManager(through=Hashtag)
    photo = models.ImageField(
        upload_to='uploads/', blank=True, null=True)

    objects = GetOrNoneManager()

    def get_ratings(self):
        ratings = 0
        list = []
        if self.ratings:
           splitrat = self.ratings.split(" ")
           if len(splitrat) >=2:
              for i in splitrat:
                 rex = re.search("(.*)/5", i) 
                 if rex:
                    list.append(rex.group(1).replace(",","."))
              result = [float(x.strip()) for x in list]
              ratings = sum(result)/float(len(result))        
           else:
              rex = re.search("(.*)/5", splitrat[0]) 
              ratings = float(rex.group(1).replace(",","."))
        return ratings
    
    def get_lat(self):
        if self.lat_lang:
           try:
              return self.lat_lang.split(",")[0]
           except:
              return None

    def get_long(self):
        if self.lat_lang:
           try:
              return self.lat_lang.split(",")[1]
           except:
              return None

    def get_popular(self):
        result = (self.likecount + self.cmcount) / 2
        return result

    def get_name(self):
        return self.name.capitalize()
        
    def get_map_url(self):
        mapurl = "https://www.google.com/maps?saddr=My+Location&daddr="+self.lat_lang
        return mapurl

    def get_get_name(self):
        result = self.name
        return result

    def save(self, *args, **kwargs):
        try:
          self.byratings = self.get_ratings()
        except Exception:
          pass

        try:
          self.bypopular = self.get_popular()
        except Exception:
          pass

        try:
           self.slug = defaultfilters.slugify(self.name)
           super(CulinaryPlace, self).save(*args, **kwargs)
        except Exception:
           self.slug = defaultfilters.slugify(self.name) + '-' + self.unique_id[:5]
           super(CulinaryPlace, self).save(*args, **kwargs)
        
    @cached_property
    def get_caption(self):
        try:
            capt = re.search('[\s\S]+Address', self.description).group()
            ## (?:.|\n)+ 
            capt = capt.replace(self.name, '').replace('\n\nAddress','')
            return capt
        except:
           return self.description
    
    def get_hours(self):
        if self.hours:
            return self.hours
        else:
            return "-"


    def delete(self, *args, **kwargs):
        storage, path = self.photo.storage, self.photo.path
        super(CulinaryPlace, self).delete(*args, **kwargs)
        storage.delete(path)

    def __str__(self):
        return "%s" % self.name


class MediaFile(models.Model):
    culinary_id = models.ForeignKey(CulinaryPlace, related_name='culinary_file', on_delete=models.CASCADE)
    unique_id = models.CharField(max_length=20, blank=True, null=True)
    media = models.FileField(
        upload_to='uploads/media/', blank=True, null=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    private = models.BooleanField(default=False)
    pinup = models.BooleanField(default=False)

    def get_name(self):
        name = self.media.name.replace("uploads/resumefile/", "")
        return name

    def get_ext(self):
        name, ext = os.path.splitext(self.media.url)
        return ext

    def __unicode__(self):
        if self.culinary_id:
            return self.culinary_id.name
       
    def delete(self, *args, **kwargs):
        storage, path = self.media.storage, self.media.path
        super(MediaFile, self).delete(*args, **kwargs)
        storage.delete(path)

admin.site.register(MediaFile)
