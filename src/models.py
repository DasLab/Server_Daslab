from django.contrib.auth.models import User
from django.db import models
from django import forms

from src.settings import *

import os


def get_member_image(instance, filename):
    name = instance.first_name.strip() + instance.last_name[0].strip()
    ext = filename[filename.rfind('.'):]
    return PATH.DATA_DIR['MEMBER_IMG_DIR'] + '%s%s' % (name,ext)

def get_pub_pdf(instance, filename):
    return PATH.DATA_DIR['PUB_PDF_DIR'] + '%s' % filename

def get_pub_image(instance, filename):
    return PATH.DATA_DIR['PUB_IMG_DIR'] + '%s' % filename

def get_pub_data(instance, filename):
    return PATH.DATA_DIR['PUB_DAT_DIR'] + '%s' % filename


class NewsItem(models.Model):
    title = models.CharField(max_length=255)
    content = models.CharField(max_length=1023, blank=True)
    date = models.DateField()

class Member(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    department = models.CharField(max_length=255, blank=True)
    more_info = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to=get_member_image, blank=True, max_length=255)
    joint_lab = models.CharField(max_length=255, blank=True)
    joint_link = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=255, blank=True)

    alumni = models.BooleanField(default=False)
    start_year = models.PositiveSmallIntegerField(blank=True, null=True)
    finish_year = models.PositiveSmallIntegerField(blank=True, null=True)


class Publication(models.Model):
    authors = models.TextField()
    year = models.PositiveSmallIntegerField()
    display_date = models.DateField()
    title = models.TextField()
    journal = models.CharField(max_length=255, blank=True, null=True)
    volume = models.CharField(max_length=31, blank=True, null=True)
    issue = models.CharField(max_length=31, blank=True, null=True)
    begin_page = models.CharField(max_length=31, blank=True, null=True)
    end_page = models.CharField(max_length=31, blank=True, null=True)

    pdf = models.FileField(upload_to=get_pub_pdf, blank=True, max_length=255)
    preprint = models.BooleanField(default=False)
    link = models.CharField(max_length=255, blank=True)

    extra_field = models.CharField(max_length=255, blank=True)
    extra_link = models.CharField(max_length=255, blank=True)
    extra_field_2 = models.CharField(max_length=255, blank=True)
    extra_link_2 = models.CharField(max_length=255, blank=True)
    extra_field_3 = models.CharField(max_length=255, blank=True)
    extra_file = models.FileField(upload_to=get_pub_data, blank=True, max_length=255)

    feature = models.BooleanField(default=False)
    image = models.ImageField(upload_to=get_pub_image, blank=True, max_length=255)




