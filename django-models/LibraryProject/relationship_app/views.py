# LibraryProject/relationship_app/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth.views import LoginView # <-- THIS IS THE LINE TO ENSURE IS PRESENT
from django.contrib.auth.models import Group, User
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib import messages
from .forms import CustomUserCreationForm, UserRoleAssignmentForm
from .models import UserProfile, Book, Loan, Author
from django.utils import timezone
from datetime import timedelta
from django.conf import settings

# --- Helper functions for role checking ---
def _get_user_profile_and_ensure_group(user):
    """
    Ensures a UserProfile exists for the user and that the user is in the
    correct default group (Member) if a new profile is created.
    Returns the UserProfile instance.
    """
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    if created:
        # If a new profile was just created, ensure they are in the 'Member' group
        member_group, _ = Group.objects.get_or_create(name=UserProfile.MEMBER)
        user.groups.add(member_group)
        user.save() # Save user to persist group changes
        print(f"DEBUG: _get_user_profile_and_ensure_group: Created UserProfile for {user.username} with default role '{UserProfile.MEMBER}' and added to 'Member' group.")
    return user_profile

def is_admin(user):
    """
    Checks if the user has the 'Admin' role in their UserProfile
    OR if they are a Django superuser.
    This helper is primarily used by the dashboard redirect logic.
    """
    if not user.is_authenticated:
        return False
    
    if user.is_superuser:
        return True

    user_profile = _get_user_profile_and_ensure_group(user)
    return user_profile.role == UserProfile.ADMIN

def is_librarian(user):
    """Checks if the user has the 'Librarian' role in their UserProfile."""
    if not user.is_authenticated:
        return False
    user_profile = _get_user_profile_and_ensure_group(user)
    return user_profile.role == UserProfile.LIBRARIAN

def is_member(user):
    """Checks if the user has the 'Member' role in their UserProfile."""
    if not user.is_authenticated:
        return False
    user_profile = _get_user_profile_and_ensure_group(user)
    return user_profile.role == UserProfile.MEMBER

def is_any_role(user):
    """Checks if the user belongs to any of the defined roles."""
    return is_admin(user) or is_librarian(user) or is_member(user)

