from django.contrib import admin

from .models import Article, Tag, Site

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'published', 'link', 'site', 'is_deleted')
    list_display_links = ('title', 'is_deleted')
    search_fields = ('published', 'title', 'tags', 'site', 'link', 'is_deleted')
    
class TagAdmin(admin.ModelAdmin):
    list_display = ('tag',)
    list_display_links = ('tag',)
    
class SiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'link', 'is_active', 'is_allowed')
    list_display_links = ('name', 'link', 'is_active', 'is_allowed')
    search_fields = ('name', 'link', 'is_active', 'is_allowed')
    
admin.site.register(Article, ArticleAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Site, SiteAdmin)    
