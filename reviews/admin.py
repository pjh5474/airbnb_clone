from django.contrib import admin
from .models import Review


class WordFilter(admin.SimpleListFilter):
    title = "Filter by Word!"
    parameter_name = "word"

    def lookups(self, request, model_admin):
        return [
            ("good", "Good"),
            ("great", "Great"),
            ("awesome", "Awesome"),
            ("tazo", "Tazo"),
        ]

    def queryset(self, request, reviews):
        word = self.value()
        if word:
            return reviews.filter(payload__contains=word)
        else:
            return reviews

    # def queryset(self, request, queryset): # queryset is the list of reviews, request is the request object


class GoodReviewFilter(admin.SimpleListFilter):
    title = "Good or Bad Review!"
    parameter_name = "Goodscore"

    def lookups(self, request, model_admin):
        return [
            ("good", "☆☆☆ 이상"),
            ("bad", "☆☆ 이하"),
        ]

    def queryset(self, request, reviews):
        word = self.value()
        if word == "good":
            return reviews.filter(rating__gte=3)
        elif word == "bad":
            return reviews.filter(rating__lt=3)
        else:
            return reviews


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "payload",
    )
    list_filter = (
        "rating",
        "user__is_host",
        "room__category",
        "room__pet_friendly",
        WordFilter,
        GoodReviewFilter,
    )
