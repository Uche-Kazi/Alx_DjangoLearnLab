# LibraryProject/relationship_app/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required # Only login_required is used now
from django.http import HttpResponseForbidden, HttpResponse # Import HttpResponse for the 403 handler
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import Group
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib import messages
from django.conf import settings

# Import CustomUser and other models
from .models import CustomUser, Book, Loan, Author
from .forms import CustomUserCreationForm, UserRoleAssignmentForm


from django.utils import timezone
from datetime import timedelta


# --- Helper functions for role checking (still used by dashboard redirect) ---
# These are kept for the dashboard's internal redirection logic, but
# the individual views will use direct 'request.user.role' checks.
def is_admin(user):
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    return user.role == CustomUser.ADMIN

def is_librarian(user):
    if not user.is_authenticated:
        return False
    return user.role == CustomUser.LIBRARIAN

def is_member(user):
    if not user.is_authenticated:
        return False
    return user.role == CustomUser.MEMBER

def is_any_role(user):
    return is_admin(user) or is_librarian(user) or is_member(user)

# --- Custom 403 Handler ---
# This handler is still defined in urls.py, but these specific views
# will return HttpResponseForbidden directly instead of raising PermissionDenied.
def custom_403_view(request, exception=None):
    messages.error(request, "You do not have permission to access this page.")
    return HttpResponseForbidden("You are not authorized to access this page.")

