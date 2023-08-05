from io import BytesIO
from .timers import Runtime

async def create_buffer(byts : bytes) -> BytesIO:
    buffer = BytesIO(byts)
    buffer.seek(0)
    return buffer