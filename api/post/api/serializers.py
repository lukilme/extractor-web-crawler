from rest_framework import serializers
from post.models import NewsPost, Comment


class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = [
            'id',
            'news_post',
            'author',
            'author_username',
            'content',
            'created_at',
            'updated_at',
            'is_active',
        ]
        read_only_fields = ['author', 'created_at', 'updated_at']


class NewsPostSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = NewsPost
        fields = [
            'id',
            'title',
            'slug',
            'content',
            'summary',
            'image',
            'source_url',
            'source_type',
            'author',
            'author_username',
            'status',
            'views_count',
            'created_at',
            'updated_at',
            'published_at',
            'comments',
        ]
        read_only_fields = [
            'slug',
            'author',
            'views_count',
            'created_at',
            'updated_at',
        ]
