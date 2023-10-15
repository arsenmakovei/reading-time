import pytest
from django.utils import timezone

from book.models import Book, ReadingSession


@pytest.mark.django_db
def test_book_model(book):
    assert Book.objects.count() == 1
    assert book.title == "Sample Book"
    assert book.author == "Sample Author"
    assert book.publication_year == 2022
    assert book.short_description == "Short description for the book."
    assert book.full_description == "This is the full description of the book."
    assert str(book) == "Sample Book"


@pytest.mark.django_db
def test_reading_session_model(user, book):
    reading_session = ReadingSession.objects.create(user=user, book=book)
    assert ReadingSession.objects.count() == 1
    assert reading_session.user == user
    assert reading_session.book == book
    assert (
        str(reading_session)
        == f"Reading session {reading_session.pk} for book: Sample Book"
    )

    # Testing end_time field
    end_time = timezone.now()
    reading_session.end_time = end_time
    reading_session.save()
    assert reading_session.end_time == end_time