# --- Custom Registration View ---
class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('relationship_app:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        member_group, _ = Group.objects.get_or_create(name=CustomUser.MEMBER)
        user.groups.add(member_group)
        user.save()
        messages.success(self.request, 'Registration successful! You can now log in.')
        return response

    def form_invalid(self, form):
        messages.error(request, 'Registration failed. Please correct the errors below.')
        return super().form_invalid(form)

# --- Custom Login View ---
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = None

    def get_success_url(self):
        return reverse_lazy('relationship_app:dashboard')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password. Please try again.')
        return super().form_invalid(form)

# --- Logout View ---
@login_required
def user_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('relationship_app:login')

# --- Generic Home Page (accessible to all) ---
def home(request):
    return render(request, 'home.html')

# --- Dashboard View (Generic, redirects based on CustomUser role) ---
@login_required
def dashboard(request):
    print(f"DEBUG: Dashboard accessed by {request.user.username}.")
    
    if is_admin(request.user):
        print(f"DEBUG: Redirecting {request.user.username} to Admin Dashboard.")
        return redirect('relationship_app:admin_dashboard')
    elif is_librarian(request.user):
        print(f"DEBUG: Redirecting {request.user.username} to Librarian Dashboard.")
        return redirect('relationship_app:librarian_dashboard')
    elif is_member(request.user):
        print(f"DEBUG: Redirecting {request.user.username} to Member Dashboard.")
        return redirect('relationship_app:member_dashboard')
    else:
        print(f"DEBUG: No specific role matched for {request.user.username}. Rendering generic dashboard.")
        messages.warning(request, "Your account does not have a specific role assigned. Please contact support.")
        return render(request, 'dashboard.html', {'user': request.user})

# --- Role-Based Dashboard Views (Direct Role Check + HttpResponseForbidden) ---

@login_required
def admin_view(request):
    """
    Admin dashboard view. Accessible only by users with the 'Admin' role.
    """
    if not request.user.is_superuser and request.user.role != CustomUser.ADMIN:
        messages.error(request, "You are not authorized to access this page.")
        return HttpResponseForbidden("You are not authorized to access this page.")
    return render(request, 'admin_view.html')

@login_required
def librarian_view(request):
    """
    Librarian dashboard view. Accessible only by users with the 'Librarian' role.
    """
    if request.user.role != CustomUser.LIBRARIAN:
        messages.error(request, "You are not authorized to access this page.")
        return HttpResponseForbidden("You are not authorized to access this page.")
    return render(request, 'librarian_view.html')

@login_required
def member_view(request):
    """
    Member dashboard view. Accessible only by users with the 'Member' role.
    """
    if request.user.role != CustomUser.MEMBER:
        messages.error(request, "You are not authorized to access this page.")
        return HttpResponseForbidden("You are not authorized to access this page.")
    return render(request, 'member_view.html')

# --- Error Page for Unauthorized Access ---
def error_page(request):
    return render(request, 'error_page.html', {'message': 'You do not have permission to access this page.'})

# --- Admin Functionality: Manage Users ---
@login_required
def manage_users(request):
    if not request.user.is_superuser and request.user.role != CustomUser.ADMIN:
        messages.error(request, "You are not authorized to access this page.")
        return HttpResponseForbidden("You are not authorized to access this page.")
    users = CustomUser.objects.all().order_by('username')
    return render(request, 'admin/manage_users.html', {'users': users})

@login_required
def assign_role(request, user_id):
    if not request.user.is_superuser and request.user.role != CustomUser.ADMIN:
        messages.error(request, "You are not authorized to perform this action.")
        return HttpResponseForbidden("You are not authorized to perform this action.")

    user_to_assign = get_object_or_404(CustomUser, pk=user_id)

    if request.method == 'POST':
        form = UserRoleAssignmentForm(request.POST, instance=user_to_assign)
        if form.is_valid():
            new_role = form.cleaned_data['role']
            user_to_assign.role = new_role
            user_to_assign.save()

            user_to_assign.groups.clear()
            if new_role == CustomUser.ADMIN:
                group, created = Group.objects.get_or_create(name=CustomUser.ADMIN)
                user_to_assign.groups.add(group)
            elif new_role == CustomUser.LIBRARIAN:
                group, created = Group.objects.get_or_create(name=CustomUser.LIBRARIAN)
                user_to_assign.groups.add(group)
            elif new_role == CustomUser.MEMBER:
                group, created = Group.objects.get_or_create(name=CustomUser.MEMBER)
                user_to_assign.groups.add(group)
            
            user_to_assign.save()

            messages.success(request, f'Role for {user_to_assign.username} updated to {new_role}.')
            return redirect('relationship_app:manage_users')
    else:
        form = UserRoleAssignmentForm(instance=user_to_assign)
    
    return render(request, 'admin/assign_role.html', {'form': form, 'user_to_assign': user_to_assign})

# --- Admin Functionality: Manage Groups (Optional, but good for completeness) ---
@login_required
def manage_groups(request):
    if not request.user.is_superuser and request.user.role != CustomUser.ADMIN:
        messages.error(request, "You are not authorized to access this page.")
        return HttpResponseForbidden("You are not authorized to access this page.")
    groups = Group.objects.all().order_by('name')
    return render(request, 'admin/manage_groups.html', {'groups': groups})

# --- Admin Functionality: View All Users (for dashboard link) ---
@login_required
def admin_user_list(request):
    if not request.user.is_superuser and request.user.role != CustomUser.ADMIN:
        messages.error(request, "You are not authorized to access this page.")
        return HttpResponseForbidden("You are not authorized to access this page.")
    users_with_roles = []
    for user in CustomUser.objects.all().order_by('username'):
        users_with_roles.append({'user': user, 'role': user.role})
    return render(request, 'admin/admin_user_list.html', {'users_with_roles': users_with_roles})

# --- Librarian Functionality: Manage Books ---
@login_required
def manage_books(request):
    if request.user.role != CustomUser.LIBRARIAN:
        messages.error(request, "You are not authorized to access this page.")
        return HttpResponseForbidden("You are not authorized to access this page.")
    books = Book.objects.all().order_by('title')
    return render(request, 'librarian/manage_books.html', {'books': books})

@login_required
def add_book(request):
    if request.user.role != CustomUser.LIBRARIAN:
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
    if request.user.role != CustomUser.LIBRARIAN:
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
    if request.user.role != CustomUser.LIBRARIAN:
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
    if request.user.role != CustomUser.LIBRARIAN:
        messages.error(request, "You are not authorized to access this page.")
        return HttpResponseForbidden("You are not authorized to access this page.")
    loans = Loan.objects.all().order_by('-loan_date')
    return render(request, 'librarian/handle_loans.html', {'loans': loans})

@login_required
def borrow_book_librarian(request):
    if request.user.role != CustomUser.LIBRARIAN:
        messages.error(request, "You are not authorized to perform this action.")
        return HttpResponseForbidden("You are not authorized to perform this action.")
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        member_id = request.POST.get('member_id')
        book = get_object_or_404(Book, pk=book_id)
        member = get_object_or_404(CustomUser, pk=member_id)

        if member.role != CustomUser.MEMBER: # Direct check for target member's role
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
    members = CustomUser.objects.filter(role=CustomUser.MEMBER)
    return render(request, 'librarian/borrow_book_librarian.html', {'books': books, 'members': members})

@login_required
def return_book_librarian(request, loan_id):
    if request.user.role != CustomUser.LIBRARIAN:
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
    if request.user.role != CustomUser.LIBRARIAN:
        messages.error(request, "You are not authorized to access this page.")
        return HttpResponseForbidden("You are not authorized to access this page.")
    members = CustomUser.objects.filter(role=CustomUser.MEMBER).order_by('username')
    return render(request, 'librarian/view_members.html', {'members': members})


# --- Member Functionality: View All Books ---
@login_required
def book_list(request):
    if request.user.role != CustomUser.MEMBER:
        messages.error(request, "You are not authorized to access this page.")
        return HttpResponseForbidden("You are not authorized to access this page.")
    books = Book.objects.filter(available_copies__gt=0).order_by('title')
    return render(request, 'relationship_app/book_list.html', {'books': books})

# --- Member Functionality: View My Borrowed Books ---
@login_required
def my_borrowed_books(request):
    if request.user.role != CustomUser.MEMBER:
        messages.error(request, "You are not authorized to access this page.")
        return HttpResponseForbidden("You are not authorized to access this page.")
    borrowed_loans = Loan.objects.filter(user=request.user, return_date__isnull=True).order_by('-loan_date')
    return render(request, 'member/my_borrowed_books.html', {'borrowed_loans': borrowed_loans})

# --- Member Functionality: Request a Book (Placeholder) ---
@login_required
def request_book(request):
    if request.user.role != CustomUser.MEMBER:
        messages.error(request, "You are not authorized to access this page.")
        return HttpResponseForbidden("You are not authorized to access this page.")
    if request.method == 'POST':
        messages.info(request, "Book request functionality is under development.")
        return redirect('relationship_app:member_dashboard')
    
    unavailable_books = Book.objects.filter(available_copies=0).order_by('title')
    return render(request, 'member/request_book.html', {'unavailable_books': unavailable_books})

# --- User Profile View ---
@login_required
def user_profile(request, username):
    target_user = get_object_or_404(CustomUser, username=username)
    context = {
        'target_user': target_user,
        'user_profile': target_user,
        'borrowed_loans': Loan.objects.filter(user=target_user, return_date__isnull=True)
    }
    return render(request, 'user_profile.html', context)

@login_required
def user_assigned_books_view(request, username):
    if request.user.role != CustomUser.ADMIN and request.user.role != CustomUser.LIBRARIAN:
        messages.error(request, "You are not authorized to access this page.")
        return HttpResponseForbidden("You are not authorized to access this page.")
    target_user = get_object_or_404(CustomUser, username=username)
    assigned_loans = Loan.objects.filter(user=target_user, return_date__isnull=True)
    context = {
        'target_user': target_user,
        'assigned_loans': assigned_loans
    }
    return render(request, 'user_assigned_books.html', context)
