from django.db import models
from django import forms
from django.utils.html import format_html
from django.utils.timezone import now

from src.settings import *

import os


def get_member_image(instance, filename):
    name = instance.first_name.strip() + instance.last_name[0].strip()
    ext = filename[filename.rfind('.'):]
    filename = PATH.DATA_DIR['MEMBER_IMG_DIR'] + '%s%s' % (name, ext)
    if os.path.exists(filename):
        os.remove(filename)
    return filename

def get_pub_pdf(instance, filename):
    filename = PATH.DATA_DIR['PUB_PDF_DIR'] + '%s' % filename
    if os.path.exists(filename):
        os.remove(filename)
    return filename

def get_pub_image(instance, filename):
    filename = PATH.DATA_DIR['PUB_IMG_DIR'] + '%s' % filename
    if os.path.exists(filename):
        os.remove(filename)
    return filename

def get_pub_data(instance, filename):
    filename = PATH.DATA_DIR['PUB_DAT_DIR'] + '%s' % filename
    if os.path.exists(filename):
        os.remove(filename)
    return filename

def get_news_image(instance, filename):
    filename = PATH.DATA_DIR['NEWS_IMG_DIR'] + '%s' % filename
    if os.path.exists(filename):
        os.remove(filename)
    return filename

def get_rot_ppt(instance, filename):
    name = instance.date.strftime('%Y%m%d') + '_' + instance.full_name.replace(' ', '')
    ext = filename[filename.rfind('.'):]
    filename = PATH.DATA_DIR['ROT_PPT_DIR'] + '%s%s' % (name, ext)
    if os.path.exists(filename):
        os.remove(filename)
    return filename

def get_rot_data(instance, filename):
    name = instance.date.strftime('%Y%m%d') + '_' + instance.full_name.replace(' ', '')
    ext = filename[filename.rfind('.'):]
    filename = PATH.DATA_DIR['ROT_DAT_DIR'] + '%s%s' % (name, ext)
    if os.path.exists(filename):
        os.remove(filename)
    return filename

def get_spe_ppt(instance, filename):
    filename = PATH.DATA_DIR['SPE_PPT_DIR'] + '%s' % filename
    if os.path.exists(filename):
        os.remove(filename)
    return filename

def get_def_image(instance, filename):
    name = instance.date.strftime('%Y%m%d') + '_' + instance.presenter.replace(' ', '')
    ext = filename[filename.rfind('.'):]
    filename = PATH.DATA_DIR['DEF_IMG_DIR'] + '%s%s' % (name, ext)
    if os.path.exists(filename):
        os.remove(filename)
    return filename


class News(models.Model):
    date = models.DateField(verbose_name='Display Date')
    content = models.TextField(
        blank=True,
        verbose_name='Main Text Content',
        help_text='<span class="glyphicon glyphicon-edit"></span>&nbsp;HTML supported.')
    link = models.URLField(
        max_length=255, blank=True,
        verbose_name='URL',
        help_text='<span class="glyphicon glyphicon-globe"></span>&nbsp;For the "read more" link.')
    image = models.ImageField(
        upload_to=get_news_image,
        max_length=255, blank=True, null=True,
        verbose_name='Display Image',
        help_text='<span class="glyphicon glyphicon-picture"></span>&nbsp; For non-EteRNA news displayed as thumbnail. Use <span class="label label-info">png/jpg</span> format, low resolution (<span class="label label-danger">NO</span> larger than <span class="label label-inverse">200x300 72dpi</span>).')
    video = models.CharField(
        max_length=12, blank=True, null=True,
        verbose_name='YouTube Video ID',
        help_text='<span class="glyphicon glyphicon-facetime-video"></span>&nbsp;For EteRNA news displayed as thumbnail. <span class="label label-success">Example</span>: <u>Lp_KozzV5Po</u>; ID only, <span class="label label-danger">NOT</span>&nbsp;<b>URL</b>.')
    is_visible = models.BooleanField(
        default=True,
        verbose_name='Is Visible?',
        help_text='<span class="glyphicon glyphicon-check"></span>&nbsp; Uncheck to hide from public site.')

    class Meta():
        verbose_name = 'News Item'
        verbose_name_plural = 'News Items'

    def image_tag(self):
        if self.image:
            return u'<img class="well" src="/site_data/news_img/%s" width=150/>' % os.path.basename(self.image.url)
    image_tag.short_description = 'Preview'
    image_tag.allow_tags = True


