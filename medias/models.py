from django.db import models
from common.models import CommonModel
from django.conf import settings


class Photo(CommonModel):

    file = models.ImageField()
    description = models.CharField(
        max_length=140,
    )
    room = models.ForeignKey(
        settings.AUTH_ROOM_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    experience = models.ForeignKey(
        settings.AUTH_EXPERIENCE_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return "Photo File"


class Video(CommonModel):

    file = models.FileField()
    experience = models.OneToOneField(
        settings.AUTH_EXPERIENCE_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return "Video File"
