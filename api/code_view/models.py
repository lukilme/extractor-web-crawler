from django.db import models
from django.conf import settings
from news_collected.models import Category


# Create your models here.
#
class CollectionScript(models.Model):
    # EXTRACTION_TYPE_CHOICES = [
    #     ("html", "HTML"),
    #     ("api", "API"),
    #     ("rss", "RSS"),
    # ]

    name = models.CharField(max_length=150)
    description = models.TextField()
    example_url = models.URLField()
    # extraction_type = models.CharField(max_length=20, choices=EXTRACTION_TYPE_CHOICES)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="collection_scripts",
    )
    is_active = models.BooleanField(default=True)
    schedule = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name
