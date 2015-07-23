from django.contrib.auth.models import User
from django.db import models
from django import forms
from django.utils.html import format_html

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
    link = models.CharField(max_length=255, blank=True, verbose_name='URL', help_text='<span class="glyphicon glyphicon-globe"></span>&nbsp;For the "read more" link.')
    image = models.ImageField(upload_to=get_news_image, blank=True, null=True, max_length=255, verbose_name='Display Image', help_text='<span class="glyphicon glyphicon-picture"></span>&nbsp; For non-EteRNA news displayed as thumbnail. Use <span class="label label-info">png/jpg</span> format, low resolution (<span class="label label-danger">NO</span> larger than <span class="label label-inverse">200x300 72dpi</span>).')
    video = models.CharField(max_length=255, blank=True, null=True, verbose_name='YouTube Video Link', help_text='<span class="glyphicon glyphicon-facetime-video"></span>&nbsp;For EteRNA news displayed as thumbnail. <span class="label label-success">Example</span>: <u>https://www.youtube.com<b>/embed/</b>Lp_KozzV5Po</u>; <span class="label label-danger">NOT</span>&nbsp;<b>/channel/</b>.')

    class Meta():
        verbose_name = 'News Item'
        verbose_name_plural = 'News Items'

    def image_tag(self):
        if self.image: 
            return u'<img class="well" src="/site_data/news_img/%s" width=150/>' % os.path.basename(self.image.url)
    image_tag.short_description = 'Preview'
    image_tag.allow_tags = True


class Member(models.Model):
    first_name = models.CharField(max_length=255, verbose_name='First Name')
    last_name = models.CharField(max_length=255, verbose_name='Last Name')
    role = models.CharField(max_length=255, verbose_name='Role / Title', help_text='<span class="glyphicon glyphicon-user"></span>&nbsp; Shows up as 1<sup>st</sup> field for title.')
    department = models.CharField(max_length=255, blank=True, verbose_name='Department Affiliation', help_text='<span class="glyphicon glyphicon-bookmark"></span>&nbsp; Shows up as 2<sup>nd</sup> field for title.')
    more_info = models.CharField(max_length=255, blank=True, null=True, verbose_name='URL', help_text='<span class="glyphicon glyphicon-globe"></span>&nbsp; For the "more info" link. Use SoM CAP link.')
    image = models.ImageField(upload_to=get_member_image, blank=True, max_length=255, verbose_name='Avatar Image', help_text='<span class="glyphicon glyphicon-picture"></span>&nbsp; Displayed as avatar. Use <span class="label label-info">png/jpg</span> format, low resolution (<span class="label label-danger">NO</span> larger than <span class="label label-inverse">200x300 72dpi</span>). If empty, default avatar will be used.')
    joint_lab = models.CharField(max_length=255, blank=True, verbose_name='Joint Lab', help_text='<span class="glyphicon glyphicon-thumbs-up"></span>&nbsp; P.I.\'s name. <span class="label label-danger">NO</span> need to add "lab".')
    joint_link = models.CharField(max_length=255, blank=True, verbose_name='Joint Lab URL', help_text='<span class="glyphicon glyphicon-globe"></span>&nbsp; Link to the joint lab website.')
    description = models.CharField(max_length=255, blank=True, verbose_name='Additional Title', help_text='<span class="glyphicon glyphicon-pencil"></span>&nbsp; Shows up as a 3<sup>rd</sup> field for title.')

    alumni = models.BooleanField(default=False, verbose_name='Is Alumni?', help_text='<span class="glyphicon glyphicon-check"></span>&nbsp; Check for alumni members.')
    start_year = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Start Year', help_text='<span class="glyphicon glyphicon-play"></span>&nbsp; For alumni display only.')
    finish_year = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Finish Year', help_text='<span class="glyphicon glyphicon-stop"></span>&nbsp; For alumni display only.')

    class Meta():
        verbose_name = 'Member'
        verbose_name_plural = 'Member Management'

    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)
    full_name.short_description = 'Full Name'
    full_name.admin_order_field = 'first_name'

    def affiliation(self):
        return '%s @ %s' % (self.role, self.department)
    affiliation.admin_order_field = 'role'

    def year(self): 
        if self.alumni:
            string = '<span class="label label-danger">Alumni</span>'
        else:
            string = '<span class="label label-success">Current</span>'
        if self.finish_year:
            y = self.finish_year
        else:
            y = ''
        return format_html('%s %s-%s' % (string, self.start_year, y))
    year.admin_order_field = 'alumni'

    def image_tag(self):
        if self.image: 
            return u'<img class="well" src="/site_data/ppl_img/%s" width=120/>' % os.path.basename(self.image.url)
    image_tag.short_description = 'Preview'
    image_tag.allow_tags = True