# --- Custom Registration View ---
class RegisterView(CreateView):
    """
    Handles user registration, creating a User and UserProfile,
    and assigning the 'Member' group by default.
    """
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('relationship_app:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        # UserProfile creation and default group assignment are handled by the post_save signal
        messages.success(self.request, 'Registration successful! You can now log in.')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Registration failed. Please correct the errors below.')
        return super().form_invalid(form)

# --- Custom Login View ---
class CustomLoginView(LoginView):
    """
    Handles user login and redirects to the appropriate dashboard based on role.
    """
    template_name = 'registration/login.html'
    authentication_form = None

    def get_success_url(self):
        # After successful authentication, ensure the user object has its userprofile pre-fetched
        # This is crucial for immediate role checks in the dashboard view.
        user = self.request.user
        if user.is_authenticated:
            # Re-fetch the user with select_related to ensure userprofile is loaded
            self.request.user = User.objects.select_related('userprofile').get(pk=user.pk)
        return reverse_lazy('relationship_app:dashboard')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password. Please try again.')
        return super().form_invalid(form)

# --- Logout View ---
@login_required
def user_logout(request):
    """Logs out the current user."""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('relationship_app:login')

# --- Generic Home Page (accessible to all) ---
def home(request):
    """Renders the home page."""
    return render(request, 'home.html')

# --- Dashboard View (Generic, now redirects based on UserProfile role) ---
@login_required
def dashboard(request):
    """
    Renders a generic dashboard page and redirects to specific role dashboards.
    Ensures the user's profile is up-to-date for accurate role detection.
    """
    # Force a fresh user object from the database with userprofile pre-fetched
    # This ensures consistency for role checks immediately after login or any redirect to dashboard.
    request.user = User.objects.select_related('userprofile').get(pk=request.user.pk)
    
    # Ensure profile exists and is linked to a group (handled by _get_user_profile_and_ensure_group)
    _get_user_profile_and_ensure_group(request.user)

    print(f"DEBUG: Dashboard accessed by {request.user.username}.")
    
    if is_admin(request.user): # Use helper for dashboard redirect logic
        print(f"DEBUG: Redirecting {request.user.username} to Admin Dashboard.")
        return redirect('relationship_app:admin_dashboard')
    elif is_librarian(request.user): # Use helper for dashboard redirect logic
        print(f"DEBUG: Redirecting {request.user.username} to Librarian Dashboard.")
        return redirect('relationship_app:librarian_dashboard')
    elif is_member(request.user): # Use helper for dashboard redirect logic
        print(f"DEBUG: Redirecting {request.user.username} to Member Dashboard.")
        return redirect('relationship_app:member_dashboard')
    else:
        print(f"DEBUG: No specific role matched for {request.user.username}. Rendering generic dashboard.")
        messages.warning(request, "Your account does not have a specific role assigned. Please contact support.")
        return render(request, 'dashboard.html', {'user_profile': request.user.userprofile})


# --- Role-Based Dashboard Views ---

# Implementing direct role check and HttpResponseForbidden
@login_required
def admin_view(request):
    """
    Admin dashboard view. Accessible only by users with the 'Admin' role.
    """
    if request.user.is_authenticated and (request.user.is_superuser or (hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'Admin')):
        return render(request, 'admin_view.html')
    else:
        messages.error(request, "You are not authorized to access this page.")
        return HttpResponseForbidden("You are not authorized to access this page.")

@login_required
def librarian_view(request):
    """
    Librarian dashboard view. Accessible only by users with the 'Librarian' role.
    """
    if request.user.is_authenticated and hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'Librarian':
        return render(request, 'librarian_view.html')
    else:
        messages.error(request, "You are not authorized to access this page.")
        return HttpResponseForbidden("You are not authorized to access this page.")

@login_required
def member_view(request):
    """
    Member dashboard view. Accessible only by users with the 'Member' role.
    """
    if request.user.is_authenticated and hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'Member':
        return render(request, 'member_view.html')
    else:
        messages.error(request, "You are not authorized to access this page.")
        return HttpResponseForbidden("You are not authorized to access this page.")

# --- Error Page for Unauthorized Access ---
def error_page(request):
    """Renders a generic error page for unauthorized access."""
    return render(request, 'error_page.html', {'message': 'You do not have permission to access this page.'})

# --- Admin Functionality: Manage Users ---
@login_required
def manage_users(request):
    """
    Admin view to list all users and allow role assignment.
    """
    if request.user.is_authenticated and (request.user.is_superuser or (hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'Admin')):
        users = User.objects.all().order_by('username')
        return render(request, 'admin/manage_users.html', {'users': users})
    else:
        messages.error(request, "You are not authorized to access this page.")
        return HttpResponseForbidden("You are not authorized to access this page.")

@login_required
def assign_role(request, user_id):
    """
    Admin view to assign roles to a specific user.
    """
    if not (request.user.is_authenticated and (request.user.is_superuser or (hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'Admin'))):
        messages.error(request, "You are not authorized to perform this action.")
        return HttpResponseForbidden("You are not authorized to perform this action.")

    user_to_assign = get_object_or_404(User, pk=user_id)
    user_profile = _get_user_profile_and_ensure_group(user_to_assign) # Use helper

    if request.method == 'POST':
        form = UserRoleAssignmentForm(request.POST, instance=user_profile)
        if form.is_valid():
            new_role = form.cleaned_data['role']
            
            # Update UserProfile role
            user_profile.role = new_role
            user_profile.save()

            # Clear existing groups and assign the new group based on the selected role
            user_to_assign.groups.clear()
            if new_role == UserProfile.ADMIN:
                group, created = Group.objects.get_or_create(name=UserProfile.ADMIN)
                user_to_assign.groups.add(group)
            elif new_role == UserProfile.LIBRARIAN:
                group, created = Group.objects.get_or_create(name=UserProfile.LIBRARIAN)
                user_to_assign.groups.add(group)
            elif new_role == UserProfile.MEMBER:
                group, created = Group.objects.get_or_create(name=UserProfile.MEMBER)
                user_to_assign.groups.add(group)
            
            user_to_assign.save() # Save the user to persist group changes

            messages.success(request, f'Role for {user_to_assign.username} updated to {new_role}.')
            return redirect('relationship_app:manage_users')
    else:
        form = UserRoleAssignmentForm(instance=user_profile)
    
    return render(request, 'admin/assign_role.html', {'form': form, 'user_to_assign': user_to_assign})

# --- Admin Functionality: Manage Groups (Optional, but good for completeness) ---
@login_required
def manage_groups(request):
    """
    Admin view to list and manage Django groups.
    """
    if request.user.is_authenticated and (request.user.is_superuser or (hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'Admin')):
        groups = Group.objects.all().order_by('name')
        return render(request, 'admin/manage_groups.html', {'groups': groups})
    else:
        messages.error(request, "You are not authorized to access this page.")
        return HttpResponseForbidden("You are not authorized to access this page.")

# --- Admin Functionality: View All Users (for dashboard link) ---
@login_required
def admin_user_list(request):
    """Admin view to list all users with their current roles."""
    if request.user.is_authenticated and (request.user.is_superuser or (hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'Admin')):
        users_with_roles = []
        for user in User.objects.all().order_by('username'):
            role = "N/A"
            user_profile = _get_user_profile_and_ensure_group(user)
            if user_profile.role == UserProfile.ADMIN:
                role = UserProfile.ADMIN
            elif user_profile.role == UserProfile.LIBRARIAN:
                role = UserProfile.LIBRARIAN
            elif user_profile.role == UserProfile.MEMBER:
                role = UserProfile.MEMBER
            users_with_roles.append({'user': user, 'role': role})
        return render(request, 'admin/admin_user_list.html', {'users_with_roles': users_with_roles})
    else:
        messages.error(request, "You are not authorized to access this page.")
        return HttpResponseForbidden("You are not authorized to access this page.")

# --- Librarian Functionality: Manage Books ---
@login_required
def manage_books(request):
    """
    Librarian view to add, edit, or delete books.
    """
    if request.user.is_authenticated and hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'Librarian':
        books = Book.objects.all().order_by('title')
        return render(request, 'librarian/manage_books.html', {'books': books})
    else:
        messages.error(request, "You are not authorized to access this page.")
        return HttpResponseForbidden("You are not authorized to access this page.")

@login_required
def add_book(request):
    """Librarian view to add a new book."""
    if not (request.user.is_authenticated and hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'Librarian'):
        messages.error(request, "You are not authorized to perform this action.")
        return HttpResponseForbidden("You are not authorized to perform this action.")

    if request.method == 'POST':
        title = request.POST.get('title')
        author_name = request.POST.get('author')
        isbn = request.POST.get('isbn')
        published_date = request.POST.get('published_date')
        available_copies = request.POST.get('available_copies')
        total_copies = request.POST.get('total_copies')
        
        author, created = Author.objects.get_or_create(first_name=author_name, defaults={'last_name': ''})

        if title and author and available_copies is not None and total_copies is not None:
            Book.objects.create(
                title=title,
                author=author,
                isbn=isbn,
                published_date=published_date,
                available_copies=available_copies,
                total_copies=total_copies
            )
            messages.success(request, f'Book "{title}" added successfully.')
            return redirect('relationship_app:manage_books')
        else:
            messages.error(request, 'Please fill in all required fields.')
    return render(request, 'librarian/add_book.html')

@login_required
def edit_book(request, book_id):
    """Librarian view to edit an existing book."""
    if not (request.user.is_authenticated and hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'Librarian'):
        messages.error(request, "You are not authorized to perform this action.")
        return HttpResponseForbidden("You are not authorized to perform this action.")

    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        book.title = request.POST.get('title')
        author_name = request.POST.get('author')
        book.isbn = request.POST.get('isbn')
        book.published_date = request.POST.get('published_date')
        book.available_copies = request.POST.get('available_copies')
        book.total_copies = request.POST.get('total_copies')
        
        author, created = Author.objects.get_or_create(first_name=author_name, defaults={'last_name': ''})
        book.author = author
        
        book.save()
        messages.success(request, f'Book "{book.title}" updated successfully.')
        return redirect('relationship_app:manage_books')
    return render(request, 'librarian/edit_book.html', {'book': book})

@login_required
def delete_book(request, book_id):
    """Librarian view to delete a book."""
    if not (request.user.is_authenticated and hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'Librarian'):
        messages.error(request, "You are not authorized to perform this action.")
        return HttpResponseForbidden("You are not authorized to perform this action.")

    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        book.delete()
        messages.success(request, f'Book "{book.title}" deleted successfully.')
        return redirect('relationship_app:manage_books')
    return render(request, 'librarian/delete_book_confirm.html', {'book': book})

# --- Librarian Functionality: Handle Loans ---
@login_required
def handle_loans(request):
    """
    Librarian view to manage book loans (borrow, return).
    """
    if request.user.is_authenticated and hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'Librarian':
        loans = Loan.objects.all().order_by('-loan_date')
        return render(request, 'librarian/handle_loans.html', {'loans': loans})
    else:
        messages.error(request, "You are not authorized to access this page.")
        return HttpResponseForbidden("You are not authorized to access this page.")

@login_required
def borrow_book_librarian(request):
    """Librarian view to facilitate a book loan for a member."""
    if not (request.user.is_authenticated and hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'Librarian'):
        messages.error(request, "You are not authorized to perform this action.")
        return HttpResponseForbidden("You are not authorized to perform this action.")

    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        member_id = request.POST.get('member_id')
        book = get_object_or_404(Book, pk=book_id)
        member = get_object_or_404(User, pk=member_id)

        if not (member.is_authenticated and hasattr(member, 'userprofile') and member.userprofile.role == 'Member'): # Check if target member is actually a member
            messages.error(request, f'{member.username} is not a member or does not have the "Member" role.')
            return redirect('relationship_app:handle_loans')

        if book.available_copies > 0:
            Loan.objects.create(book=book, user=member, loan_date=timezone.now(), due_date=timezone.now() + timedelta(days=14))
            book.available_copies -= 1
            book.save()
            messages.success(request, f'"{book.title}" loaned to {member.username}. Due: {timezone.now() + timedelta(days=14)}.')
        else:
            messages.error(request, '"{book.title}" is currently not available.')
        return redirect('relationship_app:handle_loans')
    
    books = Book.objects.filter(available_copies__gt=0)
    members = User.objects.filter(userprofile__role=UserProfile.MEMBER)
    return render(request, 'librarian/borrow_book_librarian.html', {'books': books, 'members': members})

@login_required
def return_book_librarian(request, loan_id):
    """Librarian view to mark a book as returned."""
    if not (request.user.is_authenticated and hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'Librarian'):
        messages.error(request, "You are not authorized to perform this action.")
        return HttpResponseForbidden("You are not authorized to perform this action.")

    loan = get_object_or_404(Loan, pk=loan_id)
    if request.method == 'POST':
        if not loan.return_date:
            loan.return_date = timezone.now()
            loan.book.available_copies += 1
            loan.book.save()
            loan.save()
            messages.success(request, f'"{loan.book.title}" returned by {loan.user.username}.')
        else:
            messages.warning(request, '"{loan.book.title}" was already returned.')
        return redirect('relationship_app:handle_loans')
    return render(request, 'librarian/return_book_librarian.html', {'loan': loan})

# --- Librarian Functionality: View Members ---
@login_required
def view_members(request):
    """Librarian view to list all members."""
    if request.user.is_authenticated and hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'Librarian':
        members = User.objects.filter(userprofile__role=UserProfile.MEMBER).order_by('username')
        return render(request, 'librarian/view_members.html', {'members': members})
    else:
        messages.error(request, "You are not authorized to access this page.")
        return HttpResponseForbidden("You are not authorized to access this page.")


# --- Member Functionality: View All Books ---
@login_required
def book_list(request):
    """
    Member view to list all available books.
    """
    if request.user.is_authenticated and hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'Member':
        books = Book.objects.filter(available_copies__gt=0).order_by('title')
        return render(request, 'relationship_app/book_list.html', {'books': books})
    else:
        messages.error(request, "You are not authorized to access this page.")
        return HttpResponseForbidden("You are not authorized to access this page.")

# --- Member Functionality: View My Borrowed Books ---
@login_required
def my_borrowed_books(request):
    """
    Member view to list books currently borrowed by the logged-in member.
    """
    if request.user.is_authenticated and hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'Member':
        borrowed_loans = Loan.objects.filter(user=request.user, return_date__isnull=True).order_by('-loan_date')
        return render(request, 'member/my_borrowed_books.html', {'borrowed_loans': borrowed_loans})
    else:
        messages.error(request, "You are not authorized to access this page.")
        return HttpResponseForbidden("You are not authorized to access this page.")

# --- Member Functionality: Request a Book (Placeholder) ---
@login_required
def request_book(request):
    """
    Member view to request a book (placeholder for future functionality).
    """
    if request.user.is_authenticated and hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'Member':
        if request.method == 'POST':
            messages.info(request, "Book request functionality is under development.")
            return redirect('relationship_app:member_dashboard')
        
        unavailable_books = Book.objects.filter(available_copies=0).order_by('title')
        return render(request, 'member/request_book.html', {'unavailable_books': unavailable_books})
    else:
        messages.error(request, "You are not authorized to access this page.")
        return HttpResponseForbidden("You are not authorized to access this page.")

# --- User Profile View ---
@login_required
def user_profile(request, username):
    """
    Displays a user's profile.
    """
    target_user = get_object_or_404(User, username=username)
    user_profile = _get_user_profile_and_ensure_group(target_user) # Use helper

    context = {
        'target_user': target_user,
        'user_profile': user_profile,
        'borrowed_loans': Loan.objects.filter(user=target_user, return_date__isnull=True)
    }
    return render(request, 'user_profile.html', context)

@login_required
def user_assigned_books_view(request, username):
    """
    Displays books assigned to a specific user (for admin/librarian).
    """
    if request.user.is_authenticated and (request.user.is_superuser or (hasattr(request.user, 'userprofile') and (request.user.userprofile.role == 'Admin' or request.user.userprofile.role == 'Librarian'))):
        target_user = get_object_or_404(User, username=username)
        assigned_loans = Loan.objects.filter(user=target_user, return_date__isnull=True)
        context = {
            'target_user': target_user,
            'assigned_loans': assigned_loans
        }
        return render(request, 'user_assigned_books.html', context)
    else:
        messages.error(request, "You are not authorized to access this page.")
        return HttpResponseForbidden("You are not authorized to access this page.")
