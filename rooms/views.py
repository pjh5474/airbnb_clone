from rest_framework.views import APIView
from .models import Amenity, Room
from .serializers import AmenitySerializer, RoomListSerializer, RoomDetailSerializer
from rest_framework.response import Response
from rest_framework.exceptions import (
    NotFound,
    NotAuthenticated,
    ParseError,
    PermissionDenied,
)
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_200_OK
from categories.models import Category
from django.db import transaction
from reviews.serializers import ReviewSerializer


class Amenities(APIView):
    def get(self, request):
        all_amenities = Amenity.objects.all()
        serializer = AmenitySerializer(
            all_amenities,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = AmenitySerializer(data=request.data)
        if serializer.is_valid():
            new_amenity = serializer.save()
            return Response(
                AmenitySerializer(new_amenity).data,
            )
        else:
            return Response(serializer.errors)


class AmenityDetail(APIView):
    def get_object(self, pk):
        try:
            return Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        return Response(AmenitySerializer(self.get_object(pk)).data)

    def put(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(
            amenity,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_amenity = serializer.save()
            return Response(AmenitySerializer(updated_amenity).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        amenity = self.get_object(pk)
        amenity.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class Rooms(APIView):
    def get(self, request):
        all_rooms = Room.objects.all()
        serializer = RoomListSerializer(
            all_rooms,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)

    def post(self, request):
        if request.user.is_authenticated:
            serializer = RoomDetailSerializer(data=request.data)
            if serializer.is_valid():
                category_pk = request.data.get("category")
                if not category_pk:
                    raise ParseError("Category is required")
                try:
                    category = Category.objects.get(pk=category_pk)
                    if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                        raise ParseError("Category is not a room")
                except Category.DoesNotExist:
                    raise ParseError("Category does not exist")
                try:
                    with transaction.atomic():  # This is to make sure that if one of the following fails, the whole transaction fails
                        new_room = serializer.save(
                            owner=request.user,
                            category=category,
                        )
                        amenities = request.data.get("amenities")
                        for amenity_pk in amenities:
                            amenity = Amenity.objects.get(pk=amenity_pk)
                            new_room.amenities.add(
                                amenity
                            )  # many to many relationship, so we use add
                        serializer = RoomDetailSerializer(new_room)
                        return Response(serializer.data)
                except Exception:
                    raise ParseError("Amenity does not exist")
            else:
                return Response(serializer.errors)
        else:
            raise NotAuthenticated


class RoomDetail(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        serializer = RoomDetailSerializer(
            room,
            context={"request": request},
        )  # context is used to get the request in the serializer
        return Response(serializer.data)

    def put(self, request, pk):
        room = self.get_object(pk)
        if not request.user.is_authenticated:
            raise NotAuthenticated
        if room.owner != request.user:
            raise PermissionDenied

        serializer = RoomDetailSerializer(
            room,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            new_category_pk = request.data.get("category")
            if new_category_pk:
                try:
                    new_category = Category.objects.get(pk=new_category_pk)
                    if new_category.kind == Category.CategoryKindChoices.EXPERIENCES:
                        raise ParseError("This category is not a room")
                except Category.DoesNotExist:
                    raise ParseError("This category does not exist")
            try:
                with transaction.atomic():
                    if new_category_pk:
                        room = serializer.save(category=new_category)
                    else:
                        room = serializer.save()
                    amenities = request.data.get("amenities")
                    if amenities:
                        room.amenities.clear()
                        for amenity_pk in amenities:
                            new_amenity = Amenity.objects.get(pk=amenity_pk)
                            room.amenities.add(new_amenity)
                    serializer = RoomDetailSerializer(
                        room,
                        context={"request": request},
                    )
                    return Response(serializer.data)
            except Exception:
                raise ParseError("These amenities do not exist")
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        room = self.get_object(pk)
        if not request.user.is_authenticated:
            raise NotAuthenticated
        if room.owner != request.user:
            raise PermissionDenied
        room.delete()
        return Response(status=HTTP_200_OK)


class RoomReviews(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = request.query_params.get(
                "page", 1
            )  # page is the query parameter, 1 is the default value
            page = int(page)
        except ValueError:
            page = 1
        room = self.get_object(pk)
        page_size = 5
        serializer = ReviewSerializer(
            room.review_set.all()[(page - 1) * page_size : page * page_size],
            many=True,
        )
        return Response(serializer.data)


class RoomAmenities(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = request.query_params.get(
                "page", 1
            )  # page is the query parameter, 1 is the default value
            page = int(page)
        except ValueError:
            page = 1
        room = self.get_object(pk)
        page_size = 5
        serializer = AmenitySerializer(
            room.amenities.all()[(page - 1) * page_size : page * page_size],
            many=True,
        )  # many=True means that there are many amenities
        return Response(serializer.data)
