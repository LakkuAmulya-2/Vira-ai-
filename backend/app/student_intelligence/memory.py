from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.student_intelligence import StudentMemory

async def upsert_memory(db:AsyncSession,student_id:str,namespace:str,memory_key:str,value:dict,source:str="STUDENT",confidence:float=1.0)->StudentMemory:
    row=await db.scalar(select(StudentMemory).where(StudentMemory.student_id==student_id,StudentMemory.namespace==namespace,StudentMemory.memory_key==memory_key))
    if row is None:
        row=StudentMemory(student_id=student_id,namespace=namespace,memory_key=memory_key,value=value,source=source,confidence=confidence);db.add(row)
    else:
        row.value=value;row.source=source;row.confidence=confidence
    await db.commit();await db.refresh(row);return row
