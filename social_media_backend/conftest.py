import json
import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient


@pytest.fixture
def graphql_url():
    return reverse("graphql")


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user(django_user_model):
    def _make(email="test@example.com", password="TestPass123!"):
        return django_user_model.objects.create_user(email=email, password=password)

    return _make


@pytest.fixture
def get_jwt_token(client, graphql_url):
    """
    Returns function that fetches JWT for a given (email, password).
    Usage: token = get_jwt_token(email, password)
    """

    def _get(email, password):
        mutation = f"""
        mutation {{
          tokenAuth(email: "{email}", password: "{password}") {{
            token
          }}
        }}
        """
        resp = client.post(
            graphql_url,
            data=json.dumps({"query": mutation}),
            content_type="application/json",
        )
        data = json.loads(resp.content)
        # If GraphQL errors exist they will be in data["errors"]
        return data["data"]["tokenAuth"]["token"]

    return _get
