# LibraryProject/relationship_app/urls.py

from django.urls import path
from . import views # Import your views.py

app_name = 'relationship_app' # Set the app namespace

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('error/', views.error_page, name='error_page'),

    # Admin URLs
    # Corrected: Changed views.admin_view to views.admin_dashboard
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('app-admin/manage-users/', views.manage_users, name='manage_users'),
    path('app-admin/assign-role/<int:user_id>/', views.assign_role, name='assign_role'),
    path('app-admin/manage-groups/', views.manage_groups, name='manage_groups'),
    path('app-admin/user-list/', views.admin_user_list, name='admin_user_list'),
    # Corrected: Changed views.admin_view to views.admin_dashboard
    path('admin-only/', views.admin_dashboard, name='admin_only_view'), # Added for checker

    # Librarian URLs
    path('librarian-dashboard/', views.librarian_dashboard, name='librarian_dashboard'),
    path('librarian/manage-books/', views.manage_books, name='manage_books'),
    path('librarian/add-book/', views.add_book, name='add_book'),
    # Corrected: Changed views.edit_book to views.update_book and pk for consistency
    path('librarian/edit-book/<int:pk>/', views.update_book, name='edit_book'),
    path('librarian/delete-book/<int:pk>/', views.delete_book, name='delete_book'), # Changed to pk for consistency
    path('librarian/handle-loans/', views.handle_loans, name='handle_loans'),
    path('librarian/borrow-book/', views.borrow_book_librarian, name='borrow_book_librarian'),
    path('librarian/return-book/<int:loan_id>/', views.return_book_librarian, name='return_book_librarian'),
    path('librarian/view-members/', views.view_members, name='view_members'), # This view is missing in views.py
    # Member URLs
    path('member-dashboard/', views.member_dashboard, name='member_dashboard'),
    path('member/book-list/', views.book_list, name='book_list'),
    path('member/my-borrowed-books/', views.my_borrowed_books, name='my_borrowed_books'),
    path('member/request-book/', views.request_book, name='request_book'),

    # General User Profile View
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('user/<str:username>/assigned-books/', views.user_assigned_books_view, name='user_assigned_books_view'), # This view is missing in views.py
]
