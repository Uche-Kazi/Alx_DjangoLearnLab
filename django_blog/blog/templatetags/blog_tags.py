from django import template
from django.db.models import Count
from ..models import Post

register = template.Library()

@register.simple_tag
def get_most_commented_posts(count=5):
    # This query will now work because the Post model has a 'comments' reverse relation
    # that is automatically created by the new Comment model's ForeignKey field.
    return Post.published.annotate(
        total_comments=Count('comments')
    ).order_by('-total_comments')[:count]
