from django.contrib import admin
from properties.admin_export import BLOG_POST_EXPORT, ExportMixin
from .models import BlogPost, BlogCategory


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(BlogPost)
class BlogPostAdmin(ExportMixin, admin.ModelAdmin):
    export_config = BLOG_POST_EXPORT
    list_display = ['title', 'author', 'category', 'published', 'created_at']
    list_filter = ['published', 'category', 'created_at']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'content', 'meta_tags']
    date_hierarchy = 'created_at'
