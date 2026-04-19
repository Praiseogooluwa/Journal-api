# 📓 Journal API

A backend API that allows developers to **log their learning, track journal entries, and organize notes using tags**.

This project was built as a **learning project** to understand authentication systems, multi-user platforms, database relationships, and real backend problem solving.

---

# 📚 What I Learned Building This

Building this project helped me understand important backend concepts:

🔐 **JWT Authentication**
How login systems work, how tokens are generated, and how APIs verify users.

👥 **Multi-User Platforms**
Ensuring each user can only access **their own data**.

🗄️ **Database Relationships**

* **One-to-Many** → `Users → Entries`
* **Many-to-Many** → `Entries ↔ Tags`

🛡️ **Protected Routes**
Using **FastAPI dependency injection** to protect endpoints.

🧠 **Debugging & Problem Solving**
Fixing dependency issues, solving errors, and thinking through backend edge cases.

---

# ✨ Features

🔐 **User authentication with JWT**

* Register new users
* Login and receive authentication token

🔑 **Password hashing**

* Secure password storage using **bcrypt**

📝 **Journal entries**

Users can create entries with:

* Title
* Content
* Mood
* Date

🏷️ **Tagging system**

Add tags like:

python
fastapi
debugging
backend

🔎 **Filter entries by tag**

🔒 **User-specific data**

Each user can **only access their own entries**.

---

# 🛠️ Tech Stack

| Technology    | Purpose                        |
| ------------- | ------------------------------ |
| ⚡ FastAPI     | Backend framework              |
| 🗄️ SQLite    | Local database                 |
| 🐘 PostgreSQL | Production database            |
| 🔗 SQLAlchemy | ORM for models & relationships |
| 📦 Pydantic   | Data validation                |
| 🔐 bcrypt     | Password hashing               |
| 🎫 JWT        | Authentication tokens          |

---

# 📂 Project Structure

dev-journal-api/

├── app/
│   ├── main.py
│   ├── database.py

│   ├── auth/
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── router.py
│   │   └── utils.py

│   ├── entries/
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── router.py

│   └── tags/
│       ├── models.py
│       ├── schemas.py
│       └── router.py

├── .env
├── Procfile
└── requirements.txt

---

# ⚙️ Running Locally

### 1️⃣ Clone the repository

git clone https://github.com/your-username/dev-journal-api.git
cd dev-journal-api

---

### 2️⃣ Create virtual environment

python -m venv venv

Activate it:

Mac/Linux

source venv/bin/activate

Windows

venv\Scripts\activate

---

### 3️⃣ Install dependencies

pip install -r requirements.txt

---

### 4️⃣ Create `.env` file

SECRET_KEY=your-secret-key-here

---

### 5️⃣ Run the server

uvicorn app.main:app --reload

---

### 6️⃣ Open API docs

FastAPI automatically generates documentation.

http://127.0.0.1:8000/docs

---

# 📡 API Endpoints

## 🔐 Auth

| Method | Endpoint       | Description             |
| ------ | -------------- | ----------------------- |
| POST   | /auth/register | Register a user         |
| POST   | /auth/login    | Login and get JWT token |

---

## 📝 Entries

| Method | Endpoint       | Description      |
| ------ | -------------- | ---------------- |
| POST   | /entries/      | Create entry     |
| GET    | /entries/entry | Get all entries  |
| GET    | /entries/{id}  | Get single entry |
| PUT    | /entries/{id}  | Update entry     |
| DELETE | /entries/{id}  | Delete entry     |

---

## 🏷️ Tags

| Method | Endpoint                      | Description           |
| ------ | ----------------------------- | --------------------- |
| POST   | /entries/{id}/tags            | Add tag to entry      |
| DELETE | /entries/{id}/tags/{tag_name} | Remove tag            |
| GET    | /entries/filter?tag=python    | Filter entries by tag |

---

# 🔑 Environment Variables

| Variable     | Description                                |
| ------------ | ------------------------------------------ |
| SECRET_KEY   | Secret key used to sign JWT tokens         |
| DATABASE_URL | PostgreSQL connection URL (for deployment) |

---

# 🚀 Deployment

The project is deployed using:

☁️ **Railway** — backend hosting
🐘 **PostgreSQL** — production database

Railway automatically provides the **DATABASE_URL** environment variable.

---

# 💡 Possible Future Improvements

📊 Analytics on journal activity
🔍 Search through entries
🌐 Frontend dashboard
📱 Mobile friendly interface
📅 Entry reminders

---

# 👨‍💻 Author

Built as a learning project while exploring **backend engineering, authentication systems, and database design**.
