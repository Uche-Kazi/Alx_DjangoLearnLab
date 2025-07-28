# LibraryProject/relationship_app/urls.py

from django.urls import path
from . import views # Import your views.py

app_name = 'relationship_app' # <-- THIS IS CRUCIAL FOR NAMESPACING

urlpatterns = [
    # --- Home Page ---
    path('', views.home, name='home'),

    # --- Authentication URLs ---
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),

    # --- Generic Dashboard (redirects to specific role dashboards) ---
    path('dashboard/', views.dashboard, name='dashboard'),

    # --- Role-Based Dashboard Views (as per your instructions) ---
    path('admin-dashboard/', views.admin_view, name='admin_dashboard'),
    path('librarian-dashboard/', views.librarian_view, name='librarian_dashboard'),
    path('member-dashboard/', views.member_view, name='member_dashboard'),
    path('default-dashboard/', views.dashboard, name='default_dashboard'), # Fallback to generic dashboard

    # --- Admin Specific Functionality URLs (CHANGED PREFIX TO 'app-admin/') ---
    path('app-admin/manage-users/', views.manage_users, name='manage_users'),
    path('app-admin/assign-role/<int:user_id>/', views.assign_role, name='assign_role'),
    path('app-admin/manage-groups/', views.manage_groups, name='manage_groups'),
    path('app-admin/user-list/', views.admin_user_list, name='admin_user_list'),

    # --- Librarian Specific Functionality URLs ---
    path('librarian/manage-books/', views.manage_books, name='manage_books'),
    path('librarian/add-book/', views.add_book, name='add_book'),
    path('librarian/edit-book/<int:book_id>/', views.edit_book, name='edit_book'),
    path('librarian/delete-book/<int:book_id>/', views.delete_book, name='delete_book'),
    path('librarian/handle-loans/', views.handle_loans, name='handle_loans'),
    path('librarian/borrow-book/', views.borrow_book_librarian, name='borrow_book_librarian'),
    path('librarian/return-book/<int:loan_id>/', views.return_book_librarian, name='return_book_librarian'),
    path('librarian/view-members/', views.view_members, name='view_members'),

    # --- Member Specific Functionality URLs ---
    path('member/book-list/', views.book_list, name='book_list'),
    path('member/my-borrowed-books/', views.my_borrowed_books, name='my_borrowed_books'),
    path('member/request-book/', views.request_book, name='request_book'),

    # --- User Profile URLs ---
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('user/<str:username>/assigned-books/', views.user_assigned_books_view, name='user_assigned_books'),

    # --- Error Page ---
    path('error/', views.error_page, name='error_page'),
]
