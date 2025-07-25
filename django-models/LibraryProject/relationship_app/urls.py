from django.urls import path, include
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

app_name = 'relationship_app'

urlpatterns = [
    path('books/', views.list_books, name='book_list'),
    path('libraries/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),

    # Using RegisterView from your app's views (class-based view)
    path('register/', views.RegisterView.as_view(), name='register'),
    
    # Using Django's built-in LoginView directly with template_name
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    
    # Using Django's built-in LogoutView directly with template_name
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html', next_page=reverse_lazy('relationship_app:login')), name='logout'),
]
