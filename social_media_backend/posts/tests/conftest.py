import json
import pytest


@pytest.fixture
def create_post_mutation():
    def _get(content="Hello world!"):
        return f"""
        mutation {{
          createPost(content: "{content}") {{
            post {{
              id
              contentText
              author {{
                email
              }}
            }}
          }}
        }}
        """

    return _get


@pytest.fixture
def me_posts_query():
    return """
    query {
      me {
        posts {
          id
          contentText
        }
      }
    }
    """


@pytest.fixture
def create_comment_mutation():
    def _get(content="Nice post!", post_id=1):
        return f"""
        mutation {{
          createComment(contentText: "{content}", post: {post_id}) {{
            comment {{
              id
              contentText
              user {{
                email
              }}
              post {{
                id
              }}
            }}
          }}
        }}
        """

    return _get


@pytest.fixture
def create_reaction_mutation():
    def _get(state="LIKE", post_id=1):
        return f"""
        mutation {{
          createReaction(states: "{state}", post: {post_id}) {{
            reaction {{
              id
              states
              user {{
                email
              }}
              post {{
                id
              }}
            }}
          }}
        }}
        """

    return _get


@pytest.fixture
def auth_headers(client, graphql_url, get_jwt_token, create_user):
    """Return headers for an authenticated user."""

    def _make(email="user@example.com", password="StrongPass123!"):
        create_user(email=email, password=password)
        token = get_jwt_token(email, password)
        return {"HTTP_AUTHORIZATION": f"Bearer {token}"}, email, password

    return _make


@pytest.fixture
def create_post(client, graphql_url, create_post_mutation, auth_headers):
    """Create a post for a given user and return (post_id, headers, email)."""

    def _make(content="default post", email="poster@example.com"):
        headers, user_email, _ = auth_headers(email=email)
        mutation = create_post_mutation(content)
        resp = client.post(
            graphql_url,
            data=json.dumps({"query": mutation}),
            content_type="application/json",
            **headers,
        )
        data = json.loads(resp.content)
        post_id = data["data"]["createPost"]["post"]["id"]
        return post_id, headers, user_email

    return _make
