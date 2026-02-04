# apps/scraper/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from post.models import NewsPost
from .models import ScraperSource, ScraperJob
from .forms import ScraperSourceForm
from .services import run_scraping_for_source
from django.utils import timezone

def is_admin(user):
    """Verificar se usuário é administrador"""
    return user.is_authenticated and user.is_admin_user()


@login_required
@user_passes_test(is_admin)
def dashboard_view(request):

    total_sources = ScraperSource.objects.count()
    active_sources = ScraperSource.objects.filter(status='active').count()
    total_jobs = ScraperJob.objects.count()
    successful_jobs = ScraperJob.objects.filter(status='completed').count()
    
    recent_jobs = ScraperJob.objects.select_related('source', 'started_by')[:10]
    
    recent_scraped_news = NewsPost.objects.filter(
        source_type='scraped'
    ).select_related('author')[:5]
    
    success_rate = 0
    if total_jobs > 0:
        success_rate = round((successful_jobs / total_jobs) * 100)

    context = {
        'total_sources': total_sources,
        'active_sources': active_sources,
        'total_jobs': total_jobs,
        'successful_jobs': successful_jobs,
        'success_rate': success_rate,
        'recent_jobs': recent_jobs,
        'recent_scraped_news': recent_scraped_news,
    }

    
    return render(request, 'scraper/dashboard.html', context)


@login_required
@user_passes_test(is_admin)
def sources_list_view(request):
    sources = ScraperSource.objects.all().select_related('created_by')
    
    paginator = Paginator(sources, 15)
    page_number = request.GET.get('page')
    sources_page = paginator.get_page(page_number)
    
    return render(request, 'scraper/sources_list.html', {
        'sources_page': sources_page
    })



@login_required
@user_passes_test(is_admin)
def source_create_view(request):
    if request.method == 'POST':
        form = ScraperSourceForm(request.POST)
        if form.is_valid():
            source = form.save(commit=False)
            source.created_by = request.user

            is_manual = form.cleaned_data.get('manual_mode')

            if is_manual:
                source.title_selector = None
                source.content_selector = None
                source.image_selector = None

            source.save()

            if is_manual:
                NewsPost.objects.create(
                    title=form.cleaned_data['manual_title'],
                    content=form.cleaned_data['manual_content'],
                    source_url=source.url,
                    source_type='manual',
                    author=request.user,
                    status='published',
                    published_at=timezone.now(),
                )

                messages.success(
                    request,
                    'Fonte criada e notícia publicada manualmente com sucesso!'
                )
            else:
                messages.success(
                    request,
                    'Fonte de scraping criada com sucesso!'
                )

            return redirect('scraper:sources_list')
    else:
        form = ScraperSourceForm()

    return render(request, 'scraper/source_form.html', {
        'form': form,
        'title': 'Nova Fonte de Scraping'
    })


@login_required
@user_passes_test(is_admin)
def source_edit_view(request, source_id):
    source = get_object_or_404(ScraperSource, id=source_id)
    
    if request.method == 'POST':
        form = ScraperSourceForm(request.POST, instance=source)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fonte atualizada com sucesso!')
            return redirect('scraper:sources_list')
    else:
        form = ScraperSourceForm(instance=source)
    
    return render(request, 'scraper/source_form.html', {
        'form': form,
        'title': 'Editar Fonte',
        'source': source
    })


@login_required
@user_passes_test(is_admin)
def source_delete_view(request, source_id):
    """
    Deletar fonte de scraping
    """
    source = get_object_or_404(ScraperSource, id=source_id)
    source.delete()
    messages.success(request, 'Fonte removida com sucesso!')
    return redirect('scraper:sources_list')


@login_required
@user_passes_test(is_admin)
def run_scraping_view(request, source_id):
    source = get_object_or_404(ScraperSource, id=source_id)

    is_manual = not source.title_selector and not source.content_selector

    if is_manual:
        try:
            result = run_manual_publication_for_source(source, request.user)

            messages.success(
                request,
                f'Publicação manual realizada com sucesso! Notícia publicada: {result.title}'
            )
        except Exception as e:
            messages.error(
                request,
                f'Erro na publicação manual: {str(e)}'
            )

        return redirect('scraper:dashboard')

    result = run_scraping_for_source(source.id, request.user)

    if result.get('success'):
        messages.success(
            request,
            f'Scraping executado com sucesso! Notícia publicada: {result["news_post"].title}'
        )
    else:
        messages.error(
            request,
            f'Erro no scraping: {result.get("error")}'
        )

    return redirect('scraper:dashboard')



@login_required
@user_passes_test(is_admin)
def jobs_history_view(request):
    jobs = ScraperJob.objects.select_related(
        'source',
        'started_by'
    ).order_by('-created_at')
    
    status_filter = request.GET.get('status')
    if status_filter:
        jobs = jobs.filter(status=status_filter)
    
    paginator = Paginator(jobs, 20)
    page_number = request.GET.get('page')
    jobs_page = paginator.get_page(page_number)
    
    return render(request, 'scraper/jobs_history.html', {
        'jobs_page': jobs_page,
        'status_filter': status_filter
    })


@login_required
@user_passes_test(is_admin)
def news_management_view(request):
    news_list = NewsPost.objects.select_related('author').order_by('-created_at')
    
    status_filter = request.GET.get('status')
    if status_filter:
        news_list = news_list.filter(status=status_filter)
    
    source_filter = request.GET.get('source')
    if source_filter:
        news_list = news_list.filter(source_type=source_filter)
    
    paginator = Paginator(news_list, 20)
    page_number = request.GET.get('page')
    news_page = paginator.get_page(page_number)
    
    return render(request, 'scraper/news_management.html', {
        'news_page': news_page,
        'status_filter': status_filter,
        'source_filter': source_filter
    })


@login_required
@user_passes_test(is_admin)
def news_edit_view(request, news_id):
    from apps.news.forms import NewsPostForm
    
    news = get_object_or_404(NewsPost, id=news_id)
    
    if request.method == 'POST':
        form = NewsPostForm(request.POST, request.FILES, instance=news)
        if form.is_valid():
            form.save()
            messages.success(request, 'Notícia atualizada com sucesso!')
            return redirect('scraper:news_management')
    else:
        form = NewsPostForm(instance=news)
    
    return render(request, 'scraper/news_edit.html', {
        'form': form,
        'news': news
    })


@login_required
@user_passes_test(is_admin)
def news_delete_view(request, news_id):
    news = get_object_or_404(NewsPost, id=news_id)
    title = news.title
    news.delete()
    messages.success(request, f'Notícia "{title}" removida com sucesso!')
    return redirect('scraper:news_management')