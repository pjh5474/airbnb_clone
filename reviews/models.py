from django.db import models
from common.models import CommonModel
from django.conf import settings
from django.core.validators import MaxValueValidator


class Review(CommonModel):

    """Review form a User to a Room or Experience"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
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

    payload = models.TextField()
    rating = models.PositiveIntegerField(
        validators=[MaxValueValidator(5)]
    )  # max value validator is a function that checks if the value is less than or equal to the value you set.

    def __str__(self) -> str:
        return f"Reviewed by {self.user} :: {self.room or self.experience} :: {self.rating} ☆"
