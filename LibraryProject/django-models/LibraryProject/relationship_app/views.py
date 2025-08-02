# LibraryProject/relationship_app/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.decorators import permission_required # <--- MOVED TO ITS OWN LINE
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

from .models import CustomUser, Book, Loan, Author
from .forms import BookForm, UserRoleForm

# --- Helper function to check user roles ---
def is_admin(user):
    return user.is_authenticated and user.role == CustomUser.ADMIN

def is_librarian(user):
    return user.is_authenticated and user.role == CustomUser.LIBRARIAN

def is_member(user):
    return user.is_authenticated and user.role == CustomUser.MEMBER

# --- User Registration View ---
class RegisterView(CreateView):
    model = CustomUser
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.role = CustomUser.MEMBER
        user.save()
        messages.success(self.request, 'Account created successfully! You can now log in.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)

# --- Existing views ---

def home(request):
    return render(request, 'home.html')

@login_required
def dashboard(request):
    if request.user.role == CustomUser.ADMIN:
        return redirect('relationship_app:admin_dashboard')
    elif request.user.role == CustomUser.LIBRARIAN:
        return redirect('relationship_app:librarian_dashboard')
    elif request.user.role == CustomUser.MEMBER:
        return redirect('relationship_app:member_dashboard')
    return render(request, 'dashboard.html')

@user_passes_test(is_admin, login_url='relationship_app:error_page')
def admin_dashboard(request):
    return render(request, 'admin_view.html')

@user_passes_test(is_librarian, login_url='relationship_app:error_page')
def librarian_dashboard(request):
    return render(request, 'librarian_view.html')

@user_passes_test(is_member, login_url='relationship_app:error_page')
def member_dashboard(request):
    return render(request, 'member_view.html')

def error_page(request, exception=None):
    return render(request, 'error_page.html', {'message': 'You are not authorized to access this page.'})

# --- Book Management Views (Librarian) ---

# This view handles both displaying books and adding new ones.
# It requires 'can_add_book' permission.
@user_passes_test(is_librarian, login_url='relationship_app:error_page')
@permission_required('relationship_app.can_add_book', login_url='relationship_app:error_page')
def manage_books(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            author_full_name = form.cleaned_data['author'].strip()
            name_parts = author_full_name.split(' ', 1)
            first_name = name_parts[0]
            last_name = name_parts[1] if len(name_parts) > 1 else ''

            author_obj, created = Author.objects.get_or_create(
                first_name=first_name,
                last_name=last_name
            )
            
            book = form.save(commit=False)
            book.author = author_obj
            book.save()
            messages.success(request, f'Book "{book.title}" added successfully!')
            return redirect('relationship_app:manage_books')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BookForm()

    books = Book.objects.all().order_by('title')
    return render(request, 'librarian/manage_books.html', {'books': books, 'form': form})


@user_passes_test(is_librarian, login_url='relationship_app:error_page')
@permission_required('relationship_app.can_add_book', login_url='relationship_app:error_page')
def add_book(request):
    # This view is now redundant if manage_books handles both display and add.
    # We'll keep the permission_required here just in case it's used directly,
    # but the primary add functionality is in manage_books.
    return redirect('relationship_app:manage_books')

# This view handles updating existing books.
# It requires 'can_change_book' permission.
@user_passes_test(is_librarian, login_url='relationship_app:error_page')
@permission_required('relationship_app.can_change_book', login_url='relationship_app:error_page')
def update_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            author_full_name = form.cleaned_data['author'].strip()
            name_parts = author_full_name.split(' ', 1)
            first_name = name_parts[0]
            last_name = name_parts[1] if len(name_parts) > 1 else ''

            author_obj, created = Author.objects.get_or_create(
                first_name=first_name,
                last_name=last_name
            )

            book = form.save(commit=False)
            book.author = author_obj
            book.save()
            messages.success(request, f'Book "{book.title}" updated successfully!')
            return redirect('relationship_app:manage_books')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        initial_author_name = f"{book.author.first_name} {book.author.last_name}".strip() if book.author else ""
        form = BookForm(instance=book, initial={'author': initial_author_name})

    return render(request, 'librarian/edit_book.html', {'form': form, 'book': book})

# This view handles deleting books.
# It requires 'can_delete_book' permission.
@user_passes_test(is_librarian, login_url='relationship_app:error_page')
@permission_required('relationship_app.can_delete_book', login_url='relationship_app:error_page')
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        messages.success(request, f'Book "{book.title}" deleted successfully!')
        return redirect('relationship_app:manage_books')
    return render(request, 'librarian/delete_book_confirm.html', {'book': book})

# --- Loan Management Views (Librarian) ---

@user_passes_test(is_librarian, login_url='relationship_app:error_page')
def handle_loans(request):
    loans = Loan.objects.filter(return_date__isnull=True).order_by('-loan_date')
    return render(request, 'librarian/handle_loans.html', {'loans': loans})

@user_passes_test(is_librarian, login_url='relationship_app:error_page')
def borrow_book_librarian(request):
    books = Book.objects.filter(available_copies__gt=0).order_by('title')
    members = CustomUser.objects.filter(role=CustomUser.MEMBER).order_by('username')

    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        member_id = request.POST.get('member_id')

        book = get_object_or_404(Book, id=book_id)
        member = get_object_or_404(CustomUser, id=member_id)

        if book.available_copies > 0:
            Loan.objects.create(book=book, user=member, loan_date=timezone.now(), due_date=timezone.now() + timedelta(days=14))
            book.available_copies -= 1
            book.save()
            messages.success(request, f'Book "{book.title}" successfully loaned to {member.username}.')
            return redirect('relationship_app:handle_loans')
        else:
            messages.error(request, f'"{book.title}" has no available copies.')

    return render(request, 'librarian/borrow_book_librarian.html', {'books': books, 'members': members})

@user_passes_test(is_librarian, login_url='relationship_app:error_page')
def return_book_librarian(request, loan_id):
    loan = get_object_or_404(Loan, id=loan_id, return_date__isnull=True)
    if request.method == 'POST':
        loan.return_date = timezone.now()
        loan.save()
        loan.book.available_copies += 1
        loan.book.save()
        messages.success(request, f'Book "{loan.book.title}" returned by {loan.user.username}.')
        return redirect('relationship_app:handle_loans')
    return render(request, 'librarian/return_book_librarian.html', {'loan': loan})

# --- Member Views ---

@login_required
@user_passes_test(is_member, login_url='relationship_app:error_page')
def book_list(request):
    books = Book.objects.all().order_by('title')
    return render(request, 'member/book_list.html', {'books': books})

@login_required
@user_passes_test(is_member, login_url='relationship_app:error_page')
def my_borrowed_books(request):
    borrowed_loans = Loan.objects.filter(user=request.user, return_date__isnull=True).order_by('-loan_date')
    return render(request, 'member/my_borrowed_books.html', {'borrowed_loans': borrowed_loans})

@login_required
@user_passes_test(is_member, login_url='relationship_app:error_page')
def request_book(request):
    unavailable_books = Book.objects.filter(available_copies=0).order_by('title')
    return render(request, 'member/request_book.html', {'unavailable_books': unavailable_books})

# --- User Profile & Admin User Management Views ---

@login_required
def user_profile(request, username):
    target_user = get_object_or_404(CustomUser, username=username)
    borrowed_loans = Loan.objects.filter(user=target_user, return_date__isnull=True).order_by('-loan_date')
    return render(request, 'user_profile.html', {'target_user': target_user, 'borrowed_loans': borrowed_loans})

@user_passes_test(is_admin, login_url='relationship_app:error_page')
def admin_user_list(request):
    users = CustomUser.objects.all().order_by('username')
    users_with_roles = []
    for user in users:
        users_with_roles.append({
            'user': user,
            'role': user.get_role_display()
        })
    return render(request, 'admin/admin_user_list.html', {'users_with_roles': users_with_roles})

@user_passes_test(is_admin, login_url='relationship_app:error_page')
def assign_role(request, user_id):
    user_to_assign = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        form = UserRoleForm(request.POST, instance=user_to_assign)
        if form.is_valid():
            form.save()
            messages.success(request, f'Role for {user_to_assign.username} updated successfully!')
            return redirect('relationship_app:admin_user_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRoleForm(instance=user_to_assign)
    return render(request, 'admin/assign_role.html', {'form': form, 'user_to_assign': user_to_assign})

@user_passes_test(is_admin, login_url='relationship_app:error_page')
def manage_users(request):
    return render(request, 'admin/manage_users.html')

@user_passes_test(is_admin, login_url='relationship_app:error_page')
def manage_groups(request):
    return render(request, 'admin/manage_groups.html')

@user_passes_test(is_librarian, login_url='relationship_app:error_page')
def view_members(request):
    members = CustomUser.objects.filter(role=CustomUser.MEMBER).order_by('username')
    return render(request, 'librarian/view_members.html', {'members': members})

@login_required
def user_assigned_books_view(request, username):
    target_user = get_object_or_404(CustomUser, username=username)
    assigned_loans = Loan.objects.filter(user=target_user).order_by('-loan_date')
    return render(request, 'user_assigned_books.html', {'target_user': target_user, 'assigned_loans': assigned_loans})
