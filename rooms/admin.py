from django.contrib import admin
from .models import Room, Amenity


@admin.action(description="Set price to zero")
def reset_price(model_admin, requset, rooms):
    for room in rooms:
        room.price = 0
        room.save()


# admin.action decorator is used to create a custom action
# model_admin is the admin model
# requset is the request that is sent to the server
# rooms(queryset) is the list of rooms that are selected


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):

    actions = (reset_price,)

    list_display = (
        "name",
        "price",
        "kind",
        "rating",
        "total_amenities",
        "owner",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "country",
        "city",
        "pet_friendly",
        "kind",
        "amenities",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    # readonly_fields는 어드민에서 수정할 수 없게 만드는 필드

    search_fields = (
        "name",
        "price",
        "owner__username",  # ForeignKey owner의 username을 검색할 수 있게 함
    )
    # search_fields는 어드민에서 검색할 수 있는 필드
    # ^는 시작하는 단어를 검색할 때 사용 __startswith, ^name, =는 정확히 일치하는 단어를 검색할 때 사용 __exact, =name


#    def total_amenities(self, room):
#        return room.amenities.count()


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "created_at",
        "updated_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )
