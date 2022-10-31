from django.db import models
from common.models import CommonModel
from django.conf import settings


class ChattingRoom(CommonModel):

    """Chat Room Model Definition"""

    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
    )

    def __str__(self) -> str:
        return "Chatting Room."


class Message(CommonModel):

    """Message Model Definition"""

    text = models.TextField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    room = models.ForeignKey(
        "direct_messages.ChattingRoom",
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return f"{self.user} says: {self.text}"
