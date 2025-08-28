# blog/urls.py

from django.urls import path
# Import all view functions/classes directly from .views as they are used without 'views.' prefix
from .views import (
    PostListView,
    post_detail,
    UserPostListView,
    post_share,
    edit_comment,   # <--- Ensure these are imported directly
    delete_comment, # <--- Ensure these are imported directly
)

app_name = 'blog' # Define the application namespace

urlpatterns = [
    # Post list view
    path('', PostListView.as_view(), name='post_list'),
    path('tag/<slug:tag_slug>/', PostListView.as_view(), name='post_list_by_tag'),
    path('user/<str:username>/', UserPostListView.as_view(), name='user_posts'), # Using the imported view

    # Post detail view
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         post_detail, # <--- Corrected: Using post_detail directly
         name='post_detail'),

    # Post share view
    # This pattern links to the post_share view and takes a post_id as an integer.
    path('<int:post_id>/share/', post_share, name='post_share'), # <--- Corrected: Using post_share directly

    # Comment related URLs
    path('comment/<int:comment_id>/edit/', edit_comment, name='edit_comment'), # <--- Corrected: Using edit_comment directly
    path('comment/<int:comment_id>/delete/', delete_comment, name='delete_comment'), # <--- Corrected: Using delete_comment directly

    # Other paths can go here
]
