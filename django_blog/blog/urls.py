# blog/urls.py

from django.urls import path
from . import views
from .views import (
    PostListView,
    post_detail,
    UserPostListView,
    post_share,
    CommentCreateView,  # Import new CBVs
    CommentUpdateView,  # Import new CBVs
    CommentDeleteView,  # Import new CBVs
)

app_name = 'blog'

urlpatterns = [
    # Post list view
    path('', PostListView.as_view(), name='post_list'),
    path('tag/<slug:tag_slug>/', PostListView.as_view(), name='post_list_by_tag'),
    path('user/<str:username>/', UserPostListView.as_view(), name='user_posts'),

    # Post detail view (now handles displaying comments and the create form)
    path('<int:year>/<int:month>/<int:day>/<slug:post_slug>/',
         post_detail,
         name='post_detail'),

    # Post share view
    path('<int:post_id>/share/', post_share, name='post_share'),

    # NEW Comment-related URLs using class-based views and nested structure:
    # URL for creating a new comment on a specific post
    path('<int:post_id>/comments/new/',
         CommentCreateView.as_view(),
         name='comment_create'),

    # URL for editing an existing comment
    path('comments/<int:pk>/edit/',
         CommentUpdateView.as_view(),
         name='comment_update'),

    # URL for deleting an existing comment
    path('comments/<int:pk>/delete/',
         CommentDeleteView.as_view(),
         name='comment_delete'),
]
