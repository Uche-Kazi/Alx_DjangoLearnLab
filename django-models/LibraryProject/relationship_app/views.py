from django.shortcuts import render, redirect
from django.views.generic import DetailView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.contrib.auth import login # Ensure login is available for function-based register

from .models import Book
from .models import Library
from .forms import UserRegistrationForm # Our custom registration form

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

# User Registration View (Now function-based)
def register(request): # Changed from class RegisterView to function register
    """
    Function-based view for user registration.
    Handles the UserRegistrationForm and logs the user in upon success.
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Log the user in after registration
            return redirect(reverse_lazy('relationship_app:book_list')) # Redirect to book list after login
    else:
        form = UserRegistrationForm()
    return render(request, 'relationship_app/register.html', {'form': form})


# User Login View
class CustomLoginView(LoginView):
    """
    Custom class-based view for user login.
    Uses Django's built-in LoginView.
    """
    template_name = 'relationship_app/login.html'
    authentication_form = AuthenticationForm
    next_page = reverse_lazy('relationship_app:book_list')

# User Logout View
class CustomLogoutView(LogoutView):
    """
    Custom class-based view for user logout.
    Uses Django's built-in LogoutView.
    """
    next_page = reverse_lazy('relationship_app:login')
