# ~/Alx_DjangoLearnLab/django_blog/blog/views.py

from django.shortcuts import render

# A simple placeholder view for the homepage
def home_page_view(request):
    return render(request, 'blog/home.html', {})
