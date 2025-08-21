# ~/Alx_DjangoLearnLab/django_blog/blog/views.py

from django.shortcuts import render

def home_page_view(request):
    """
    Simple placeholder view for the blog homepage.
    """
    return render(request, 'blog/home.html', {})
