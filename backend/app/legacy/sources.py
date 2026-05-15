from fastapi import APIRouter
router = APIRouter()
SOURCES = [
 {'name':'Reuters','class':'fact_core'},
 {'name':'AP','class':'fact_core'},
 {'name':'Xinhua','class':'china_state'},
 {'name':'Al Jazeera','class':'global_south'},
 {'name':'TASS','class':'russia_state'}
]
@router.get('/')
def list_sources():
    return SOURCES
