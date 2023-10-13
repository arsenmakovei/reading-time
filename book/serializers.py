from datetime import timedelta

from django.db.models import Sum, F
from rest_framework import serializers

from book.models import Book, ReadingSession


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "author",
            "publication_year",
            "short_description",
            "full_description",
        )


class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "author",
            "publication_year",
            "short_description",
        )


class BookDetailSerializer(serializers.ModelSerializer):
    last_read_date = serializers.SerializerMethodField()
    total_reading_time = serializers.SerializerMethodField()

    class Meta(BookSerializer.Meta):
        model = Book
        fields = BookSerializer.Meta.fields + ("last_read_date", "total_reading_time")

    def get_last_read_date(self, obj):
        current_user = self.context["request"].user

        if current_user.is_authenticated:
            last_reading_session = (
                ReadingSession.objects.filter(book=obj, user=current_user)
                .order_by("-end_time")
                .first()
            )

            if last_reading_session:
                return last_reading_session.end_time

        return None

    def get_total_reading_time(self, obj):
        user = self.context["request"].user

        if user.is_authenticated:
            total_reading_time = ReadingSession.objects.filter(
                book=obj, user=user
            ).aggregate(total_time=Sum(F("end_time") - F("start_time")))["total_time"]

            if total_reading_time:
                return str(total_reading_time)

        return str(timedelta(0))


class ReadingSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingSession
        fields = ("id", "user", "book", "start_time", "end_time")
        read_only_fields = ("id", "user", "book", "start_time", "end_time")
