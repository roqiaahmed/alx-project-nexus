import json
from django.contrib.auth import get_user_model

User = get_user_model()


def test_creat_post_with_auth_user(
    client, graphql_url, get_jwt_token, create_post_mutation, create_user, db
):
    post = create_post_mutation("my new post")
    email = "me@example.com"
    password = "StrongPass123!"
    create_user(email=email, password=password)
    token = get_jwt_token(email, password)
    headers = {"HTTP_AUTHORIZATION": f"Bearer {token}"}
    resp = client.post(
        graphql_url,
        data=json.dumps({"query": post}),
        content_type="application/json",
        **headers,
    )
    assert resp.status_code == 200
    data = json.loads(resp.content)
    assert data["data"]["createPost"]["post"]["contentText"] == "my new post"
    assert data["data"]["createPost"]["post"]["author"]["email"] == "me@example.com"


def test_create_post_unauthenticated(client, graphql_url, create_post_mutation, db):
    mutation = create_post_mutation("unauth post")
    resp = client.post(
        graphql_url,
        data=json.dumps({"query": mutation}),
        content_type="application/json",
    )
    data = json.loads(resp.content)
    assert "errors" in data
    assert data["data"]["createPost"] is None


def test_query_all_posts(
    client, graphql_url, get_jwt_token, create_post_mutation, create_user, db
):
    email = "user@example.com"
    password = "StrongPass123!"
    user = create_user(email=email, password=password)
    token = get_jwt_token(email, password)
    headers = {"HTTP_AUTHORIZATION": f"Bearer {token}"}

    # Create 2 posts
    client.post(
        graphql_url,
        data=json.dumps({"query": create_post_mutation("post 1")}),
        content_type="application/json",
        **headers,
    )
    client.post(
        graphql_url,
        data=json.dumps({"query": create_post_mutation("post 2")}),
        content_type="application/json",
        **headers,
    )

    # Fetch all posts
    query = """
    query {
      allPosts {
        contentText
        author { email }
      }
    }
    """
    resp = client.post(
        graphql_url,
        data=json.dumps({"query": query}),
        content_type="application/json",
    )
    data = json.loads(resp.content)
    posts = data["data"]["allPosts"]
    assert len(posts) >= 2
    assert any(p["contentText"] == "post 1" for p in posts)
    assert any(p["contentText"] == "post 2" for p in posts)


def test_query_me_posts(
    client, graphql_url, get_jwt_token, create_post_mutation, create_user, db
):
    email = "me@example.com"
    password = "StrongPass123!"
    create_user(email=email, password=password)
    token = get_jwt_token(email, password)
    headers = {"HTTP_AUTHORIZATION": f"Bearer {token}"}

    # Create a post
    client.post(
        graphql_url,
        data=json.dumps({"query": create_post_mutation("personal post")}),
        content_type="application/json",
        **headers,
    )

    query = """
    query {
      me {
        posts {
          contentText
        }
      }
    }
    """
    resp = client.post(
        graphql_url,
        data=json.dumps({"query": query}),
        content_type="application/json",
        **headers,
    )
    data = json.loads(resp.content)
    posts = data["data"]["me"]["posts"]
    assert len(posts) == 1
    assert posts[0]["contentText"] == "personal post"


def test_create_comment_with_auth_user(
    client, graphql_url, create_comment_mutation, create_post
):
    post_id, headers, email = create_post(
        "original post", email="commenter@example.com"
    )

    mutation = create_comment_mutation("my first comment", post_id=post_id)
    resp = client.post(
        graphql_url,
        data=json.dumps({"query": mutation}),
        content_type="application/json",
        **headers,
    )

    data = json.loads(resp.content)

    assert resp.status_code == 200
    assert data["data"]["createComment"]["comment"]["contentText"] == "my first comment"
    assert data["data"]["createComment"]["comment"]["user"]["email"] == email
    assert data["data"]["createComment"]["comment"]["post"]["id"] == post_id


def test_create_reaction_with_auth_user(
    client, graphql_url, create_reaction_mutation, create_post
):
    post_id, headers, email = create_post(
        "post for reaction", email="reactor@example.com"
    )

    mutation = create_reaction_mutation("LIKE", post_id=post_id)
    resp = client.post(
        graphql_url,
        data=json.dumps({"query": mutation}),
        content_type="application/json",
        **headers,
    )

    data = json.loads(resp.content)
    assert resp.status_code == 200
    assert data["data"]["createReaction"]["reaction"]["states"] == "LIKE"
    assert data["data"]["createReaction"]["reaction"]["user"]["email"] == email
    assert data["data"]["createReaction"]["reaction"]["post"]["id"] == post_id
