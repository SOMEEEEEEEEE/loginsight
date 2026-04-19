from fastapi import APIRouter
from query.services.result_service import get_result

router = APIRouter()

@router.get("/results/{task_id}")
def fetch_result(task_id: str):
    return get_result(task_id)