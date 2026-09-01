from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import CurrentUser, get_current_user
from app.db.session import get_db
from app.tools.knowledge.contracts import KnowledgeSearchRequest
from app.tools.knowledge.service import search_verified_knowledge

router = APIRouter()

@router.post("/knowledge")
async def search_knowledge(
    payload: KnowledgeSearchRequest,
    db: AsyncSession = Depends(get_db),
    _: CurrentUser = Depends(get_current_user),
):
    return await search_verified_knowledge(db, payload)
