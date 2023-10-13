from datetime import timedelta

from celery import shared_task
from django.contrib.auth import get_user_model
from django.db.models import Sum, F
from django.utils import timezone

from book.models import ReadingSession


@shared_task
def collect_reading_statistics():
    users = get_user_model().objects.all()

    for user in users:
        seven_days_ago = timezone.now() - timedelta(days=7)
        seven_days_reading_sessions = ReadingSession.objects.filter(
            user=user, start_time__gte=seven_days_ago
        )
        total_reading_time_7_days = seven_days_reading_sessions.aggregate(
            total_time=Sum(F("end_time") - F("start_time"))
        )["total_time"]

        thirty_days_ago = timezone.now() - timedelta(days=30)
        thirty_days_reading_sessions = ReadingSession.objects.filter(
            user=user, start_time__gte=thirty_days_ago
        )
        total_reading_time_30_days = thirty_days_reading_sessions.aggregate(
            total_time=Sum(F("end_time") - F("start_time"))
        )["total_time"]

        if total_reading_time_7_days and total_reading_time_30_days:
            user.total_reading_time_7_days = total_reading_time_7_days
            user.total_reading_time_30_days = total_reading_time_30_days
            user.save()
