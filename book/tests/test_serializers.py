from datetime import timedelta

import pytest
from django.urls import reverse
from django.utils import timezone

from book.models import ReadingSession
from book.utils import calculate_reading_time_for_book


def book_detail_url(book_id: int) -> str:
    return reverse("book:book-detail", args=[book_id])


@pytest.fixture
def reading_session(user, book):
    start_time = timezone.now()
    end_time = start_time + timedelta(hours=2)  # Assuming a reading session of 2 hours
    return ReadingSession.objects.create(
        user=user, book=book, start_time=start_time, end_time=end_time
    )


@pytest.fixture
def reading_session2(user, book):
    start_time = timezone.now() + timedelta(hours=3)
    end_time = start_time + timedelta(hours=1)
    ReadingSession.objects.create(
        user=user, book=book, start_time=start_time, end_time=end_time
    )


@pytest.mark.django_db
def test_get_last_read_date_authenticated(api_client, user, book, reading_session):
    api_client.force_authenticate(user=user)
    url = book_detail_url(book.id)
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data["last_read_date"] == reading_session.end_time


@pytest.mark.django_db
def test_get_last_read_date_unauthenticated(api_client, book):
    url = book_detail_url(book.id)
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data["last_read_date"] is None


@pytest.mark.django_db
def test_get_total_reading_time_authenticated(
    api_client, user, book, reading_session, reading_session2
):
    total_reading_time = calculate_reading_time_for_book(user=user, book=book)

    api_client.force_authenticate(user=user)
    url = book_detail_url(book.id)
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data["total_reading_time"] == str(total_reading_time)


@pytest.mark.django_db
def test_get_total_reading_time_unauthenticated(api_client, book):
    url = book_detail_url(book.id)
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data["total_reading_time"] == str(timedelta(0))
