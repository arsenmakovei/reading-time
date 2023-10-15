from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone

from book.models import Book, ReadingSession
from book.tasks import collect_reading_statistics
from book.utils import calculate_reading_time_in_last_days


def create_reading_session(
    user: get_user_model, book: Book, days_ago: int, duration_hours: int
) -> None:
    start_time = timezone.now() - timedelta(days=days_ago)
    end_time = start_time + timedelta(hours=duration_hours)
    ReadingSession.objects.create(
        user=user, book=book, start_time=start_time, end_time=end_time
    )


@pytest.fixture
def reading_session1(user, book):
    create_reading_session(user=user, book=book, days_ago=1, duration_hours=2)


@pytest.fixture
def reading_session2(user, book):
    create_reading_session(user=user, book=book, days_ago=10, duration_hours=1)


@pytest.mark.django_db
def test_collect_reading_statistics(user, book, reading_session1, reading_session2):
    total_reading_time_7_days = calculate_reading_time_in_last_days(user=user, days=7)
    total_reading_time_30_days = calculate_reading_time_in_last_days(user=user, days=30)

    collect_reading_statistics()
    user.refresh_from_db()
    assert user.total_reading_time_7_days == total_reading_time_7_days
    assert user.total_reading_time_30_days == total_reading_time_30_days