class Member(models.Model):
    first_name = models.CharField(
        max_length=255,
        verbose_name='First Name')
    last_name = models.CharField(
        max_length=255,
        verbose_name='Last Name')
    role = models.CharField(
        max_length=255,
        verbose_name='Role / Title',
        help_text='<span class="glyphicon glyphicon-user"></span>&nbsp; Shows up as 1<sup>st</sup> field for title.')
    department = models.CharField(
        max_length=255, blank=True,
        verbose_name='Department Affiliation',
        help_text='<span class="glyphicon glyphicon-bookmark"></span>&nbsp; Shows up as 2<sup>nd</sup> field for title.')
    more_info = models.CharField(
        max_length=255, blank=True, null=True,
        verbose_name='URL',
        help_text='<span class="glyphicon glyphicon-globe"></span>&nbsp; For the "more info" link. Use SoM CAP link.')
    image = models.ImageField(
        upload_to=get_member_image,
        max_length=255, blank=True,
        verbose_name='Avatar Image',
        help_text='<span class="glyphicon glyphicon-picture"></span>&nbsp; Displayed as avatar. Use <span class="label label-info">png/jpg</span> format, low resolution (<span class="label label-danger">NO</span> larger than <span class="label label-inverse">200x300 72dpi</span>). If empty, default avatar will be used.')
    joint_lab = models.CharField(
        max_length=255, blank=True,
        verbose_name='Joint Lab',
        help_text='<span class="glyphicon glyphicon-thumbs-up"></span>&nbsp; P.I.\'s name. <span class="label label-danger">NO</span> need to add "lab".')
    joint_link = models.URLField(
        max_length=255, blank=True,
        verbose_name='Joint Lab URL',
        help_text='<span class="glyphicon glyphicon-globe"></span>&nbsp; Link to the joint lab website.')
    description = models.CharField(
        max_length=255, blank=True,
        verbose_name='Additional Title',
        help_text='<span class="glyphicon glyphicon-pencil"></span>&nbsp; Shows up as a 3<sup>rd</sup> field for title.')

    email = models.EmailField(
        max_length=255, blank=True,
        verbose_name='Email')
    phone = models.BigIntegerField(
        blank=True,
        verbose_name='Phone Number',
        help_text='<span class="glyphicon glyphicon-phone"></span>&nbsp; Cell phone number.')
    sunet_id = models.CharField(
        max_length=31, blank=True,
        verbose_name='SUNet ID',
        help_text='<span class="glyphicon glyphicon-credit-card"></span>&nbsp; SUNet ID login to match WebAuth.')
    bday = models.CharField(
        max_length=5, blank=True,
        verbose_name='Birthday',
        help_text='<span class="glyphicon glyphicon-gift"></span>&nbsp; Birthday, in the format of <span class="label label-inverse">mm/dd</span>. <span class="label label-success">Example</span>: "<b>04/19</b>".')
    is_visible = models.BooleanField(
        default=True,
        verbose_name='Is Visible?',
        help_text='<span class="glyphicon glyphicon-check"></span>&nbsp; Uncheck to hide from public site.')

    is_alumni = models.BooleanField(
        default=False,
        verbose_name='Is Alumni?',
        help_text='<span class="glyphicon glyphicon-check"></span>&nbsp; Check for alumni members.')
    start_year = models.PositiveSmallIntegerField(
        default=now().year, blank=True, null=True,
        verbose_name='Start Year',
        help_text='<span class="glyphicon glyphicon-play"></span>&nbsp; For alumni display only.')
    finish_year = models.PositiveSmallIntegerField(
        blank=True, null=True,
        verbose_name='Finish Year',
        help_text='<span class="glyphicon glyphicon-stop"></span>&nbsp; For alumni display only.')

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
        if self.is_alumni:
            string = '<span class="label label-danger">Alumni</span>'
        else:
            string = '<span class="label label-success">Current</span>'
        if self.finish_year:
            y = self.finish_year
        else:
            y = ''
        return format_html('%s %s-%s' % (string, self.start_year, y))
    year.admin_order_field = 'is_alumni'

    def image_tag(self):
        if self.image:
            return u'<img class="thumbnail" src="/site_data/ppl_img/%s" width=120/>' % os.path.basename(self.image.url)
    image_tag.short_description = 'Preview'
    image_tag.allow_tags = True


