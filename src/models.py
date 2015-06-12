from django.contrib.auth.models import User
from django.db import models
from django import forms

from src.settings import *

import os


def get_member_image(instance, filename):
    name = instance.first_name + instance.last_name[0]
    ext = filename[filename.rfind('.'):]
    return PATH.DATA_DIR['MEMBER_IMG_DIR'] + '%s%s' % (name,ext)


class NewsItem(models.Model):
    title = models.CharField(max_length=255)
    content = models.CharField(max_length=1023, blank=True)
    date = models.DateField()

class CurrentMember(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    more_info = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to=get_member_image, blank=True, max_length=255)
    joint_lab = models.CharField(max_length=255, blank=True)
    joint_link = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=255, blank=True)

class PastMember(models.Model):
    full_name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    start_year = models.PositiveSmallIntegerField()
    finish_year = models.PositiveSmallIntegerField()
    


