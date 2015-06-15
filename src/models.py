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

def get_news_image(instance, filename):
    return PATH.DATA_DIR['NEWS_IMG_DIR'] + '%s' % filename

def get_rot_ppt(instance, filename):
    name = instance.date.strftime('%Y%m%d') + '_' + instance.full_name.replace(' ','')
    ext = filename[filename.rfind('.'):]
    return PATH.DATA_DIR['ROT_PPT_DIR'] + '%s%s' % (name,ext)

def get_rot_data(instance, filename):
    name = instance.date.strftime('%Y%m%d') + '_' + instance.full_name.replace(' ','')
    ext = filename[filename.rfind('.'):]
    return PATH.DATA_DIR['ROT_DAT_DIR'] + '%s%s' % (name,ext)

def get_spe_ppt(instance, filename):
    return PATH.DATA_DIR['SPE_PPT_DIR'] + '%s' % filename


class News(models.Model):
    date = models.DateField()
    content = models.TextField(blank=True)
    link = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to=get_news_image, blank=True, null=True, max_length=255)
    video = models.CharField(max_length=255, blank=True, null=True)

    class Meta():
        verbose_name = 'News Item'
        verbose_name_plural = 'News Items'


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

    class Meta():
        verbose_name = 'Member'
        verbose_name_plural = 'Member Management'


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

    class Meta():
        verbose_name = 'Publication Entry'
        verbose_name_plural = 'Publication Entries'
        

############################################################################################################################################

class FlashSlide(models.Model):
    date = models.DateField()
    link = models.CharField(max_length=255, blank=True)

    class Meta():
        verbose_name = 'Flash Slide'
        verbose_name_plural = 'Flash Slides'


class RotationStudent(models.Model):
    date = models.DateField()
    full_name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    ppt = models.FileField(upload_to=get_rot_ppt, blank=True, max_length=255)
    data = models.FileField(upload_to=get_rot_data, blank=True, max_length=255)

    class Meta():
        verbose_name = 'Rotation Presentation'
        verbose_name_plural = 'Rotation Presentations'


class EternaYoutube(models.Model):
    date = models.DateField()
    presenter = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    link = models.CharField(max_length=255, blank=True)

    class Meta():
        verbose_name = 'EteRNA Open Group Meeting'
        verbose_name_plural = 'EteRNA Open Group Meetings'


class Presentation(models.Model):
    date = models.DateField()
    presenter = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    ppt = models.FileField(upload_to=get_spe_ppt, blank=True, max_length=255)
    link = models.CharField(max_length=255, blank=True)

    class Meta():
        verbose_name = 'Archived Presentation'
        verbose_name_plural = 'Archived Presentations'


