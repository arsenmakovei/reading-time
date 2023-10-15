import pytest
from django.contrib.auth import get_user_model


User = get_user_model()


@pytest.fixture
def user_data():
    return {"email": "test@example.com", "password": "testpassword"}


@pytest.mark.django_db
def test_create_user(user_data):
    user = User.objects.create_user(**user_data)
    assert user.email == user_data["email"]
    assert user.check_password(user_data["password"])
    assert not user.is_staff
    assert not user.is_superuser


@pytest.mark.django_db
def test_create_superuser(user_data):
    admin_user = User.objects.create_superuser(**user_data)
    assert admin_user.email == user_data["email"]
    assert admin_user.check_password(user_data["password"])
    assert admin_user.is_staff
    assert admin_user.is_superuser


@pytest.mark.django_db
def test_create_user_empty_email(user_data):
    user_data["email"] = ""
    with pytest.raises(ValueError):
        User.objects.create_user(**user_data)


@pytest.mark.django_db
def test_create_superuser_not_staff(user_data):
    user_data["is_staff"] = False
    with pytest.raises(ValueError):
        User.objects.create_superuser(**user_data)


@pytest.mark.django_db
def test_create_superuser_not_superuser(user_data):
    user_data["is_superuser"] = False
    with pytest.raises(ValueError):
        User.objects.create_superuser(**user_data)
