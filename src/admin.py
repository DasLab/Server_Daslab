from django.contrib import admin
from django.forms import ModelForm, widgets
from django.utils.html import format_html
from django.shortcuts import render_to_response
from django.template import RequestContext
# from django.contrib.admin import AdminSite

# from suit.widgets import AutosizedTextarea
from suit.widgets import EnclosedInput, SuitDateWidget

from src.models import *
from src.settings import PATH


class NewsForm(ModelForm):
    class Meta:
        widgets = {
            'date': SuitDateWidget,
            'content': widgets.Textarea(attrs={'style':'width: 90%','rows':'6' }),
            'link': widgets.TextInput(attrs={'style':'width: 90%' }),
            # 'link': EnclosedInput(prepend='icon-user', attrs={'style':'width: 90%' }),
            'video': widgets.TextInput(attrs={'style':'width: 90%' }),
        }

class NewsAdmin(admin.ModelAdmin):
    list_display = ('date', 'content', 'link')
    form = NewsForm
    readonly_fields = ('image_tag',)

    fieldsets = [
        (format_html('<i class="icon-comment"></i> Contents'), {'fields': ['date', 'content', ('image', 'image_tag')]}),
        (format_html('<i class="icon-share"></i> Links'), {'fields': ['link', 'video']}),
    ]
admin.site.register(News, NewsAdmin)


class MemberForm(ModelForm):
    class Meta:
        widgets = {
            'role': widgets.TextInput(attrs={'style':'width: 90%' }),
            'more_info': widgets.TextInput(attrs={'style':'width: 90%' }),
            'description': widgets.TextInput(attrs={'style':'width: 90%' }),
            'department': widgets.TextInput(attrs={'style':'width: 90%' }),
        }

class MemberAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'year', 'joint_lab', 'affiliation')
    form = MemberForm
    readonly_fields = ('image_tag',)

    fieldsets = [
        (format_html('<i class="icon-user"></i> Personal Information'), {'fields': [('first_name', 'last_name'), 'role', ('image', 'image_tag'), 'description', 'more_info']}),
        (format_html('<i class="icon-home"></i> Affiliation'), {'fields': ['department', ('joint_lab', 'joint_link')]}),
        (format_html('<i class="icon-road"></i> Alumni Information'), {'fields': ['alumni', ('start_year', 'finish_year')]}),
    ]
admin.site.register(Member, MemberAdmin)


class PublicationForm(ModelForm):
    class Meta:
        widgets = {
            'display_date': SuitDateWidget,
            'authors': widgets.Textarea(attrs={'style':'width: 90%','rows':'4' }),
            'title': widgets.Textarea(attrs={'style':'width: 90%','rows':'4' }),
            'journal': widgets.TextInput(attrs={'style':'width: 90%' }),
            'link': widgets.TextInput(attrs={'style':'width: 90%' }),
            'extra_link': widgets.TextInput(attrs={'style':'width: 90%' }),
            'extra_link_2': widgets.TextInput(attrs={'style':'width: 90%' }),
        }

class PublicationAdmin(admin.ModelAdmin):
    list_display = ('year', 'journal', 'authors', 'title', 'link')
    form = PublicationForm
    readonly_fields = ('image_tag',)

    fieldsets = [
        (format_html('<i class="icon-book"></i> Citation'), {'fields': ['title', ('year', 'display_date'), 'authors', 'journal', ('volume', 'issue'), ('begin_page', 'end_page')]}),
        (format_html('<i class="icon-th-large"></i> Media'), {'fields': ['pdf', 'preprint', 'feature', ('image', 'image_tag')]}),
        (format_html('<i class="icon-share"></i> Links'), {'fields': ['link', 'extra_field', 'extra_link', 'extra_field_2', 'extra_link_2', 'extra_field_3', 'extra_file']}),
    ]
admin.site.register(Publication, PublicationAdmin)


############################################################################################################################################

class FlashSlideForm(ModelForm):
    class Meta:
        widgets = {
            'date': SuitDateWidget,
            'link': widgets.TextInput(attrs={'style':'width: 90%' }),
        }

class FlashSlideAdmin(admin.ModelAdmin):
    list_display = ('date', 'link')
    form = FlashSlideForm

    fieldsets = [
        (format_html('<i class="icon-share"></i> Links'), {'fields': ['date', 'link']}),
    ]
admin.site.register(FlashSlide, FlashSlideAdmin)


class RotationStudentForm(ModelForm):
    class Meta:
        widgets = {
            'date': SuitDateWidget,
            'title': widgets.TextInput(attrs={'style':'width: 90%' }),
        }

class RotationStudentAdmin(admin.ModelAdmin):
    list_display = ('date', 'full_name', 'title')
    form = RotationStudentForm

    fieldsets = [
        (format_html('<i class="icon-user"></i> Personal Information'), {'fields': ['date', 'full_name', 'title']}),
        (format_html('<i class="icon-share"></i> Links'), {'fields': ['ppt', 'data']}),
    ]
admin.site.register(RotationStudent, RotationStudentAdmin)


class EternaYoutubeForm(ModelForm):
    class Meta:
        widgets = {
            'date': SuitDateWidget,
            'link': widgets.TextInput(attrs={'style':'width: 90%' }),
            'title': widgets.TextInput(attrs={'style':'width: 90%' }),
        }

class EternaYoutubeAdmin(admin.ModelAdmin):
    list_display = ('date', 'presenter', 'title', 'link')
    form = EternaYoutubeForm

    fieldsets = [
        (format_html('<i class="icon-share"></i> Links'), {'fields': ['date', 'presenter', 'title', 'link']}),
    ]
admin.site.register(EternaYoutube, EternaYoutubeAdmin)


class PresentationForm(ModelForm):
    class Meta:
        widgets = {
            'date': SuitDateWidget,
            'link': widgets.TextInput(attrs={'style':'width: 90%' }),
            'title': widgets.TextInput(attrs={'style':'width: 90%' }),
        }

class PresentationAdmin(admin.ModelAdmin):
    list_display = ('date', 'presenter', 'title')
    form = PresentationForm

    fieldsets = [
        (format_html('<i class="icon-share"></i> Links'), {'fields': ['date', 'presenter', 'title', 'ppt', 'link']}),
    ]
admin.site.register(Presentation, PresentationAdmin)


############################################################################################################################################

def apache(request):
    return render_to_response(PATH.HTML_PATH['admin_apache'], {}, context_instance=RequestContext(request))
admin.site.register_view('apache', view=apache, visible=False)

def dashboard(request):
    return render_to_response(PATH.HTML_PATH['admin_dash'], {}, context_instance=RequestContext(request))
admin.site.register_view('dashboard', view=dashboard, visible=False)

def doc(request):
    return render_to_response(PATH.HTML_PATH['admin_doc'], {}, context_instance=RequestContext(request))
admin.site.register_view('doc', view=doc, visible=False)


