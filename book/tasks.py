from celery import shared_task
from django.contrib.auth import get_user_model

from book.utils import calculate_reading_time_in_last_days


@shared_task
def collect_reading_statistics() -> None:
    """Celery task calculates the total reading time for each user
    based on their ReadingSession records and updates the user objects with
    the total reading time for the last 7 and 30 days respectively."""
    users = get_user_model().objects.all()

    for user in users:
        total_reading_time_7_days = calculate_reading_time_in_last_days(
            user=user, days=7
        )
        total_reading_time_30_days = calculate_reading_time_in_last_days(
            user=user, days=30
        )

        if total_reading_time_7_days and total_reading_time_30_days:
            user.total_reading_time_7_days = total_reading_time_7_days
            user.total_reading_time_30_days = total_reading_time_30_days
            user.save()
