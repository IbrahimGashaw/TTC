from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import BlogPost, BlogCategory


def blog_list(request):
    posts = BlogPost.objects.filter(published=True)
    search_query = request.GET.get('q', '')
    category_slug = request.GET.get('category', '')
    tag = request.GET.get('tag', '')

    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(excerpt__icontains=search_query) |
            Q(meta_tags__icontains=search_query)
        )
    if category_slug:
        posts = posts.filter(category__slug=category_slug)
    if tag:
        posts = posts.filter(meta_tags__icontains=tag)

    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'posts': page_obj,
        'categories': BlogCategory.objects.all(),
        'search_query': search_query,
        'active_category': category_slug,
        'active_tag': tag,
    }
    return render(request, 'blog/blog_list.html', context)


def post_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, published=True)
    recent_posts = BlogPost.objects.filter(published=True).exclude(id=post.id)[:3]

    context = {
        'post': post,
        'recent_posts': recent_posts,
        'categories': BlogCategory.objects.all(),
    }
    return render(request, 'blog/post_detail.html', context)

