Library Management System
This is a Django-based web application for managing a library's book collection and user permissions. This project was developed as part of the ALX Django Learn Lab.
Features
•	User Authentication: Users can register, log in, and log out.
•	Book Management:
o	Books can be created, viewed, edited, and deleted.
o	Book data includes title, author, published date, and ISBN.
•	Permissions and Roles:
o	The system uses custom permissions to control access to different features.
o	Users are assigned to groups (e.g., Librarian, Member) that grant specific permissions.
•	Author Management: Authors can be created and managed.
Directory Structure
The project has a nested structure as required by the ALX checker:
•	advanced_features_and_security/
o	LibraryProject/
	bookshelf/ (The main application for managing books)
	accounts/ (User authentication and profile management)
	LibraryProject/ (Project-level settings, URLs, etc.)
	manage.py
	README.md (This file)
How to Run
1.	Clone the repository.
2.	Install dependencies: pip install -r requirements.txt (if applicable).
3.	Apply migrations: python manage.py migrate.
4.	Create a superuser: python manage.py createsuperuser.
5.	Run the server: python manage.py runserver.

