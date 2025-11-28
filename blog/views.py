from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import BlogPost


def blog_list(request):
    posts = BlogPost.objects.filter(published=True)
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'posts': page_obj,
    }
    return render(request, 'blog/blog_list.html', context)


def post_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, published=True)
    recent_posts = BlogPost.objects.filter(published=True).exclude(id=post.id)[:3]
    
    context = {
        'post': post,
        'recent_posts': recent_posts,
    }
    return render(request, 'blog/post_detail.html', context)

