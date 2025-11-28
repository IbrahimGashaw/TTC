from django.contrib import admin
from .models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'published', 'created_at']
    list_filter = ['published', 'created_at']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'content']
    date_hierarchy = 'created_at'

