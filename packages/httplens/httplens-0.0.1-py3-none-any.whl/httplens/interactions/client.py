import aiohttp
from aiohttp.client_reqrep import ClientResponse
import asyncio
from typing import Optional

class APIClient():
    def __init__(self, session : Optional[aiohttp.ClientSession] = None, *session_args, **session_kwargs):
        self.session = session or aiohttp.ClientSession(*session_args, **session_kwargs)



    async def perform_http_task(self, task : str, *args, **kwargs) -> ClientResponse:
        method = getattr(self.session, task)
        response = await method(*args, **kwargs)
        return response


    
    async def close(self):
        await self.session.close()
        
            
            