from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
from uuid import uuid4
from datetime import datetime
import os

app = FastAPI(title="Task Board API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============== In-Memory Storage ==============
tasks_db: List[dict] = []


# ============== Pydantic Models ==============
class TaskCreate(BaseModel):
    title: str
    priority: str = "medium"  # low, medium, high
    category: str = "general"  # Unique feature: categories


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None
    category: Optional[str] = None


class TaskResponse(BaseModel):
    id: str
    title: str
    completed: bool
    priority: str
    category: str
    created_at: str
    completed_at: Optional[str] = None


# ============== Helper Functions ==============
def calculate_progress() -> dict:
    """Calculate task completion progress with detailed stats"""
    total = len(tasks_db)
    if total == 0:
        return {"percentage": 0, "completed": 0, "total": 0}

    completed = sum(1 for task in tasks_db if task["completed"])
    percentage = round((completed / total) * 100, 1)

    return {"percentage": percentage, "completed": completed, "total": total}


def get_category_stats() -> dict:
    """Get stats by category - Unique feature"""
    categories = {}
    for task in tasks_db:
        cat = task["category"]
        if cat not in categories:
            categories[cat] = {"total": 0, "completed": 0}
        categories[cat]["total"] += 1
        if task["completed"]:
            categories[cat]["completed"] += 1
    return categories


# ============== API Endpoints ==============


@app.get("/api/tasks")
def get_all_tasks():
    """Get all tasks with progress statistics"""
    # Sort by created_at descending (newest first)
    sorted_tasks = sorted(tasks_db,
                          key=lambda x: x["created_at"],
                          reverse=True)
    return {
        "tasks": sorted_tasks,
        "progress": calculate_progress(),
        "category_stats": get_category_stats()
    }


@app.post("/api/tasks")
def create_task(task: TaskCreate):
    """Create a new task"""
    if not task.title.strip():
        raise HTTPException(status_code=400,
                            detail="Task title cannot be empty")

    new_task = {
        "id": str(uuid4()),
        "title": task.title.strip(),
        "completed": False,
        "priority": task.priority,
        "category": task.category,
        "created_at": datetime.now().isoformat(),
        "completed_at": None
    }
    tasks_db.append(new_task)

    return {
        "task": new_task,
        "progress": calculate_progress(),
        "message": "Task created successfully"
    }


@app.put("/api/tasks/{task_id}/toggle")
def toggle_task_completion(task_id: str):
    """Toggle task completion status"""
    for task in tasks_db:
        if task["id"] == task_id:
            task["completed"] = not task["completed"]
            task["completed_at"] = datetime.now().isoformat(
            ) if task["completed"] else None
            return {
                "task": task,
                "progress": calculate_progress(),
                "message": "Task updated successfully"
            }

    raise HTTPException(status_code=404, detail="Task not found")


@app.put("/api/tasks/{task_id}")
def update_task(task_id: str, task_update: TaskUpdate):
    """Update task details"""
    for task in tasks_db:
        if task["id"] == task_id:
            if task_update.title is not None:
                task["title"] = task_update.title.strip()
            if task_update.completed is not None:
                task["completed"] = task_update.completed
                task["completed_at"] = datetime.now().isoformat(
                ) if task_update.completed else None
            if task_update.priority is not None:
                task["priority"] = task_update.priority
            if task_update.category is not None:
                task["category"] = task_update.category
            return {
                "task": task,
                "progress": calculate_progress(),
                "message": "Task updated successfully"
            }

    raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/api/tasks/{task_id}")
def delete_task(task_id: str):
    """Delete a task"""
    global tasks_db
    original_length = len(tasks_db)
    tasks_db = [task for task in tasks_db if task["id"] != task_id]

    if len(tasks_db) == original_length:
        raise HTTPException(status_code=404, detail="Task not found")

    return {
        "success": True,
        "progress": calculate_progress(),
        "message": "Task deleted successfully"
    }


@app.delete("/api/tasks")
def clear_completed_tasks():
    """Clear all completed tasks - Bonus feature"""
    global tasks_db
    before_count = len(tasks_db)
    tasks_db = [task for task in tasks_db if not task["completed"]]
    deleted_count = before_count - len(tasks_db)

    return {
        "success": True,
        "deleted_count": deleted_count,
        "progress": calculate_progress(),
        "message": f"Cleared {deleted_count} completed tasks"
    }


# ============== Serve Frontend ==============
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "..", "frontend", "static")

@app.get("/")
def serve_frontend():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

if os.path.exists(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")



# ============== Health Check ==============
@app.get("/api/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
