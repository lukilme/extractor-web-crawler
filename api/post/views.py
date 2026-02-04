from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from .models import NewsPost, Comment
from .forms import CommentForm


@login_required
def feed_view(request):
    news_list = NewsPost.objects.filter(
        status='published'
    ).select_related('author').annotate(
        comments_count=Count('comments')
    )

    search_query = request.GET.get('q', '')
    if search_query:
        news_list = news_list.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(summary__icontains=search_query)
        )
    
    paginator = Paginator(news_list, 10)
    page_number = request.GET.get('page')
    news_page = paginator.get_page(page_number)
    
    context = {
        'news_page': news_page,
        'search_query': search_query,
    }
    
    return render(request, 'news/feed.html', context)


@login_required
def news_detail_view(request, slug):

    news = get_object_or_404(
        NewsPost.objects.select_related('author'),
        slug=slug,
        status='published'
    )
    
    news.increment_views()
    
    comments = news.comments.filter(
        is_active=True
    ).select_related('author').order_by('-created_at')
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.news_post = news
            comment.save()
            messages.success(request, 'Comentário adicionado com sucesso!')
            return redirect('news:detail', slug=slug)
    else:
        form = CommentForm()
    
    context = {
        'news': news,
        'comments': comments,
        'form': form,
    }
    
    return render(request, 'news/detail.html', context)


@login_required
def delete_comment_view(request, comment_id):

    comment = get_object_or_404(Comment, id=comment_id)
    
    if request.user == comment.author or request.user.is_admin_user():
        news_slug = comment.news_post.slug
        comment.delete()
        messages.success(request, 'Comentário removido com sucesso!')
        return redirect('news:detail', slug=news_slug)
    else:
        messages.error(request, 'Você não tem permissão para remover este comentário.')
        return redirect('news:feed')