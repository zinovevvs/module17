from fastapi import APIRouter

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/")
def all_users():
    pass

@router.get("/{user_id}")
def user_by_id(user_id: int):
    pass

@router.post("/create")
def create_user():
    pass

@router.put("/update")
def update_user():
    pass

@router.delete("/delete")
def delete_user():
    pass