class Publication(models.Model):
    authors = models.TextField(
        help_text='<span class="glyphicon glyphicon-user"></span>&nbsp; Follow the format seen on the website: <span class="label label-inverse">Das, R.,</span>.')
    year = models.PositiveSmallIntegerField(default=now().year)
    display_date = models.DateField(
        default=now().date(),
        verbose_name='Display Date',
        help_text='<span class="glyphicon glyphicon-random"></span>&nbsp; For display ordering within each year. Assign a virtual date as used when sorting.')
    title = models.TextField(
        help_text='<i class="icon-bullhorn"></i> Do <span class="label label-danger">NOT</span> use "CamelCase / InterCaps / CapWords". Only capitalize the first word.')
    journal = models.CharField(
        max_length=255, blank=True, null=True,
        help_text='<span class="glyphicon glyphicon-home"></span>&nbsp; Use journal <span class="label label-danger">full</span> name. Capitalize each word.')
    volume = models.CharField(
        max_length=31, blank=True, null=True,
        help_text='<span class="glyphicon glyphicon-book"></span>&nbsp; Use <span class="label label-inverse">in press, epub available.</span> if not printed yet.')
    issue = models.CharField(max_length=31, blank=True, null=True)
    begin_page = models.CharField(
        max_length=31, blank=True, null=True,
        verbose_name='Start Page')
    end_page = models.CharField(
        max_length=31, blank=True, null=True,
        verbose_name='End Page')

    pdf = models.FileField(
        upload_to=get_pub_pdf,
        max_length=255, blank=True,
        verbose_name='PDF File',
        help_text='<span class="glyphicon glyphicon-file"></span>&nbsp; Shows as <b>"Paper"</b> link. Use file name format <span class="label label-inverse">YEAR_LASTNAME_JOURNAL.pdf</span>: year in 4-digits, first author\'s lat name (no space) and journal name in short form. <span class="label label-success">Example</span>: 2012_Kladwang_NatChem.pdf.')
    is_preprint = models.BooleanField(
        default=False,
        verbose_name='Is Preprint?',
        help_text='<span class="glyphicon glyphicon-tag"></span>&nbsp; Check if this publication is the provided link is to ArXiv, meaning with <b>"Preprint"</b> instead of <b>"Paper"</b> link.')
    is_visible = models.BooleanField(
        default=True,
        verbose_name='Is Visible?',
        help_text='<span class="glyphicon glyphicon-eye-close"></span>&nbsp; Check if this publication is displayed in the public site.')
    link = models.URLField(
        max_length=255, blank=True,
        verbose_name='URL',
        help_text='<span class="glyphicon glyphicon-globe"></span>&nbsp; Shows as <b>"Link"</b> to redirect to journal website.')

    extra_field = models.CharField(
        max_length=255, blank=True,
        verbose_name='Extra Field #1',
        help_text='<span class="glyphicon glyphicon-edit"></span>&nbsp; Name for extra field for external link. <span class="label label-success">Example</span>: Server.')
    extra_link = models.URLField(
        max_length=255, blank=True,
        verbose_name='Extra Link #1',
        help_text='<span class="glyphicon glyphicon-globe"></span>&nbsp; Link for extra field for external link.')
    extra_field_2 = models.CharField(
        max_length=255, blank=True,
        verbose_name='Extra Field #2',
        help_text='<span class="glyphicon glyphicon-edit"></span>&nbsp; Name for extra field for external link. <span class="label label-success">Example</span>: Software.')
    extra_link_2 = models.URLField(
        max_length=255, blank=True,
        verbose_name='Extra Link #2',
        help_text='<span class="glyphicon glyphicon-globe"></span>&nbsp; Link for extra field for external link.')
    extra_field_3 = models.CharField(
        max_length=255, blank=True,
        verbose_name='Extra Field #3',
        help_text='<span class="glyphicon glyphicon-edit"></span>&nbsp; Name for extra field for upload file. <span class="label label-success">Example</span>: Data.')
    extra_file = models.FileField(
        upload_to=get_pub_data,
        max_length=255, blank=True,
        verbose_name='Extra File',
        help_text='<span class="glyphicon glyphicon-file"></span>&nbsp; For extra file on server.')

    is_feature = models.BooleanField(
        default=False,
        verbose_name='Is Featured?',
        help_text='<span class="glyphicon glyphicon-flag"></span>&nbsp; Check if this publication is <b>"featured"</b>, meaning with teal background and thumbnail.')
    image = models.ImageField(
        upload_to=get_pub_image,
        max_length=255, blank=True,
        verbose_name='Feature Image',
        help_text='<span class="glyphicon glyphicon-picture"></span>&nbsp; For featured publications only. Use <span class="label label-info">png/jpg</span> format, low resolution (<span class="label label-danger">NO</span> larger than <span class="label label-inverse">200x300 72dpi</span>). Use the <span class="label label-danger">SAME</span> name as <b>pdf</b> file.')

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
    date = models.DateField(default=now())
    link = models.URLField(
        max_length=255, blank=True,
        verbose_name='URL',
        help_text='<span class="glyphicon glyphicon-globe"></span>&nbsp; Link to Google Doc Slides.')

    class Meta():
        verbose_name = 'Flash Slide'
        verbose_name_plural = 'Flash Slides'


