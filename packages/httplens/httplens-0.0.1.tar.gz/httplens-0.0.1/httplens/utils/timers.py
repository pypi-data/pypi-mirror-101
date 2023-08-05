import time #ik its not async i am terribly sorry
from httplens.ext.decorators import with_executor
from httplens.errors import *

class Runtime():
    def __init__(self):
        self.start_time = None
        self.end_tme = None

    @with_executor
    def start_clock(self) -> None:
        self.start_time = time.perf_counter()


    @with_executor
    def end_clock(self) -> None:
        self.end_time = time.perf_counter()

    
    @with_executor
    def calculate_runtime(self) -> float:
        if self.start_time == None or self.end_time == None:
            raise RuntimeAsyncException("Cannot calculate runtime. You may have forgotten to start and/or end the clock")
        return float(self.end_time - self.start_time)



    