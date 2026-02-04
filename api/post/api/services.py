from django.utils import timezone


def publish_news(news_post):
    news_post.status = 'published'
    news_post.published_at = timezone.now()
    news_post.save(update_fields=['status', 'published_at'])


def increment_news_views(news_post):
    news_post.increment_views()
