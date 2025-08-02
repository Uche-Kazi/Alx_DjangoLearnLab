# advanced_features_and_security/LibraryProject/relationship_app/forms.py
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div
from .models import Book, CustomUser


class BookForm(forms.ModelForm):
    """
    Form for creating and updating Book instances.
    It uses crispy forms to style the layout.
    """
    class Meta:
        model = Book
        # Removed 'cover_image' and 'publisher' fields as they do not exist in the Book model.
        # This resolves the FieldError.
        fields = ('title', 'author', 'isbn', 'description')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Book Information',
                'title',
                'author',
                'isbn',
                'description',
            ),
            ButtonHolder(
                Submit('submit', 'Save Book', css_class='button white')
            )
        )


class UserRoleForm(forms.ModelForm):
    """
    Form for updating a user's role.
    It uses crispy forms to style the layout.
    """
    class Meta:
        model = CustomUser
        # The only field we want to update here is the user's role
        fields = ('role',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                'role',
                css_class='col-6'
            ),
            ButtonHolder(
                Submit('submit', 'Update Role', css_class='button white')
            )
        )
