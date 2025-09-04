from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # This list allows us to control which fields are displayed in the admin list view.
    list_display = ['title', 'slug', 'author', 'publish', 'status']
    
    # This filter sidebar allows users to filter by status, publish date, and author.
    list_filter = ['status', 'created', 'publish', 'author']
    
    # This search bar allows users to search posts by title and body content.
    search_fields = ['title', 'body']
    
    # This prepopulates the slug field based on the title, making it easier for users.
    prepopulated_fields = {'slug': ('title',)}
    
    # This allows for a hierarchical browsing of posts by date.
    date_hierarchy = 'publish'
    
    # This orders posts by status and then by publish date.
    ordering = ['status', 'publish']