class JournalClub(models.Model):
    date = models.DateField(default=now())
    presenter = models.CharField(max_length=255)
    authors = models.CharField(
        max_length=255, blank=True,
        help_text='<span class="glyphicon glyphicon-user"></span>&nbsp; Abbreviated first author last name only: <span class="label label-inverse">Das</span>.')
    year = models.PositiveSmallIntegerField()
    title = models.TextField(
        blank=True,
        help_text='<i class="icon-bullhorn"></i> Do <span class="label label-danger">NOT</span> use "CamelCase / InterCaps / CapWords". Only capitalize the first word.')
    citation = models.CharField(
        max_length=255, blank=True, null=True,
        help_text='Journal, Volume, Issue, and Pages.')
    link = models.URLField(
        max_length=255,
        verbose_name='URL',
        help_text='<span class="glyphicon glyphicon-globe"></span>&nbsp; Shows as <b>"Link"</b> to redirect to journal website.')

    class Meta():
        verbose_name = 'Journal Club'
        verbose_name_plural = 'Journal Clubs'


class RotationStudent(models.Model):
    date = models.DateField(
        default=now(),
        verbose_name='Presentation Date')
    full_name = models.CharField(
        max_length=255,
        verbose_name='Student')
    title = models.CharField(
        max_length=255,
        verbose_name='Presentation Title',
        help_text='<span class="glyphicon glyphicon-bullhorn"></span>&nbsp; Do <span class="label label-danger">NOT</span> use "CamelCase / InterCaps / CapWords". Only capitalize the first word.')
    ppt = models.FileField(
        upload_to=get_rot_ppt,
        max_length=255, blank=True,
        verbose_name='Slides Upload',
        help_text='<span class="glyphicon glyphicon-film"></span>&nbsp; Link to slides on server. Use file name format <span class="label label-inverse">DATE_FULLNAME.pptx</span>: date in 8-digits(yyyymmdd), full name (no space). <span class="label label-success">Example</span>: 20120321_SiqiTian.pptx.')
    data = models.FileField(
        upload_to=get_rot_data,
        max_length=255, blank=True,
        verbose_name='Extra Data', help_text='<span class="glyphicon glyphicon-hdd"></span>&nbsp; Link to extra data file.')

    class Meta():
        verbose_name = 'Rotation Presentation'
        verbose_name_plural = 'Rotation Presentations'


class EternaYoutube(models.Model):
    date = models.DateField(
        default=now(),
        verbose_name='Presentation Date')
    presenter = models.CharField(max_length=255)
    title = models.CharField(
        max_length=255,
        verbose_name='Presentation Title',
        help_text='<span class="glyphicon glyphicon-bullhorn"></span>&nbsp; Do <span class="label label-danger">NOT</span> use "CamelCase / InterCaps / CapWords". Only capitalize the first word.')
    link = models.URLField(
        max_length=255, blank=True,
        verbose_name='YouTube URL',
        help_text='<span class="glyphicon glyphicon-facetime-video"></span>&nbsp; Shows as <b>"Link"</b> to redirect to youtube. <span class="label label-success">Example</span>: <u>https://www.youtube.com/watch?v=Lp_KozzV5Po</u>.')

    class Meta():
        verbose_name = 'EteRNA Open Group Meeting'
        verbose_name_plural = 'EteRNA Open Group Meetings'


class Presentation(models.Model):
    date = models.DateField(
        default=now(),
        verbose_name='Presentation Date')
    presenter = models.CharField(max_length=255)
    title = models.CharField(
        max_length=255,
        verbose_name='Presentation Title',
        help_text='<span class="glyphicon glyphicon-bullhorn"></span>&nbsp; Do <span class="label label-danger">NOT</span> use "CamelCase / InterCaps / CapWords". Only capitalize the first word.')
    ppt = models.FileField(
        upload_to=get_spe_ppt,
        max_length=255, blank=True,
        verbose_name='Slides Upload', help_text='<span class="glyphicon glyphicon-film"></span>&nbsp; Link to slides on server. <span class="label label-danger">NO</span> spaces in file name.')
    link = models.URLField(
        max_length=255, blank=True,
        verbose_name='URL',
        help_text='<span class="glyphicon glyphicon-globe"></span>&nbsp; Link to Google Doc Slides.')

    class Meta():
        verbose_name = 'Archived Presentation'
        verbose_name_plural = 'Archived Presentations'


class DefensePoster(models.Model):
    date = models.DateField(verbose_name='Defense Date')
    presenter = models.CharField(
        max_length=255,
        verbose_name='Student')
    title = models.CharField(
        max_length=255,
        verbose_name='Presentation Title',
        help_text='<span class="glyphicon glyphicon-bullhorn"></span>&nbsp; Do <span class="label label-danger">NOT</span> use "CamelCase / InterCaps / CapWords". Only capitalize the first word.')
    image = models.ImageField(
        upload_to=get_def_image,
        max_length=255, blank=True,
        verbose_name='Poster Image',
        help_text='<span class="glyphicon glyphicon-film"></span>&nbsp; Link to poster on server. <span class="label label-danger">NO</span> spaces in file name.')

    class Meta():
        verbose_name = 'Defense Poster'
        verbose_name_plural = 'Defense Posters'

    def image_tag(self):
        if self.image:
            return u'<img class="thumbnail" src="/site_data/def_img/%s" width=120/>' % os.path.basename(self.image.url)
    image_tag.short_description = 'Preview'
    image_tag.allow_tags = True


