from fastapi import APIRouter

router = APIRouter(prefix="/task", tags=["task"])

@router.get("/")
def all_tasks():
    pass

@router.get("/{task_id}")
def task_by_id(task_id: int):
    pass

@router.post("/create")
def create_task():
    pass

@router.put("/update")
def update_task():
    pass

@router.delete("/delete")
def delete_task():
    pass

