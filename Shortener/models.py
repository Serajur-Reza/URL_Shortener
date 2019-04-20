from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django_hosts.resolvers import reverse

# Create your models here.

from .validators import valid
from .utils import code_generator,create_shortCode

SHORTCODE_MAX=getattr(settings, "SHORTCODE_MAX", 15)

class URLManager(models.Manager):
    def all(self, *args, **kwargs):
        qs_main = super(URLManager, self).all(*args,**kwargs)
        qs=qs_main.filter(active=True)
        return qs

    def refresh_codes(self ,items=100):
        print(items)
        qs=URL.objects.filter(id_gte=1)

        if items is not None and isinstance(items, int):
            qs=qs.order_by('-id')[:items]

        new_codes=0
        for q in qs:
            q.shortCode=create_shortCode(q)
            print(q.shortCode)
            q.save()
            new_codes+=1
        return "New codes are {i}".format(i=new_codes)

class URL(models.Model):
    url=models.CharField(max_length=220, validators=[valid])
    shortCode=models.CharField(max_length=SHORTCODE_MAX, unique=True, blank=True)
    updated=models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    active= models.BooleanField(default=True)

    objects=URLManager()

    def save(self, *args, **kwargs):
        if self.shortCode is None or self.shortCode == "":
            self.shortCode=create_shortCode(self)

        if not "http" in self.url:
            self.url="http://"+self.url

        super(URL, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.url)

    def __unicode__(self):
        return str(self.url)

    def get_short_code(self):
        url_path=reverse("sCode", kwargs={'shortCode':self.shortCode}, host='www', scheme='http')
        return url_path
