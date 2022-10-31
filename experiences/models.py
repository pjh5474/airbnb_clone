from django.db import models
from common.models import CommonModel
from django.conf import settings


class Experience(CommonModel):

    """Experience Model Definition"""

    country = models.CharField(
        max_length=50,
        default="한국",
    )
    city = models.CharField(
        max_length=80,
        default="서울",
    )
    name = models.CharField(
        max_length=250,
    )
    host = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    price = models.PositiveIntegerField()
    address = models.CharField(
        max_length=250,
    )
    start = models.TimeField()
    end = models.TimeField()
    description = models.TextField()
    perks = models.ManyToManyField(
        "experiences.Perk",
    )

    category = models.ForeignKey(
        settings.AUTH_CATEGORY_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )  # models.SET_NULL: 카테고리가 삭제되면 해당 카테고리를 가진 모든 모델의 카테고리를 null로 바꿔줌

    def __str__(self) -> str:
        return self.name


class Perk(CommonModel):

    """What is included in the experience"""

    name = models.CharField(
        max_length=100,
    )
    detail = models.CharField(
        max_length=250,
        blank=True,
        default="",
    )
    explanation = models.TextField(
        blank=True,
        default="",
    )

    def __str__(self):
        return self.name
