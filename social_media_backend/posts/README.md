# 📌 Posts App

The **Posts** app provides functionality for creating, managing, and interacting with user-generated posts in the social media project.  
It also supports **comments** and **reactions** on posts.

---

## 🚀 Features

- **Posts**

  - Create, query, and list posts
  - Each post is associated with an authenticated user (author)
  - Supports timestamps (`created_at`, `updated_at`)

- **Comments**

  - Authenticated users can add comments to posts
  - Includes `content_text`, timestamps, and user reference
  - Displayed as part of post details

- **Reactions**

  - Authenticated users can react to posts
  - Each reaction has a `state` (e.g., like, dislike, etc.)
  - Linked to both user and post

- **GraphQL Integration**
  - Mutations for `createPost`, `createComment`, `createReaction`
  - Queries for fetching posts (with nested author, comments, and reactions)

---

## 🗂️ Models Overview

- **Post**

  - `content_text`: Text content of the post
  - `author`: FK to `User`
  - `created_at`, `updated_at`

- **Comment**

  - `content_text`: Text content of the comment
  - `user`: FK to `User`
  - `post`: FK to `Post`
  - `created_at`, `updated_at`

- **Reaction**
  - `states`: String field for reaction type (e.g., "like")
  - `user`: FK to `User`
  - `post`: FK to `Post`

---

## 🧪 Tests

The app includes integration tests for:

- ✅ Creating a post (with authenticated user)
- ✅ Querying all posts
- ✅ Querying posts by the current user (`me`)
- ✅ Creating a comment (authenticated)
- ✅ Creating a reaction (authenticated)

Run tests with:

```bash
pytest posts/
```

---

## 📌 Example GraphQL Usage

- Create Post

```bash
mutation {
  createPost(content: "My first post!") {
    post {
      id
      contentText
      author {
        email
      }
    }
  }
}
```

- Create Comment

```bash
mutation {
  createComment(post: 1, contentText: "Great post!") {
    comment {
      id
      contentText
      user {
        email
      }
    }
  }
}
```

- Create Reaction

```bash
mutation {
  createReaction(post: 1, states: "like") {
    reaction {
      id
      states
      user {
        email
      }
    }
  }
}
```

- Query All Posts

```bash
query {
  allPosts {
    id
    contentText
    author {
      email
    }
    comments {
      contentText
    }
    reactions {
      states
    }
  }
}
```

---

## ⚡ Notes

- All mutations require an authenticated user (JWT token).
- Comments and reactions are nested inside posts, so no separate query types were added.
- The app is designed to be extendable (e.g., add reaction types, comment threads).
