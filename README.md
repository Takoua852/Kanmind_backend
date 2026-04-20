# Kanmind Backend

## 📌 Project Description
This is the backend of the Kanmind project built with Django.  
It handles the API, database models, and backend logic.  
The frontend is maintained in a separate repository.

## 🛠 Technologies
- Python 3.x
- Django
- SQLite (default) 
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
```

### 5. Apply migrations
```bash
python manage.py migrate
```

### 6. Run the development server
```bash
python manage.py runserver
```
Server will be available at:
[text](http://127.0.0.1:8000/)


## 📂 Project Structure
```
Kanmind_backend/
├── core/                 # Project settings, URLs, middleware
├── kanban_app/           # Board management logic
├── tasks_app/            # Task management (CRUD, comments, assignments)
├── users_auth_app/       # Authentication & user management
├── manage.py             # Django management script
├── requirements.txt      # Project dependencies
└── README.md             # Documentation
```

## 💡 Notes
- The `.gitignore` file ensures that sensitive data and the virtual environment are not included in the repository.
- For production, configure your database and secret keys securely.
---

Feel free to adjust project names, paths, or add more details as needed!


## 📚 API Endpoints

🔑 Authentication
| Method | Endpoint           | Description                             |
| ------ | ------------------ | --------------------------------------- |
| POST   | /api/registration/ | Register a new user                     |
| POST   | /api/login/        | User login                              |
| GET    | /api/email-check/  | Check if an email is already registered |

📋 Boards
| Method | Endpoint          | Description            |
| ------ | ----------------- | ---------------------- |
| GET    | /api/boards/      | List all boards        |
| POST   | /api/boards/      | Create a new board     |
| GET    | /api/boards/{id}/ | Retrieve board by ID   |
| PATCH  | /api/boards/{id}/ | Update board (partial) |
| DELETE | /api/boards/{id}/ | Delete board           |

✅ Tasks                                                                                 
| Method | Endpoint                               | Description                        |
| ------ | -------------------------------------- | ---------------------------------- |
| GET    | /api/tasks/assigned-to-me/             | Tasks assigned to current user     |
| GET    | /api/tasks/reviewing/                  | Tasks under review by current user |
| POST   | /api/tasks/                            | Create a new task                  |
| PATCH  | /api/tasks/{id}/                       | Update task (partial)              |
| DELETE | /api/tasks/{id}/                       | Delete task                        |
| GET    | /api/tasks/{id}/comments/              | List comments for a task           |
| POST   | /api/tasks/{id}/comments/              | Add a comment                      |
| DELETE | /api/tasks/{id}/comments/{comment_id}/ | Delete a comment                   |


## 🔐 Environment Notes
Never commit your .env file
Keep your SECRET_KEY private
Use proper environment variables in production

## 💡 Notes
.gitignore excludes sensitive files and virtual environments
SQLite is used by default for development


## 📜 License

This project is licensed under the [MIT License](LICENSE).