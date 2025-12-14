### loom video
```https://www.loom.com/share/ab10f728364e47e5bed672aa5446e423```

# ✨ Task Board – Full Stack Application

A modern, animated **Task Board application** built with **FastAPI** and **React (CDN-based)**.  
It helps you stay organized with task priorities, categories, progress tracking, and a beautiful UI.

---

## 🚀 Features

### ✅ Core Features
- Create, update, delete tasks
- Mark tasks as completed
- Progress tracking with percentage bar
- Clear all completed tasks
- In-memory storage (no database required)

### 🌟 Unique Enhancements
- 📂 Task categories (Work, Personal, Health, Learning, etc.)
- 🚦 Task priorities (Low, Medium, High)
- 📊 Category-wise task statistics
- 🎉 Confetti celebration on 100% completion
- 🎨 Glassmorphism UI with Tailwind CSS
- ⚡ Smooth animations and transitions

---

## 🛠 Tech Stack

### Backend
- **FastAPI**
- **Uvicorn**
- **Python 3.11**

### Frontend
- **React 18 (CDN)**
- **Tailwind CSS**
- **Babel (in-browser compilation)**
- **Canvas Confetti**

---

## 📁 Project Structure

fluid.ai/
│
├── backend/
│   ├── main.py
|   ├── requirements.txt
|   ├── pyproject.toml
|   └── uv.lock
│
├── frontend/
│   ├── static/
│       └── index.html
│
├── render.yaml
└── README.md


---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/chimt4chi/fluid.ai.git
cd backend
```

### 2. Create Virtual Environment (Recommended)
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Backend Dependencies
```bash
pip install fastapi uvicorn
```
You should see:
```Uvicorn running on http://127.0.0.1:8000```

open:
```
http://127.0.0.1:8000/
```

### Available Endpoints
Method	Endpoint	Description
1. `GET	/api/tasks	Get all tasks + progress`
2. `POST	/api/tasks	Create a new task`
3. `PUT	/api/tasks/{id}	Update task`
4. `PUT	/api/tasks/{id}/toggle	Toggle completion`
5. `DELETE	/api/tasks/{id}	Delete task`
6. `DELETE	/api/tasks	Clear completed tasks`
7. `GET	/api/health	Health check`