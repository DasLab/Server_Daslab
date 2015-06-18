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
    date = models.DateField(verbose_name='Display Date')
    content = models.TextField(blank=True, verbose_name='Main Text Content')
    link = models.CharField(max_length=255, blank=True, verbose_name='URL', help_text='<i class="icon-globe"></i> For the "read more" link.')
    image = models.ImageField(upload_to=get_news_image, blank=True, null=True, max_length=255, verbose_name='Display Image', help_text='<i class="icon-picture"></i> For non-EteRNA news displayed as thumbnail. Use <span class="label label-info">png/jpg</span> format, low resolution (<span class="label label-important">NO</span> larger than <span class="label label-inverse">200x300 72dpi</span>).')
    video = models.CharField(max_length=255, blank=True, null=True, verbose_name='YouTube Video Link', help_text='<i class="icon-facetime-video"></i> For EteRNA news displayed as thumbnail. <span class="label label-success">Example</span>: <u>https://www.youtube.com<b>/embed/</b>Lp_KozzV5Po</u>; <span class="label label-important">NOT</span>&nbsp;<b>/channel/</b>.')

    class Meta():
        verbose_name = 'News Item'
        verbose_name_plural = 'News Items'

    def image_tag(self):
        if self.image: 
            return u'<img class="well" src="/site_data/news_img/%s" width=120/>' % os.path.basename(self.image.url)
    image_tag.short_description = 'Preview'
    image_tag.allow_tags = True


class Member(models.Model):
    first_name = models.CharField(max_length=255, verbose_name='First Name')
    last_name = models.CharField(max_length=255, verbose_name='Last Name')
    role = models.CharField(max_length=255, verbose_name='Role / Title', help_text='<i class="icon-user"></i> Shows up as 1<sup>st</sup> field for title.')
    department = models.CharField(max_length=255, blank=True, verbose_name='Department Affiliation', help_text='<i class="icon-bookmark"></i> Shows up as 2<sup>nd</sup> field for title.')
    more_info = models.CharField(max_length=255, blank=True, verbose_name='URL', help_text='<i class="icon-globe"></i> For the "more info" link. Use SoM CAP link.')
    image = models.ImageField(upload_to=get_member_image, blank=True, max_length=255, verbose_name='Avatar Image', help_text='<i class="icon-picture"></i> Displayed as avatar. Use <span class="label label-info">png/jpg</span> format, low resolution (<span class="label label-important">NO</span> larger than <span class="label label-inverse">200x300 72dpi</span>). If empty, default avatar will be used.')
    joint_lab = models.CharField(max_length=255, blank=True, verbose_name='Joint Lab', help_text='<i class="icon-thumbs-up"></i> P.I.\'s name. <span class="label label-important">NO</span> need to add "lab".')
    joint_link = models.CharField(max_length=255, blank=True, verbose_name='Joint Lab URL', help_text='<i class="icon-globe"></i> Link to the joint lab website.')
    description = models.CharField(max_length=255, blank=True, verbose_name='Additional Title', help_text='<i class="icon-pencil"></i> Shows up as a 3<sup>rd</sup> field for title.')

    alumni = models.BooleanField(default=False, verbose_name='Is Alumni?', help_text='<i class="icon-check"></i> Check for alumni members.')
    start_year = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Start Year', help_text='<i class="icon-play"></i> For alumni display only.')
    finish_year = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Finish Year', help_text='<i class="icon-stop"></i> For alumni display only.')

    class Meta():
        verbose_name = 'Member'
        verbose_name_plural = 'Member Management'

    def image_tag(self):
        if self.image: 
            return u'<img class="well" src="/site_data/ppl_img/%s" width=120/>' % os.path.basename(self.image.url)
    image_tag.short_description = 'Preview'
    image_tag.allow_tags = True


class Publication(models.Model):
    authors = models.TextField(help_text='<i class="icon-user"></i> Follow the format seen on the website: <span class="label label-inverse">Das, R.,</span>.')
    year = models.PositiveSmallIntegerField()
    display_date = models.DateField(verbose_name='Display Date', help_text='<i class="icon-random"></i> For display ordering within each year. Assign a virtual date as used when sorting.')
    title = models.TextField(help_text='<i class="icon-bullhorn"></i> Only use upper-case for the first word.')
    journal = models.CharField(max_length=255, blank=True, null=True)
    volume = models.CharField(max_length=31, blank=True, null=True, help_text='<i class="icon-book"></i> Use <span class="label label-inverse">in press, epub available.</span> if not printed yet.')
    issue = models.CharField(max_length=31, blank=True, null=True)
    begin_page = models.CharField(max_length=31, blank=True, null=True, verbose_name='Start Page')
    end_page = models.CharField(max_length=31, blank=True, null=True, verbose_name='End Page')

    pdf = models.FileField(upload_to=get_pub_pdf, blank=True, max_length=255, verbose_name='PDF File', help_text='<i class="icon-file"></i> Shows as <b>"Paper"</b> link. Use file name format <span class="label label-inverse">YEAR_LASTNAME_JOURNAL.pdf</span>: year in 4-digits, first author\'s lat name (no space) and journal name in short form. <span class="label label-success">Example</span>: 2012_Kladwang_NatChem.pdf.')
    preprint = models.BooleanField(default=False, verbose_name='Is Preprint?', help_text='<i class="icon-tag"></i> Check if this publication is the provided link is to ArXiv, meaning with <b>"Preprint"</b> instead of <b>"Paper"</b> link.')
    link = models.CharField(max_length=255, blank=True, verbose_name='URL', help_text='<i class="icon-globe"></i> Shows as <b>"Link"</b> to redirect to journal website.')

    extra_field = models.CharField(max_length=255, blank=True)
    extra_link = models.CharField(max_length=255, blank=True)
    extra_field_2 = models.CharField(max_length=255, blank=True)
    extra_link_2 = models.CharField(max_length=255, blank=True)
    extra_field_3 = models.CharField(max_length=255, blank=True)
    extra_file = models.FileField(upload_to=get_pub_data, blank=True, max_length=255)

    feature = models.BooleanField(default=False, verbose_name='Is Featured?', help_text='<i class="icon-flag"></i> Check if this publication is <b>"featured"</b>, meaning with teal background and thumbnail.')
    image = models.ImageField(upload_to=get_pub_image, blank=True, max_length=255, verbose_name='Feature Image', help_text='<i class="icon-picture"></i> For featured publications only.')

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


