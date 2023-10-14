import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from book.models import ReadingSession


def start_reading_session_url(book_id: int) -> str:
    return reverse("book:book-start-reading-session", args=[book_id])


def end_reading_session_url(book_id: int) -> str:
    return reverse("book:book-end-reading-session", args=[book_id])


@pytest.fixture
def active_reading_session(user, book):
    return ReadingSession.objects.create(user=user, book=book)


@pytest.fixture
def inactive_reading_session(user, book):
    return ReadingSession.objects.create(
        user=user,
        book=book,
        end_time=timezone.now(),
    )


@pytest.mark.django_db
def test_start_reading_session(api_client, user, book):
    api_client.force_authenticate(user=user)
    url = start_reading_session_url(book.id)
    response = api_client.post(url)
    assert response.status_code == status.HTTP_200_OK
    assert ReadingSession.objects.filter(user=user, book=book, end_time=None).exists()


@pytest.mark.django_db
def test_start_reading_session_with_active_session(
    api_client, user, book, active_reading_session
):
    api_client.force_authenticate(user=user)
    url = start_reading_session_url(book.id)
    response = api_client.post(url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_end_reading_session(api_client, user, book, active_reading_session):
    api_client.force_authenticate(user=user)
    url = end_reading_session_url(book.id)
    response = api_client.post(url)
    assert response.status_code == status.HTTP_200_OK
    active_reading_session.refresh_from_db()
    assert active_reading_session.end_time is not None


@pytest.mark.django_db
def test_end_reading_session_without_active_session(
    api_client, user, book, inactive_reading_session
):
    api_client.force_authenticate(user=user)
    url = end_reading_session_url(book.id)
    response = api_client.post(url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
