# Update Operation

## Command:
```python
from bookshelf.models import Book
book_to_update = Book.objects.get(title="1984") # Or use 'Nineteen Eighty-Four' if you re-run shell
book_to_update.title = "Nineteen Eighty-Four"
book_to_update.save()
print(f"book.title: {book_to_update.title}") # Modified print statement