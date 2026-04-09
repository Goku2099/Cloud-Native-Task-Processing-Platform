import time
from datetime import datetime
from .database import tasks_collection

def process_tasks():
    print("Worker started. Waiting for tasks...")

    while True:
        task = tasks_collection.find_one({"status": "pending"})

        if task:
            task_id = task["_id"]
            print(f"Processing task: {task_id}")

            # mark as processing
            tasks_collection.update_one(
                {"_id": task_id},
                {"$set": {"status": "processing"}}
            )

            # simulate heavy work
            time.sleep(5)

            # mark as completed
            tasks_collection.update_one(
                {"_id": task_id},
                {"$set": {
                    "status": "completed",
                    "completed_at": datetime.utcnow()
                }}
            )

            print(f"Task completed: {task_id}")

        else:
            time.sleep(3)  # no task, wait


if __name__ == "__main__":
    process_tasks()
