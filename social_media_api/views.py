from django.http import HttpResponse


def hello_world_view(request):
    """
    A simple view that returns an HTTP response with "Hello, World!".
    This is a temporary view to test the server and URL configuration.
    """
    return HttpResponse("<h1>Hello, World! Welcome to the Social Media API.</h1>")