class Publication(models.Model):
    authors = models.TextField(help_text='<span class="glyphicon glyphicon-user"></span>&nbsp; Follow the format seen on the website: <span class="label label-inverse">Das, R.,</span>.')
    year = models.PositiveSmallIntegerField()
    display_date = models.DateField(verbose_name='Display Date', help_text='<span class="glyphicon glyphicon-random"></span>&nbsp; For display ordering within each year. Assign a virtual date as used when sorting.')
    title = models.TextField(help_text='<i class="icon-bullhorn"></i> Do <span class="label label-danger">NOT</span> use "CamelCase / InterCaps / CapWords". Only capitalize the first word.')
    journal = models.CharField(max_length=255, blank=True, null=True, help_text='<span class="glyphicon glyphicon-home"></span>&nbsp; Use journal <span class="label label-danger">full</span> name. Capitalize each word.')
    volume = models.CharField(max_length=31, blank=True, null=True, help_text='<span class="glyphicon glyphicon-book"></span>&nbsp; Use <span class="label label-inverse">in press, epub available.</span> if not printed yet.')
    issue = models.CharField(max_length=31, blank=True, null=True)
    begin_page = models.CharField(max_length=31, blank=True, null=True, verbose_name='Start Page')
    end_page = models.CharField(max_length=31, blank=True, null=True, verbose_name='End Page')

    pdf = models.FileField(upload_to=get_pub_pdf, blank=True, max_length=255, verbose_name='PDF File', help_text='<span class="glyphicon glyphicon-file"></span>&nbsp; Shows as <b>"Paper"</b> link. Use file name format <span class="label label-inverse">YEAR_LASTNAME_JOURNAL.pdf</span>: year in 4-digits, first author\'s lat name (no space) and journal name in short form. <span class="label label-success">Example</span>: 2012_Kladwang_NatChem.pdf.')
    preprint = models.BooleanField(default=False, verbose_name='Is Preprint?', help_text='<span class="glyphicon glyphicon-tag"></span>&nbsp; Check if this publication is the provided link is to ArXiv, meaning with <b>"Preprint"</b> instead of <b>"Paper"</b> link.')
    link = models.CharField(max_length=255, blank=True, verbose_name='URL', help_text='<span class="glyphicon glyphicon-globe"></span>&nbsp; Shows as <b>"Link"</b> to redirect to journal website.')

    extra_field = models.CharField(max_length=255, blank=True, verbose_name='Extra Field #1', help_text='<span class="glyphicon glyphicon-edit"></span>&nbsp; Name for extra field for external link. <span class="label label-success">Example</span>: Server.')
    extra_link = models.CharField(max_length=255, blank=True, verbose_name='Extra Link #1', help_text='<span class="glyphicon glyphicon-globe"></span>&nbsp; Link for extra field for external link.')
    extra_field_2 = models.CharField(max_length=255, blank=True, verbose_name='Extra Field #2', help_text='<span class="glyphicon glyphicon-edit"></span>&nbsp; Name for extra field for external link. <span class="label label-success">Example</span>: Software.')
    extra_link_2 = models.CharField(max_length=255, blank=True, verbose_name='Extra Link #2', help_text='<span class="glyphicon glyphicon-globe"></span>&nbsp; Link for extra field for external link.')
    extra_field_3 = models.CharField(max_length=255, blank=True, verbose_name='Extra Field #3', help_text='<span class="glyphicon glyphicon-edit"></span>&nbsp; Name for extra field for upload file. <span class="label label-success">Example</span>: Data.')
    extra_file = models.FileField(upload_to=get_pub_data, blank=True, max_length=255, verbose_name='Extra File', help_text='<span class="glyphicon glyphicon-file"></span>&nbsp; For extra file on server.')

    feature = models.BooleanField(default=False, verbose_name='Is Featured?', help_text='<span class="glyphicon glyphicon-flag"></span>&nbsp; Check if this publication is <b>"featured"</b>, meaning with teal background and thumbnail.')
    image = models.ImageField(upload_to=get_pub_image, blank=True, max_length=255, verbose_name='Feature Image', help_text='<span class="glyphicon glyphicon-picture"></span>&nbsp; For featured publications only. Use <span class="label label-info">png/jpg</span> format, low resolution (<span class="label label-danger">NO</span> larger than <span class="label label-inverse">200x300 72dpi</span>). Use the <span class="label label-danger">SAME</span> name as <b>pdf</b> file.')

    class Meta():
        verbose_name = 'Publication Entry'
        verbose_name_plural = 'Publication Entries'

    def image_tag(self):
        if self.image: 
            return u'<img class="well" src="/site_data/pub_img/%s" width=150/>' % os.path.basename(self.image.url)
    image_tag.short_description = 'Preview'
    image_tag.allow_tags = True


############################################################################################################################################

class FlashSlide(models.Model):
    date = models.DateField()
    link = models.CharField(max_length=255, blank=True, verbose_name='URL', help_text='<span class="glyphicon glyphicon-globe"></span>&nbsp; Link to Google Doc Slides.')

    class Meta():
        verbose_name = 'Flash Slide'
        verbose_name_plural = 'Flash Slides'


