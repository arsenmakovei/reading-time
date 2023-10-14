from django.conf import settings
from django.db import models


class Book(models.Model):
    """Represents a Book model with its details."""

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publication_year = models.PositiveIntegerField()
    short_description = models.TextField()
    full_description = models.TextField()

    def __str__(self) -> str:
        return self.title


class ReadingSession(models.Model):
    """Represents a reading session model for a specific book by a user."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reading_sessions",
    )
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="reading_sessions"
    )
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return f"Reading session {self.pk} for book: {self.book.title}"
