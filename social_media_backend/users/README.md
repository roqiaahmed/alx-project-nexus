# Users App

The **Users app** handles authentication and user management for the project.  
It is built with **Django**, **Graphene-Django**, and **django-graphql-jwt** to provide a JWT-based authentication system.

---

## 🚀 Features

- Custom User model (email-based login)
- Register new users
- Authenticate with JWT tokens
- Refresh & verify tokens
- Query the currently authenticated user (`me`)

---

## 🔑 GraphQL Operations

- Register a New User

```bash
    mutation {
    registerUser(
        email: "user@example.com",
        password: "StrongPass123!"
    ) {
        user {
        id
        email
        }
    }
}
```

- Login & Get Token

```bash
mutation {
  tokenAuth(email: "user@example.com", password: "StrongPass123!") {
    token
  }
}
```

- Query Current User

```bash
query {
  me {
    id
    email
  }
}
```

- Update Profile

```bash
mutation {
  updateProfile(firstName: "Roqia", bio: "Backend dev learning GraphQL") {
    user {
      id
      email
      firstName
      lastName
      bio
      avatar
    }
  }
}
```

## All authenticated requests must include the token:

```
Authorization: JWT <your_token_here>
```
