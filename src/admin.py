from src.models import *
from django.contrib import admin

# class ConstructInLine(admin.StackedInline):
#     model = ConstructSection
#     extra = 0

# class EntryAnnotationInLine(admin.TabularInline):
#     model = EntryAnnotation
#     extra = 1

# class EntryAdmin(admin.ModelAdmin):
#     inlines = [EntryAnnotationInLine, ConstructInLine]
#     list_display = ('id', 'rmdb_id', 'version', 'short_description', 'revision_status')

# class PublicationAdmin(admin.ModelAdmin):
#     list_display = ('pubmed_id', 'title', 'authors')

# class OrganismAdmin(admin.ModelAdmin):
#     list_display = ('taxonomy_id', 'name')

# class NewsItemAdmin(admin.ModelAdmin):
#     list_display = ('date', 'title')

# admin.site.register(RMDBEntry, EntryAdmin)
# admin.site.register(NewsItem, NewsItemAdmin)
# admin.site.register(Publication, PublicationAdmin)
# admin.site.register(Organism, OrganismAdmin)

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


