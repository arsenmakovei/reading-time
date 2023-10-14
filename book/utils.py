from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db.models import Sum, F, QuerySet
from django.utils import timezone

from book.models import ReadingSession, Book


def calculate_total_reading_time(reading_sessions: QuerySet[ReadingSession]):
    return reading_sessions.aggregate(total_time=Sum(F("end_time") - F("start_time")))[
        "total_time"
    ]


def calculate_reading_time_for_book(user: get_user_model, book: Book) -> timedelta:
    reading_sessions = ReadingSession.objects.filter(book=book, user=user)
    total_reading_time = calculate_total_reading_time(reading_sessions)

    return total_reading_time


def calculate_reading_time_in_last_days(user: get_user_model, days: int) -> timedelta:
    days_ago = timezone.now() - timedelta(days=days)
    reading_sessions = ReadingSession.objects.filter(
        user=user, start_time__gte=days_ago
    )
    total_reading_time = calculate_total_reading_time(reading_sessions)

    return total_reading_time
