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
    position_choices = [
        ("한식", "한식"),
        ("분식", "분식"),
        ("중식", "중식"),
        ("일식", "일식"),
        ("양식", "양식"),
        ("아시안", "아시안"),
        ("카페/디저트", "카페/디저트"),
        ("기타", None),
    ]

    position = models.CharField(
        max_length=10,
        choices=position_choices,
        default="선택",
    )
    menu = models.TextField()
    contact = models.CharField(max_length=14, blank=True)
    homepage = models.CharField(max_length=40, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    x = models.CharField(max_length=80, blank=False, null=False)
    y = models.CharField(max_length=80, blank=False, null=False)
    image = ProcessedImageField(
        upload_to="images/",
        blank=True,
        processors=[ResizeToFill(1200, 960)],
        format="JPEG",
        options={"quality": 80},
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    like_art_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="like_review"
    )


class Comment(models.Model):
    content = models.TextField()
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    grade = models.FloatField(validators=[MinValueValidator(0.0),MaxValueValidator(5.0)])
    credit = models.TextField()
    image = ProcessedImageField(
        upload_to="images/",
        blank=True,
        processors=[ResizeToFill(1200, 960)],
        format="JPEG",
        options={"quality": 80},
    )
