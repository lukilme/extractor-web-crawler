from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('comum', 'Usuário Comum'),
        ('admin', 'Administrador'),
    )
    
    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        default='comum',
        verbose_name='Tipo de Usuário'
    )
    
    bio = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='Biografia'
    )
    
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name='Avatar'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['-date_joined']
    
    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"
    
    def is_admin_user(self):
        """Verifica se o usuário é administrador"""
        return self.user_type == 'admin' or self.is_superuser