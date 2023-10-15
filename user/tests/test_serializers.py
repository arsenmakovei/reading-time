import pytest
from django.contrib.auth import get_user_model

from user.serializers import UserSerializer


@pytest.fixture
def user_data():
    return {
        "email": "test@example.com",
        "password": "testpassword",
        "first_name": "John",
        "last_name": "Doe",
    }


@pytest.fixture
def user(user_data):
    return get_user_model().objects.create_user(**user_data)


@pytest.mark.django_db
def test_user_serializer_create(user_data):
    serializer = UserSerializer(data=user_data)
    assert serializer.is_valid()
    user = serializer.save()
    assert user.email == user_data["email"]
    assert user.check_password(user_data["password"])


@pytest.mark.django_db
def test_user_serializer_update(user, user_data):
    updated_data = {
        "email": "updated@example.com",
        "first_name": "Jane",
        "last_name": "Smith",
    }
    serializer = UserSerializer(instance=user, data=updated_data, partial=True)
    assert serializer.is_valid()
    updated_user = serializer.save()
    assert updated_user.email == updated_data["email"]
    assert updated_user.first_name == updated_data["first_name"]
    assert updated_user.last_name == updated_data["last_name"]


@pytest.mark.django_db
def test_user_serializer_password_update(user, user_data):
    updated_data = {
        "password": "newpassword",
    }
    serializer = UserSerializer(instance=user, data=updated_data, partial=True)
    assert serializer.is_valid()
    updated_user = serializer.save()
    assert updated_user.check_password(updated_data["password"])


@pytest.mark.django_db
def test_user_serializer_invalid_password_too_short(user, user_data):
    updated_data = {
        "password": "test",
    }
    serializer = UserSerializer(instance=user, data=updated_data, partial=True)
    assert not serializer.is_valid()
    assert "password" in serializer.errors


@pytest.mark.django_db
def test_user_serializer_invalid_email(user, user_data):
    updated_data = {
        "email": "invalidemail",
    }
    serializer = UserSerializer(instance=user, data=updated_data, partial=True)
    assert not serializer.is_valid()
    assert "email" in serializer.errors
