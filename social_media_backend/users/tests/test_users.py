import json
import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


def test_register_user_via_graphql(client, graphql_url, db):
    mutation = """
    mutation {
      registerUser(
        email: "newuser@example.com",
        password: "NewPass123!"
      ) {
        user {
          id
          email
        }
      }
    }
    """
    resp = client.post(
        graphql_url,
        data=json.dumps({"query": mutation}),
        content_type="application/json",
    )
    assert resp.status_code == 200
    data = json.loads(resp.content)
    assert "errors" not in data
    assert data["data"]["registerUser"]["user"]["email"] == "newuser@example.com"
    assert User.objects.filter(email="newuser@example.com").exists()


def test_login_and_me_query(client, graphql_url, create_user, get_jwt_token, db):
    # create user
    email = "me@example.com"
    password = "StrongPass123!"
    create_user(email=email, password=password)

    # login / token
    token = get_jwt_token(email, password)
    assert token is not None and token != ""

    # now call `me` with the JWT in headers
    query = """
    query {
      me {
        email
        firstName
        lastName
      }
    }
    """
    headers = {"HTTP_AUTHORIZATION": f"Bearer {token}"}
    resp = client.post(
        graphql_url,
        data=json.dumps({"query": query}),
        content_type="application/json",
        **headers,
    )
    assert resp.status_code == 200
    data = json.loads(resp.content)
    assert "errors" not in data
    assert data["data"]["me"]["email"] == email


def test_update_profile_mutation(client, graphql_url, create_user, get_jwt_token, db):
    # create & login
    email = "update@example.com"
    password = "PassUpdate123!"
    user = create_user(email=email, password=password)
    token = get_jwt_token(email, password)

    # update profile (authenticated)
    mutation = """
    mutation {
      updateProfile(firstName: "Updated", bio: "Hello testing!") {
        user {
          email
          firstName
          bio
        }
      }
    }
    """
    headers = {"HTTP_AUTHORIZATION": f"Bearer {token}"}
    resp = client.post(
        graphql_url,
        data=json.dumps({"query": mutation}),
        content_type="application/json",
        **headers,
    )
    assert resp.status_code == 200
    data = json.loads(resp.content)
    assert "errors" not in data
    assert data["data"]["updateProfile"]["user"]["firstName"] == "Updated"

    # Confirm DB changed
    user.refresh_from_db()
    assert user.first_name == "Updated"
    assert user.bio == "Hello testing!"
