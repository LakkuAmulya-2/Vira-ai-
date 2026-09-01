from uuid import uuid4
from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router
from app.core.config import settings
from app.core.rate_limit import rate_limit
app=FastAPI(title="Vira AI API",version="1.0.0",openapi_url=f"{settings.api_v1_prefix}/openapi.json")
app.add_middleware(CORSMiddleware,allow_origins=settings.cors_origins,allow_credentials=True,allow_methods=["GET","POST","PUT","PATCH","DELETE"],allow_headers=["Authorization","Content-Type","X-Request-ID"])
@app.middleware("http")
async def security_pipeline(request:Request,call_next):
    request.state.request_id=request.headers.get("X-Request-ID",str(uuid4()))
    if request.url.path.startswith(settings.api_v1_prefix):await rate_limit(request)
    response=await call_next(request);response.headers["X-Request-ID"]=request.state.request_id
    return response
app.include_router(api_router,prefix=settings.api_v1_prefix)
@app.get("/healthz",include_in_schema=False)
async def healthz()->dict[str,str]:return {"status":"ok"}
@app.get("/readyz",include_in_schema=False)
async def readyz()->dict[str,str]:return {"status":"ready","environment":settings.app_env}
