from fastapi import FastAPI, Depends
from datetime import datetime
from .database import tasks_collection
from .schemas import TaskCreate
from .auth import get_current_user

app = FastAPI(title="Task Service")

@app.post("/tasks")
def create_task(
    task: TaskCreate,
    user_email: str = Depends(get_current_user)
):
    task_data = {
        "task_type": task.task_type,
        "user_email": user_email,
        "status": "pending",
        "created_at": datetime.utcnow()
    }

    result = tasks_collection.insert_one(task_data)

    return {
        "message": "Task created",
        "task_id": str(result.inserted_id)
    }


@app.get("/tasks")
def list_tasks():
    tasks = []
    for task in tasks_collection.find():
        task["_id"] = str(task["_id"])
        tasks.append(task)
    return tasks
