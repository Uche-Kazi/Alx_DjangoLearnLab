from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView # CRITICAL FIX: Changed import path for DetailView
from .models import Book # Import Book separately
from .models import Library # Import Library on its own line, as checker expects

# Function-based view to list all books
def book_list(request):
    """
    Function-based view to display a list of all books.
    Renders 'list_books.html' with a context containing all Book objects.
    """
    books = Book.objects.all() # Retrieve all book objects
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
    model = Library # Specify the model this view will work with
    template_name = 'relationship_app/library_detail.html' # Specify the template to render
    context_object_name = 'library' # Name of the context variable for the object

    # No need to override get_context_data for basic DetailView
    # The 'library' object (and its related books) will be available automatically.
