from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from post.models import NewsPost, Comment
from .serializers import NewsPostSerializer, CommentSerializer
from .services import publish_news, increment_news_views


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class NewsPostViewSet(viewsets.ModelViewSet):
    serializer_class = NewsPostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_queryset(self):
        qs = NewsPost.objects.select_related('author').prefetch_related('comments')
        if self.action == 'list':
            return qs.filter(status='published')
        return qs

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        increment_news_views(instance)
        return super().retrieve(request, *args, **kwargs)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def publish(self, request, pk=None):
        publish_news(self.get_object())
        return Response({'status': 'publicado'})


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(
            is_active=True,
            news_post__status='published'
        ).select_related('author', 'news_post')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
