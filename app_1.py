from typing import List, Optional
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Модель задачи

class Task(BaseModel):
    title: str
    description: str
    completed: bool = False

# Хранилище задач
tasks = {}
task_id_counter = 1


@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return list(tasks.values())


@app.get("/tasks/{id}", response_model=Task)
def get_task(id: int):
    if id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[id]


@app.post("/tasks", response_model=Task)
def create_task(task: Task):
    global task_id_counter
    tasks[task_id_counter] = task
    task_id_counter += 1
    return task


@app.put("/tasks/{id}", response_model=Task)
def update_task(id: int, updated_task: Task):
    if id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    tasks[id] = updated_task
    return updated_task


@app.delete("/tasks/{id}")
def delete_task(id: int):
    if id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    del tasks[id]
    return {"detail": "Task deleted successfully"}


if __name__ == "main":
    uvicorn.run("app_1:app", host="127.0.0.1", port=8000, reload=True)
