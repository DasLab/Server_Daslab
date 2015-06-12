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

class NewsItemAdmin(admin.ModelAdmin):
    list_display = ('date', 'title')
admin.site.register(NewsItem, NewsItemAdmin)

class CurrentMemberAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'role')
admin.site.register(CurrentMember, CurrentMemberAdmin)

class PastMemberAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'finish_year', 'role')
admin.site.register(PastMember, PastMemberAdmin)

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

