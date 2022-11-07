from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail


class User(AbstractUser):
    followings = models.ManyToManyField(
        "self", symmetrical=False, related_name="followers"
    )


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    image = ProcessedImageField(
        upload_to="images/",
        blank=True,
        processors=[Thumbnail(200, 300)],
        format="JPEG",
        options={"quality": 50},
    )
    status_message = models.CharField(
        max_length=100,
        blank=True,
    )

    position_choices = [
        ("먹보", None),
        ("한식", "한식"),
        ("분식", "분식"),
        ("중식", "중식"),
        ("일식", "일식"),
        ("양식", "양식"),
        ("아시안", "아시안"),
        ("카페/디저트", "카페/디저트"),
    ]

    position = models.CharField(
        max_length=10,
        choices=position_choices,
        default="선택",
    )
