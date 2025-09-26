# 🌐 Social Media Backend

This is a **Django + GraphQL** social media backend project built with **Docker**.  
It supports user registration, authentication, posts, comments, and reactions.

The project is part of the **[ALX Project Nexus](https://github.com/roqiaahmed/alx-project-nexus.git)** repository.

---

## 📂 Project Structure

alx-project-nexus/
│── social_media_backend/ # Main Django project
│ ├── users/ # Users app
│ ├── posts/ # Posts app
│ ├── core/ # Core schema
| |── social_media_backend # settings
│ └── ...
│── docker-compose.yml
│── Dockerfile
│── README.md

---

- [Users App README.md](https://github.com/roqiaahmed/alx-project-nexus/blob/main/social_media_backend/users/README.md)
- [Posts App README.md](https://github.com/roqiaahmed/alx-project-nexus/blob/main/social_media_backend/posts/README.md)

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/roqiaahmed/alx-project-nexus.git
cd alx-project-nexus/social_media_backend
```

create .env file with:

```bash
DJANGO_SECRET_KEY= #your django secret key
DB_DRIVER="django.db.backends.postgresql"
PG_DB=social_media # Datebase name
PG_USER=postgres # Datebase user
PG_PASSWORD=password # Datebase password
PG_HOST=db # db for docker. without docker use "localhost"
PG_PORT=5432 # Datebase port
```

### 2️⃣ Run with Docker

- Build and start the containers:

```bash
docker-compose up --build
```

### 3️⃣ Make Migrations

- Inside the container, run:

```bash
docker-compose exec web python manage.py makemigrations users
docker-compose exec web python manage.py makemigrations posts
```

### 4️⃣ Apply Migrations

- Inside the container, run:

```bash
docker-compose exec web python manage.py migrate
```

---

## Running Tests

Run all tests inside the container:

```bash
docker-compose exec web pytest
```

---

## 📌 Apps Included

- ➡️ [Users App](https://github.com/roqiaahmed/alx-project-nexus/blob/main/social_media_backend/users/README.md): Handles registration, login (JWT), and profiles.

- ➡️ [Posts App](https://github.com/roqiaahmed/alx-project-nexus/blob/main/social_media_backend/posts/README.md) : Handles posts, comments, and reactions.

---

### ⚡ Notes

- Uses JWT Authentication (graphql-jwt) for login and authorization.
- Designed for GraphQL-first development.
- Extendable to add more social media features (follows, etc).
