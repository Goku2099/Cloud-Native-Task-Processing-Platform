from pydantic import BaseModel
from datetime import datetime

class TaskCreate(BaseModel):
    task_type: str
    user_email: str

class TaskResponse(BaseModel):
    task_id: str
    task_type: str
    user_email: str
    status: str
    created_at: datetime
