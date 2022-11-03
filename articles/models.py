from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Review(models.Model):
    title = models.CharField(max_length=80)
    addr = models.CharField(max_length=80)
    x = models.CharField(max_length=80, blank=False, null=False)
    y = models.CharField(max_length=80, blank=False, null=False)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    image = ProcessedImageField(
        upload_to="images/",
        blank=True,
        processors=[ResizeToFill(1200, 960)],
        format="JPEG",
        options={"quality": 80},
    )

    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="like_review"
    )


class Comment(models.Model):
    content = models.TextField()
    article = models.ForeignKey(Review, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
