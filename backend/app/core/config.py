from functools import lru_cache
from pydantic import field_validator
from pydantic_settings import BaseSettings,SettingsConfigDict
class Settings(BaseSettings):
 model_config=SettingsConfigDict(env_file=".env",case_sensitive=False)
 app_env:str="development";api_v1_prefix:str="/api/v1";database_url:str;jwt_secret:str;jwt_algorithm:str="HS256";cors_origins:list[str]|str="http://localhost:3000";redis_url:str|None=None;langgraph_checkpointer_url:str|None=None;rate_limit_per_minute:int=120
 @field_validator("jwt_secret")
 @classmethod
 def validate_secret(cls,value:str)->str:
  if len(value)<32:raise ValueError("JWT_SECRET must be at least 32 characters")
  return value
 @field_validator("cors_origins",mode="before")
 @classmethod
 def parse_origins(cls,value):return value.split(",") if isinstance(value,str) else value
@lru_cache
def get_settings()->Settings:return Settings()
settings=get_settings()
