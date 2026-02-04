

from django.db import models
from django.conf import settings


class ScraperSource(models.Model):

    STATUS_CHOICES = (
        ('active', 'Ativo'),
        ('inactive', 'Inativo'),
        ('error', 'Erro'),
    )
    
    name = models.CharField(max_length=200, verbose_name='Nome da Fonte')
    url = models.URLField(verbose_name='URL')
    
    title_selector = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        help_text='Seletor CSS para título (ex: h1.title)',
        verbose_name='Seletor de Título'
    )

    content_selector = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        help_text='Seletor CSS para conteúdo (ex: div.content)',
        verbose_name='Seletor de Conteúdo'
    )

    
    image_selector = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        help_text='Seletor CSS para imagem (ex: img.featured)',
        verbose_name='Seletor de Imagem'
    )
    
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active',
        verbose_name='Status'
    )
    
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='scraper_sources',
        verbose_name='Criado por'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    last_scraped_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Última execução'
    )
    
    success_count = models.PositiveIntegerField(
        default=0,
        verbose_name='Execuções bem-sucedidas'
    )
    
    error_count = models.PositiveIntegerField(
        default=0,
        verbose_name='Execuções com erro'
    )
    
    class Meta:
        verbose_name = 'Fonte de Scraping'
        verbose_name_plural = 'Fontes de Scraping'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.url}"


class ScraperJob(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pendente'),
        ('running', 'Executando'),
        ('completed', 'Concluído'),
        ('failed', 'Falhou'),
    )
    
    source = models.ForeignKey(
        ScraperSource,
        on_delete=models.CASCADE,
        related_name='jobs',
        verbose_name='Fonte'
    )
    
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Status'
    )
    
    started_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='scraper_jobs',
        verbose_name='Iniciado por'
    )
    
    items_scraped = models.PositiveIntegerField(
        default=0,
        verbose_name='Itens coletados'
    )
    
    items_published = models.PositiveIntegerField(
        default=0,
        verbose_name='Itens publicados'
    )
    
    error_message = models.TextField(
        blank=True,
        verbose_name='Mensagem de erro'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Execução de Scraping'
        verbose_name_plural = 'Execuções de Scraping'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Job #{self.id} - {self.source.name} ({self.get_status_display()})"