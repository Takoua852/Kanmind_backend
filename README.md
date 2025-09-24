# Kanmind Backend

## 📌 Project Description
This is the backend of the Kanmind project built with Django.  
It handles the API, database models, and backend logic.  
The frontend is maintained in a separate repository.

## 🛠 Technologies
- Python 3.x
- Django
- SQLite (default) or PostgreSQL (if configured)
- python-dotenv

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/Takoua852/Kanmind_backend.git
cd Kanmind_backend
```

### 2. Create and activate a virtual environment
```bash
python -m venv env
env\Scripts\activate # On Windows
source env/bin/activate  # On Linux/Mac
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Create a `.env` file in the project root and add your settings (example):
```
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
```

### 5. Apply migrations
```bash
python manage.py migrate
```

### 6. Run the development server
```bash
python manage.py runserver
```

<!-- ## 🧪 Running Tests
```bash
python manage.py test
``` -->

## 📂 Project Structure
```
Kanmind_backend/
├── core/                 # Global settings, URLs, middleware
├── kanban_app/           # Kanban board logic (boards, columns, etc.)
├── tasks_app/            # Task management (CRUD, comments, assignments)
├── users_auth_app/       # Authentication & user management
├── manage.py             # Django management script
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation
```

## 💡 Notes
- The `.gitignore` file ensures that sensitive data and the virtual environment are not included in the repository.
- For production, configure your database and secret keys securely.
- More documentation will be added soon.

---

Feel free to adjust project names, paths, or add more details as needed!


## 📚 API Endpoints

| Method | Endpoint                               | Description                             |

🔑 Authentication

| POST   | /api/registration/                     | Register a new user                     |
| POST   | /api/login/                            | User login                              |
| GET    | /api/email-check/                      | Check if an email is already registered |

📋 Boards

| GET    | /api/boards/                           | List all boards                         |
| POST   | /api/boards/                           | Create a new board                      |
| GET    | /api/boards/{id}/                      | Retrieve board by ID                    |
| PATCH  | /api/boards/{id}/                      | Partially update board by ID            |
| DELETE | /api/boards/{id}/                      | Delete board by ID                      |

✅ Tasks

| GET    | /api/tasks/assigned-to-me/             | List tasks assigned to the current user |
| GET    | /api/tasks/reviewing/                  | List tasks the current user is reviewing|
| POST   | /api/tasks/                            | Create a new task                       |
| PATCH  | /api/tasks/{id}/                       | Partially update task by ID             |
| DELETE | /api/tasks/{id}/                       | Delete task by ID                       |
| GET    | /api/tasks/{id}/comments/              | List comments for a specific task       |
| POST   | /api/tasks/{id}/comments/              | Add a comment to a specific task        |
| DELETE | /api/tasks/{id}/comments/{comment_id}/ | Delete a specific comment from a task   |

📜 License

This project is licensed under the [MIT License](LICENSE).