class RotationStudent(models.Model):
    date = models.DateField(verbose_name='Presentation Date')
    full_name = models.CharField(max_length=255, verbose_name='Full Name')
    title = models.CharField(max_length=255, verbose_name='Presentation Title', help_text='<span class="glyphicon glyphicon-bullhorn"></span>&nbsp; Do <span class="label label-danger">NOT</span> use "CamelCase / InterCaps / CapWords". Only capitalize the first word.')
    ppt = models.FileField(upload_to=get_rot_ppt, blank=True, max_length=255, verbose_name='Slides Upload', help_text='<span class="glyphicon glyphicon-film"></span>&nbsp; Link to slides on server. Use file name format <span class="label label-inverse">DATE_FULLNAME.pptx</span>: date in 8-digits(yyyymmdd), full name (no space). <span class="label label-success">Exampe</span>: 20120321_SiqiTian.pptx.')
    data = models.FileField(upload_to=get_rot_data, blank=True, max_length=255, verbose_name='Extra Data', help_text='<span class="glyphicon glyphicon-hdd"></span>&nbsp; Link to extra data file.')

    class Meta():
        verbose_name = 'Rotation Presentation'
        verbose_name_plural = 'Rotation Presentations'


class EternaYoutube(models.Model):
    date = models.DateField(verbose_name='Presentation Date')
    presenter = models.CharField(max_length=255)
    title = models.CharField(max_length=255, verbose_name='Presentation Title', help_text='<span class="glyphicon glyphicon-bullhorn"></span>&nbsp; Do <span class="label label-danger">NOT</span> use "CamelCase / InterCaps / CapWords". Only capitalize the first word.')
    link = models.CharField(max_length=255, blank=True, verbose_name='YouTube URL', help_text='<span class="glyphicon glyphicon-facetime-video"></span>&nbsp; Shows as <b>"Link"</b> to redirect to youtube. <span class="label label-success">Example</span>: <u>https://www.youtube.com/watch?v=Lp_KozzV5Po</u>.')

    class Meta():
        verbose_name = 'EteRNA Open Group Meeting'
        verbose_name_plural = 'EteRNA Open Group Meetings'


class Presentation(models.Model):
    date = models.DateField(verbose_name='Presentation Date')
    presenter = models.CharField(max_length=255)
    title = models.CharField(max_length=255, verbose_name='Presentation Title', help_text='<span class="glyphicon glyphicon-bullhorn"></span>&nbsp; Do <span class="label label-danger">NOT</span> use "CamelCase / InterCaps / CapWords". Only capitalize the first word.')
    ppt = models.FileField(upload_to=get_spe_ppt, blank=True, max_length=255, verbose_name='Slides Upload', help_text='<span class="glyphicon glyphicon-film"></span>&nbsp; Link to slides on server. <span class="label label-danger">NO</span> spaces in file name.')
    link = models.CharField(max_length=255, blank=True, verbose_name='URL', help_text='<span class="glyphicon glyphicon-globe"></span>&nbsp; Link to Google Doc Slides.')

    class Meta():
        verbose_name = 'Archived Presentation'
        verbose_name_plural = 'Archived Presentations'


############################################################################################################################################


WEEKDAY_CHOICES = (
    ('0', 'Sunday'),
    ('1', 'Monday'),
    ('2', 'Tuesday'),
    ('3', 'Wednesday'),
    ('4', 'Thursday'),
    ('5', 'Friday'),
    ('6', 'Saturday'),
)

class BackupForm(forms.Form):
    # is_backup = forms.BooleanField()
    # is_upload = forms.BooleanField()
    time_backup = forms.TimeField(required=True)
    time_upload = forms.TimeField(required=True)
    day_backup = forms.ChoiceField(choices=WEEKDAY_CHOICES)
    day_upload = forms.ChoiceField(choices=WEEKDAY_CHOICES)
    keep = forms.IntegerField()


TEXT_TYPE_CHOICES = (
    (0, ' Plain Text'),
    (1, ' Word Document'),
)

SORT_ORDER_CHOICES = (
    (0, ' Year Ascending'),
    (1, ' Year Descending'),
)

NUMBER_ORDER_CHOICES = (
    (0, ' Incremental'),
    (1, ' Decremental'),
)

class ExportForm(forms.Form):
    text_type = forms.ChoiceField(choices=TEXT_TYPE_CHOICES, widget=forms.RadioSelect(), initial=1)
    year_start = forms.IntegerField(initial=1996)
    sort_order = forms.ChoiceField(choices=SORT_ORDER_CHOICES, widget=forms.RadioSelect(), initial=1)
    number_order = forms.ChoiceField(choices=NUMBER_ORDER_CHOICES, widget=forms.RadioSelect(), initial=1)

    bold_author = forms.BooleanField(initial=True)
    bold_year = forms.BooleanField(initial=True)
    underline_title = forms.BooleanField(initial=True)
    italic_journal = forms.BooleanField(initial=True)
    bold_volume = forms.BooleanField(initial=True)

    order_number = forms.BooleanField(initial=True)
    quote_title = forms.BooleanField(initial=True)
    double_space = forms.BooleanField(initial=False)
    include_preprint = forms.BooleanField(initial=True)






