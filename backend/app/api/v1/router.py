from fastapi import APIRouter

from app.api.v1.routes import knowledge, students

api_router = APIRouter()
api_router.include_router(students.router, prefix="/students", tags=["students"])
api_router.include_router(knowledge.router, prefix="/knowledge", tags=["knowledge"])
