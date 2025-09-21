from fastapi import APIRouter

router = APIRouter()

@router.get("/my_friends")
async def get_my_friends():
    pass
