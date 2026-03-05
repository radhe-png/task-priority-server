from fastapi import APIRouter
import logging

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.get("/health")
def check_status():
    logger.info("Server is running on port 8000")
    return {"status": "running..."}