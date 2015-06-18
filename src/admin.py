from django.contrib import admin
from django.forms import ModelForm, widgets
# from django.contrib.admin import AdminSite

# from suit.widgets import AutosizedTextarea
from suit.widgets import EnclosedInput, SuitDateWidget

from src.models import *

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
        ('Contents', {'fields': ['date', 'content', ('image', 'image_tag')]}),
        ('Links', {'fields': ['link', 'video']}),
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
    list_display = ('alumni', 'first_name', 'last_name', 'role', 'department', 'start_year', 'finish_year')
    form = MemberForm
    readonly_fields = ('image_tag',)

    fieldsets = [
        ('Personal Information', {'fields': [('first_name', 'last_name'), 'role', ('image', 'image_tag'), 'description', 'more_info']}),
        ('Affiliation', {'fields': ['department', ('joint_lab', 'joint_link')]}),
        ('Alumni Information', {'fields': ['alumni', ('start_year', 'finish_year')]}),
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

    fieldsets = [
        ('Citation', {'fields': ['title', ('year', 'display_date'), 'authors', 'journal', ('volume', 'issue'), ('begin_page', 'end_page')]}),
        ('Media', {'fields': ['pdf', 'preprint', 'feature', 'image']}),
        ('Link', {'fields': ['link', 'extra_field', 'extra_link', 'extra_field_2', 'extra_link_2', 'extra_field_3', 'extra_file']}),
    ]
admin.site.register(Publication, PublicationAdmin)


############################################################################################################################################

class FlashSlideAdmin(admin.ModelAdmin):
    list_display = ('date', 'link')

    def get_form(self, request, obj=None, **kwargs):
        form = super(FlashSlideAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['link'].widget.attrs['style'] = 'width: 75em;'
        return form
admin.site.register(FlashSlide, FlashSlideAdmin)

class RotationStudentAdmin(admin.ModelAdmin):
    list_display = ('date', 'full_name', 'title')

    def get_form(self, request, obj=None, **kwargs):
        form = super(RotationStudentAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['title'].widget.attrs['style'] = 'width: 75em;'
        return form
admin.site.register(RotationStudent, RotationStudentAdmin)

class EternaYoutubeAdmin(admin.ModelAdmin):
    list_display = ('date', 'presenter', 'title', 'link')

    def get_form(self, request, obj=None, **kwargs):
        form = super(EternaYoutubeAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['title'].widget.attrs['style'] = 'width: 75em;'
        form.base_fields['link'].widget.attrs['style'] = 'width: 75em;'
        return form
admin.site.register(EternaYoutube, EternaYoutubeAdmin)

class PresentationAdmin(admin.ModelAdmin):
    list_display = ('date', 'presenter', 'title')

    def get_form(self, request, obj=None, **kwargs):
        form = super(PresentationAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['presenter'].widget.attrs['style'] = 'width: 75em;'
        form.base_fields['title'].widget.attrs['style'] = 'width: 75em;'
        form.base_fields['link'].widget.attrs['style'] = 'width: 75em;'
        return form
admin.site.register(Presentation, PresentationAdmin)


