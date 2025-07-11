# Delete Operation

## Command:
```python
from bookshelf.models import Book
book_to_delete = Book.objects.get(title="Nineteen Eighty-Four") # Retrieve the updated book
book_to_delete.delete()
print(f"book.delete: {Book.objects.all()}") # Modified print statement