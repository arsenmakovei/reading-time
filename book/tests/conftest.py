import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from book.models import Book


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return get_user_model().objects.create_user(
        email="test@example.com",
        password="testpassword",
    )


@pytest.fixture
def book():
    return Book.objects.create(
        title="Sample Book",
        author="Sample Author",
        publication_year=2022,
        short_description="Short description for the book.",
        full_description="This is the full description of the book.",
    )
