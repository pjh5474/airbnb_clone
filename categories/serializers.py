from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"  # or fields = ("id", "name", "description", "created_at", "updated_at"), exclude = ("id", "created_at", "updated_at")