class SlackMessage(models.Model):
    date = models.DateField(
        default=now(),
        verbose_name='Message Date')
    receiver = models.CharField(max_length=255)
    content = models.TextField(
        help_text='<span class="glyphicon glyphicon-comment"></span>&nbsp;Main text of message</span>.')
    attachment = models.TextField(
        help_text='<span class="glyphicon glyphicon-compressed"></span>&nbsp;Attachment JSON (multi-media) of message.')

    def message(self):
        return '%s @ %s' % (self.content, self.attachment)
    message.admin_order_field = 'attachment'

    class Meta():
        verbose_name = 'Slack Message'
        verbose_name_plural = 'Slack Messages'


############################################################################################################################################


WEEKDAY_CHOICES = (
    ('', '------'),
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
    day_backup = forms.ChoiceField(choices=WEEKDAY_CHOICES, required=True)
    day_upload = forms.ChoiceField(choices=WEEKDAY_CHOICES, required=True)
    keep = forms.IntegerField(required=True)


TEXT_TYPE_CHOICES = (
    ('0', '(TXT) Plain Text '),
    ('1', '(DOCX) Word Document '),
)

SORT_ORDER_CHOICES = (
    ('0', ' ASC '),
    ('1', ' DESC '),
)

NUMBER_ORDER_CHOICES = (
    ('0', ' ASC '),
    ('1', ' DESC '),
)

class ExportForm(forms.Form):
    text_type = forms.ChoiceField(choices=TEXT_TYPE_CHOICES, initial=1, required=True)
    year_start = forms.IntegerField(initial=1996, required=True)
    sort_order = forms.ChoiceField(choices=SORT_ORDER_CHOICES, initial=1, required=True)
    number_order = forms.ChoiceField(choices=NUMBER_ORDER_CHOICES, initial=1, required=True)

    bold_author = forms.BooleanField(initial=True, required=False)
    bold_year = forms.BooleanField(initial=True, required=False)
    underline_title = forms.BooleanField(initial=True, required=False)
    italic_journal = forms.BooleanField(initial=True, required=False)
    bold_volume = forms.BooleanField(initial=True, required=False)

    order_number = forms.BooleanField(initial=True, required=False)
    quote_title = forms.BooleanField(initial=True, required=False)
    double_space = forms.BooleanField(initial=False, required=False)
    include_preprint = forms.BooleanField(initial=True, required=False)
    include_hidden = forms.BooleanField(initial=False, required=False)


REMINDER_1_CHOICES = (
    ('', '---'),
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
)

REMINDER_2_CHOICES = (
    ('', '---'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
)

CACHE_3 = (
    ('', '---'),
    ('2', '2'),
    ('3', '3'),
    ('5', '5'),
    ('10', '10'),
)

CACHE_15 = (
    ('', '---'),
    ('10', '10'),
    ('15', '15'),
    ('20', '20'),
    ('30', '30'),
)

CACHE_30 = (
    ('', '---'),
    ('30', '30'),
    ('60', '60'),
)

class BotSettingForm(forms.Form):
    is_slack = forms.BooleanField(initial=True, required=False)
    is_cache = forms.BooleanField(initial=True, required=False)

    is_duty_bday = forms.BooleanField(initial=True, required=False)
    is_duty_breakfast = forms.BooleanField(initial=True, required=False)
    is_duty_aws = forms.BooleanField(initial=True, required=False)
    is_duty_schedule = forms.BooleanField(initial=True, required=False)
    is_duty_website = forms.BooleanField(initial=True, required=False)
    is_duty_trip = forms.BooleanField(initial=True, required=False)
    is_duty_git = forms.BooleanField(initial=True, required=False)

    is_admin_backup = forms.BooleanField(initial=True, required=False)
    is_admin_gdrive = forms.BooleanField(initial=True, required=False)
    is_admin_version = forms.BooleanField(initial=True, required=False)
    is_admin_report = forms.BooleanField(initial=True, required=False)
    is_admin_aws_warn = forms.BooleanField(initial=True, required=False)

    is_bday = forms.BooleanField(initial=True, required=False)
    is_flash_slide = forms.BooleanField(initial=True, required=False)
    is_version = forms.BooleanField(initial=True, required=False)
    is_report = forms.BooleanField(initial=True, required=False)

    is_user_jc_1 = forms.BooleanField(initial=True, required=False)
    is_user_jc_2 = forms.BooleanField(initial=True, required=False)
    is_admin_jc = forms.BooleanField(initial=True, required=False)
    is_user_es_1 = forms.BooleanField(initial=True, required=False)
    is_user_es_2 = forms.BooleanField(initial=True, required=False)
    is_admin_es = forms.BooleanField(initial=True, required=False)
    is_user_rot_1 = forms.BooleanField(initial=True, required=False)
    is_user_rot_2 = forms.BooleanField(initial=True, required=False)
    is_admin_rot = forms.BooleanField(initial=True, required=False)

    is_duty_mic = forms.BooleanField(initial=True, required=False)
    is_duty_broadcast = forms.BooleanField(initial=True, required=False)
    is_duty_webnews = forms.BooleanField(initial=True, required=False)

    day_duty_month = forms.ChoiceField(choices=WEEKDAY_CHOICES, required=True)
    day_duty_quarter = forms.ChoiceField(choices=WEEKDAY_CHOICES, required=True)
    day_meeting = forms.ChoiceField(choices=WEEKDAY_CHOICES, required=False)
    day_reminder_1 = forms.ChoiceField(choices=REMINDER_1_CHOICES, required=True)
    day_reminder_2 = forms.ChoiceField(choices=REMINDER_2_CHOICES, required=True)

    cache_3 = forms.ChoiceField(choices=CACHE_3, required=True)
    cache_15 = forms.ChoiceField(choices=CACHE_15, required=True)
    cache_30 = forms.ChoiceField(choices=CACHE_30, required=True)

class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput)
    flag = forms.CharField(required=True)

class PasswordForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    password_old = forms.CharField(required=True, widget=forms.PasswordInput)
    password_new = forms.CharField(required=True, widget=forms.PasswordInput)
    password_new_rep = forms.CharField(required=True, widget=forms.PasswordInput)


class UploadForm(forms.Form):
    upload_date = forms.DateField(required=True)
    upload_presenter = forms.CharField(required=True)
    upload_title = forms.CharField(required=True)
    upload_file = forms.FileField(required=True)
    upload_link = forms.CharField(required=False)

class ContactForm(forms.Form):
    contact_phone = forms.IntegerField(required=True)
    contact_email = forms.EmailField(required=True)
    contact_bday = forms.CharField(required=True)

class EmailForm(forms.Form):
    email_from = forms.EmailField(required=True)
    email_subject = forms.CharField(required=True)
    email_content = forms.CharField(widget=forms.Textarea, required=True)


def email_form(request):
    return {'email_form': EmailForm()}

def debug_flag(request):
    if DEBUG:
        return {
            'DEBUG_STR': '',
            'DEBUG_DIR': '',
        }
    else:
        return {
            'DEBUG_STR': '.min',
            'DEBUG_DIR': 'min/',
        }

def ga_tracker(request):
    return {'TRACKING_ID': GA['TRACKING_ID']}

def js_ver(request):
    stats = simplejson.load(open('%s/cache/stat_ver.json' % MEDIA_ROOT, 'r'))
    json = {
        field: stats[field]
        for field in ['jquery', 'bootstrap', 'fullcal', 'moment']
    }
    return {
        'js_ver': {
            str(k):str(v)
            for (k, v) in json.items()
        }
    }
