from datetime import timedelta

from rest_framework import serializers

from book.models import Book, ReadingSession
from book.utils import calculate_reading_time_for_book


class BookSerializer(serializers.ModelSerializer):
    """Base serializer for the Book model."""

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
    """Serializer for displaying a list of books."""

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
    """Serializer for displaying detailed book information including
    last read date and total reading time."""

    last_read_date = serializers.SerializerMethodField()
    total_reading_time = serializers.SerializerMethodField()

    class Meta(BookSerializer.Meta):
        model = Book
        fields = BookSerializer.Meta.fields + ("last_read_date", "total_reading_time")

    def get_last_read_date(self, obj: Book) -> str | None:
        """Retrieves the last read date of the book
        for the current authenticated user."""
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

    def get_total_reading_time(self, obj: Book) -> str:
        """Retrieves the total reading time of the book
        for the current authenticated user."""
        user = self.context["request"].user

        if user.is_authenticated:
            total_reading_time = calculate_reading_time_for_book(user=user, book=obj)

            if total_reading_time:
                return str(total_reading_time)

        return str(timedelta(0))


class ReadingSessionSerializer(serializers.ModelSerializer):
    """Serializer for the ReadingSession model."""

    class Meta:
        model = ReadingSession
        fields = ("id", "user", "book", "start_time", "end_time")
        read_only_fields = ("id", "user", "book", "start_time", "end_time")
