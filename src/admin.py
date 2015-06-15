from django.contrib import admin
from django.contrib.admin import AdminSite

from src.models import *
# from .models import MyModel
# from src.settings import PATH

# class MyAdminSite(AdminSite):
#     login_template = PATH.HTML_PATH['login']
#     site_header = 'Das Lab Website Administration'

# admin_site = MyAdminSite(name='myadmin')
# admin_site.register(MyModel)

class NewsAdmin(admin.ModelAdmin):
    list_display = ('date', 'content', 'link')

    def get_form(self, request, obj=None, **kwargs):
        form = super(NewsAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['content'].widget.attrs['style'] = 'width: 75em; height: 8em;'
        form.base_fields['link'].widget.attrs['style'] = 'width: 75em;'
        return form
admin.site.register(News, NewsAdmin)

class MemberAdmin(admin.ModelAdmin):
    list_display = ('alumni', 'first_name', 'last_name', 'role', 'department', 'start_year', 'finish_year')
admin.site.register(Member, MemberAdmin)

class PublicationAdmin(admin.ModelAdmin):
    list_display = ('year', 'journal', 'authors', 'title', 'link')

    def get_form(self, request, obj=None, **kwargs):
        form = super(PublicationAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['authors'].widget.attrs['style'] = 'width: 75em; height: 8em;'
        form.base_fields['title'].widget.attrs['style'] = 'width: 75em; height: 5em;'
        form.base_fields['journal'].widget.attrs['style'] = 'width: 75em;'
        form.base_fields['link'].widget.attrs['style'] = 'width: 75em;'
        form.base_fields['extra_link'].widget.attrs['style'] = 'width: 75em;'
        form.base_fields['extra_link_2'].widget.attrs['style'] = 'width: 75em;'
        form.base_fields['image'].widget.attrs['style'] = 'width: 75em;'
        return form    
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


