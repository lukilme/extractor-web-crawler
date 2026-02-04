from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse


class NewsPost(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Rascunho'),
        ('published', 'Publicado'),
        ('archived', 'Arquivado'),
    )
    
    SOURCE_CHOICES = (
        ('manual', 'Manual'),
        ('scraped', 'Web Scraping'),
    )
    
    title = models.CharField(max_length=255, verbose_name='Título')
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    content = models.TextField(verbose_name='Conteúdo')
    summary = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='Resumo'
    )
    
    image = models.ImageField(
        upload_to='news_images/',
        blank=True,
        null=True,
        verbose_name='Imagem'
    )
    
    source_url = models.URLField(
        blank=True,
        null=True,
        verbose_name='URL da Fonte'
    )
    
    source_type = models.CharField(
        max_length=10,
        choices=SOURCE_CHOICES,
        default='manual',
        verbose_name='Tipo de Fonte'
    )
    
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='news_posts',
        verbose_name='Autor'
    )
    
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name='Status'
    )
    
    views_count = models.PositiveIntegerField(default=0, verbose_name='Visualizações')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    published_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Publicado em'
    )
    
    class Meta:
        verbose_name = 'Notícia'
        verbose_name_plural = 'Notícias'
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(fields=['-published_at']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('news:detail', kwargs={'slug': self.slug})
    
    def increment_views(self):
        self.views_count += 1
        self.save(update_fields=['views_count'])


class Comment(models.Model):

    news_post = models.ForeignKey(
        NewsPost,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Notícia'
    )
    
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Autor'
    )
    
    content = models.TextField(verbose_name='Comentário')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    
    is_active = models.BooleanField(default=True, verbose_name='Ativo')
    
    class Meta:
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'Comentário de {self.author.username} em {self.news_post.title}'