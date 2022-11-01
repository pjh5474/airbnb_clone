from django.db import models
from django.conf import settings
from common.models import CommonModel
from django.core.validators import MinValueValidator

# Create your models here.
class Room(CommonModel):

    """Room Model Definition"""

    class RoomKindChoices(models.TextChoices):
        ENTIRE_PLACE = ("entire_place", "Entire Place")
        PRIVATE_ROOM = ("private_room", "Private Room")
        SHARED_ROOM = ("shared_room", "Shared Room")

    name = models.CharField(
        max_length=180,
        default="",
    )
    country = models.CharField(
        max_length=50,
        default="한국",
    )
    city = models.CharField(
        max_length=80,
        default="서울",
    )
    price = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    rooms = models.PositiveIntegerField()
    toilets = models.PositiveIntegerField()
    description = models.TextField()
    address = models.CharField(
        max_length=250,
    )
    pet_friendly = models.BooleanField(
        default=True,
    )
    kind = models.CharField(
        max_length=20,
        choices=RoomKindChoices.choices,
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        # related_name="rooms",  # related_name은 역참조할 때 사용하는 이름, 기본은 _set
    )

    amenities = models.ManyToManyField(
        "rooms.Amenity",
        # related_name="rooms",
    )

    category = models.ForeignKey(
        settings.AUTH_CATEGORY_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        # related_name="rooms",
    )

    def __str__(self) -> str:  # __str__은 객체를 문자열로 표현할 때 사용하는 함수, -> str은 반환값이 str이라는 뜻
        return self.name

    def total_amenities(self):
        return self.amenities.count()

    def rating(self):
        count = self.review_set.count()
        if count == 0:
            return "No Reviews"
        else:
            total_rating = 0
            for review in self.review_set.all().values("rating"):  # values는 딕셔너리 형태로 반환
                total_rating += review[
                    "rating"
                ]  # 딕셔너리 형태로 반환되기 때문에 review["rating"]으로 접근
            return round(total_rating / count, 2)  # round는 소수점 자리수를 지정할 수 있음


class Amenity(CommonModel):

    """Amenity Model Definition"""

    name = models.CharField(
        max_length=150,
    )
    description = models.CharField(
        max_length=150,
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = "Amenities"  # 복수형으로 표현하고 싶을 때
