import redis.asyncio as aioredis
from src.Config import config


JTI_EXPIRE=3600
token_blocklist=aioredis.from_url(config.REDIS_URL)
async def add_jti_to_blocklist(jti:str)->None:
  await token_blocklist.set(name=jti,value='blackd',ex=JTI_EXPIRE)



async def token_in_blocklist(jti:str):
  result=await token_blocklist.get(jti)
  return result is not None 
  