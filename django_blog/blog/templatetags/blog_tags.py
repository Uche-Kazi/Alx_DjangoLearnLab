from django import template
from django.utils.html import mark_safe # Important for rendering HTML from markdown
from django.db.models import Count # For counting comments
import markdown # You need to install this library

register = template.Library()

@register.filter(name='markdown')
def markdown_format(text):
    """
    Custom template filter to convert Markdown text to HTML.
    Requires the 'markdown' library to be installed.
    Usage: {{ post.body|markdown }}
    """
    return mark_safe(markdown.markdown(text))


@register.simple_tag
def total_comments():
    """
    Returns the total number of comments across all posts.
    Usage: {% total_comments %}
    """
    from ..models import Comment # Import Comment model relative to this file
    return Comment.objects.count()

@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    """
    Displays a list of the latest published posts.
    Usage: {% show_latest_posts 3 %}
    """
    from ..models import Post # Import Post model relative to this file
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}

@register.simple_tag
def get_most_commented_posts(count=5):
    """
    Returns the most commented posts.
    Usage: {% get_most_commented_posts as most_commented_posts %}
    """
    from ..models import Post # Import Post model relative to this file
    return Post.published.annotate(
        total_comments=Count('comments')
    ).order_by('-total_comments')[:count]

