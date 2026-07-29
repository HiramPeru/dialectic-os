from fastapi import APIRouter
from app.intelligence.providers import get_llm_status

router = APIRouter()

@router.get('/health')
def health():
    return {
        'status': 'ok',
        'llm': get_llm_status(),
    }
