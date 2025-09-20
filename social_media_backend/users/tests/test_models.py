import pytest
from users.models import User


@pytest.mark.django_db
def test_user_email_is_unique():
    User.objects.create_user(email="test@example.com", password="pass1234")
    with pytest.raises(Exception):
        User.objects.create_user(email="test@example.com", password="pass1234")


@pytest.mark.django_db
def test_username_field_is_email():
    user = User.objects.create_user(email="unique@example.com", password="pass1234")
    assert user.USERNAME_FIELD == "email"
    assert user.email == "unique@example.com"
