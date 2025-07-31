# LibraryProject/relationship_app/forms.py

from django import forms
from .models import Book, CustomUser, Author
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

class BookForm(forms.ModelForm):
    # Override the 'author' field to be a CharField for free text input
    author = forms.CharField(max_length=200, label="Author Name")

    class Meta:
        model = Book
        # EXCLUDE 'author' from Meta.fields because we are handling it manually in the view
        fields = ['title', 'isbn', 'published_date', 'available_copies', 'total_copies']
        widgets = {
            'published_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='form-group col-md-6 mb-0'),
                Column('author', css_class='form-group col-md-6 mb-0'), # This refers to the CharField defined above
                css_class='form-row'
            ),
            Row(
                Column('isbn', css_class='form-group col-md-6 mb-0'),
                Column('published_date', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('available_copies', css_class='form-group col-md-6 mb-0'),
                Column('total_copies', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Add Book', css_class='btn btn-primary mt-4')
        )

class UserRoleForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['role']
        labels = {
            'role': 'Assign Role',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'role',
            Submit('submit', 'Update Role', css_class='btn btn-primary mt-4')
        )
