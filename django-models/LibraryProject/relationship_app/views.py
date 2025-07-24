from django.shortcuts import render, redirect
from django.views.generic import DetailView, CreateView
from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy

from .models import Book
from .models import Library
from .forms import UserRegistrationForm

# Function-based view to list all books
def list_books(request):
    """
    Function-based view to display a list of all books.
    Renders 'list_books.html' with a context containing all Book objects.
    """
    books = Book.objects.all()
    context = {
        'books': books
    }
    return render(request, 'relationship_app/list_books.html', context)

# Class-based view to display details for a specific library
class LibraryDetailView(DetailView):
    """
    Class-based view to display details of a specific library,
    including all books available in that library.
    Utilizes Django's DetailView.
    """
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

# User Registration View
class RegisterView(CreateView):
    """
    Class-based view for user registration.
    Uses UserRegistrationForm to create a new user.
    """
    template_name = 'relationship_app/register.html'
    form_class = UserRegistrationForm
    # CRITICAL FIX: Use namespaced URL for login
    success_url = reverse_lazy('relationship_app:login')

# User Login View - Added debugging methods
class CustomLoginView(LoginView):
    """
    Custom class-based view for user login.
    Uses Django's built-in LoginView.
    """
    template_name = 'relationship_app/login.html'
    authentication_form = AuthenticationForm
    # CRITICAL FIX: Use namespaced URL for book_list
    next_page = reverse_lazy('relationship_app:book_list')

    def form_valid(self, form):
        """
        This method is called when the login form is submitted with valid data.
        It logs the user in and redirects to the success URL.
        """
        print("Login form is VALID. Attempting to log in user...")
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        This method is called when the login form is submitted with invalid data.
        It re-renders the form with errors.
        """
        print("Login form is INVALID. Errors:", form.errors)
        return super().form_invalid(form)

# User Logout View
def custom_logout_view(request):
    """
    Handles user logout.
    Logs out the user and redirects to the login page.
    """
    if request.method == 'POST':
        logout(request)
        # CRITICAL FIX: Use namespaced URL for login
        return redirect(reverse_lazy('relationship_app:login'))
    return redirect(reverse_lazy('relationship_app:login'))
