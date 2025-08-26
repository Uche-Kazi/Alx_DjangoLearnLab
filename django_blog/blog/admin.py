# ~/Alx_DjangoLearnLab/django_blog/blog/admin.py

from django.contrib import admin
from .models import Post, Comment # Import both Post and Comment models

# Register your Post model using a custom ModelAdmin
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # 'list_display' controls which fields are shown in the change list page
    # Using 'published_date' as 'publish' and assuming 'status' might be a future field or handled differently
    list_display = ('title', 'author', 'published_date')

    # 'list_filter' adds filters to the right sidebar
    list_filter = ('author', 'published_date') # Filter by author and publication date

    # 'search_fields' enables a search bar for specified fields
    search_fields = ('title', 'content') # Search by title and content

    # Removed 'slug' from prepopulated_fields as it's not in your model.
    # If you want a slug, you'll need to add a SlugField to your Post model.
    # prepopulated_fields = {'slug': ('title',)} # This line is commented out as 'slug' is not a field

    # 'raw_id_fields' changes the input widget for foreign key fields to a text input
    # with a lookup button, which is better for many-to-one relationships with many instances.
    raw_id_fields = ('author',) # 'author' is a ForeignKey, so this is appropriate

    # 'date_hierarchy' adds a date-based drilldown navigation bar at the top
    date_hierarchy = 'published_date' # Use 'published_date' for date hierarchy

    # 'ordering' specifies the default ordering for the change list
    ordering = ('-published_date',) # Order by published date, newest first

# Register your Comment model using a custom ModelAdmin
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    # 'list_display' controls which fields are shown in the change list page for comments
    list_display = ('author', 'post', 'text', 'created_date') # Display author, associated post, text, and creation date

    # 'list_filter' adds filters for creation timestamps and associated post
    list_filter = ('created_date', 'post') # Filter by creation date and post

    # 'search_fields' enables a search bar for comment details
    # We can search by the comment's text and the author's username
    search_fields = ('text', 'author__username')

