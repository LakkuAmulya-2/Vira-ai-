from fastapi import APIRouter
from app.api.v1.routes import agents, career, ingestion, journey, knowledge, recommendations, student_intelligence, students, workflows

api_router = APIRouter()
api_router.include_router(students.router, prefix="/students", tags=["students"])
api_router.include_router(student_intelligence.router, prefix="/student-intelligence", tags=["student-intelligence"])
api_router.include_router(career.router, prefix="/career", tags=["career"])
api_router.include_router(knowledge.router, prefix="/knowledge", tags=["knowledge"])
api_router.include_router(ingestion.router, prefix="/ingestion", tags=["ingestion"])
api_router.include_router(recommendations.router, prefix="/recommendations", tags=["recommendations"])
api_router.include_router(agents.router, prefix="/agents", tags=["agents"])
api_router.include_router(journey.router, prefix="/journey", tags=["journey"])
api_router.include_router(workflows.router, prefix="/workflows", tags=["workflows"])
