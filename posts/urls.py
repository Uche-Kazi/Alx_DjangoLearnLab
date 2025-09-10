from django.urls import path
from .views import (
    PostListCreateView,
    PostDetailView,
    CommentListCreateView,
    LikeCreateView,
    LikeDestroyView
)

urlpatterns = [
    path('', PostListCreateView.as_view(), name='post-list-create'),
    path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('<int:pk>/comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('<int:pk>/like/', LikeCreateView.as_view(), name='like-create'),
    path('<int:pk>/unlike/', LikeDestroyView.as_view(), name='like-delete'),
]
