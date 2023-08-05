import functools
import asyncio
from concurrent import futures
from ..errors import *


def with_executor(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        try:
            partial = functools.partial(function, *args, **kwargs)
            loop = asyncio.get_event_loop()
            return loop.run_in_executor(futures.ThreadPoolExecutor(), partial)
        except Exception as e:
            raise ExecutorError(e)

    
    return wrapper