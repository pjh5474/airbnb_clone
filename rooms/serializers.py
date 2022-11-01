from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Amenity, Room
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer
from reviews.serializers import ReviewSerializer


class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = (
            "name",
            "description",
        )


class RoomListSerializer(ModelSerializer):
    rating = SerializerMethodField()
    is_owner = SerializerMethodField()

    class Meta:
        model = Room
        fields = (
            "name",
            "country",
            "city",
            "price",
            "rating",
            "is_owner",
        )

    def get_rating(self, room):
        return room.rating()

    def get_is_owner(self, room):
        request = self.context["request"]
        return room.owner == request.user


class RoomDetailSerializer(ModelSerializer):

    owner = TinyUserSerializer(read_only=True)

    category = CategorySerializer(
        read_only=True,
    )
    rating = SerializerMethodField()
    is_owner = SerializerMethodField()
    amenities_count = SerializerMethodField()

    class Meta:
        model = Room
        fields = "__all__"

    def get_rating(
        self, room
    ):  # SerializerMethodField를 사용하려면 get_필드명() 형식으로 함수를 만들어야 함
        return room.rating()

    def get_is_owner(self, room):
        request = self.context["request"]
        return room.owner == request.user

    def get_amenities_count(self, room):
        amenities_count = room.amenities.count()
        return amenities_count
