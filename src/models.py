from django.contrib.auth.models import User
from django.db import models
from django import forms

from src.settings import *

import os


def get_member_image(instance, filename):
    return PATH.DATA_DIR['MEMBER_IMG_DIR'] + '%s' % instance.image


class NewsItem(models.Model):
    title = models.CharField(max_length=255)
    content = models.CharField(max_length=1023, blank=True)
    date = models.DateField()

class CurrentMember(models.Model):
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    more_info = models.CharField(max_length=255)
    image = models.FileField(upload_to=get_member_image, blank=True, null=True)
    joint_lab = models.CharField(max_length=31)
    joint_link = models.CharField(max_length=255)
    description = models.CharField(max_length=255)


