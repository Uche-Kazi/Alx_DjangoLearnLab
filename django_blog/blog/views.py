from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Post, Comment
from .forms import CommentForm
from django.db.models import Q

class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 3

    def get_queryset(self):
        # Start with the base queryset of published posts.
        queryset = super().get_queryset()

        # Check for a search query.
        if 'q' in self.request.GET:
            # Get the search term and apply filters to both content and tags.
            q = self.request.GET['q']
            queryset = queryset.filter(
                Q(content__icontains=q) | Q(tags__name__icontains=q)
            ).distinct()
        
        return queryset

def post_detail(request, slug):
    template_name = 'post_detail.html'
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, template_name, {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})
