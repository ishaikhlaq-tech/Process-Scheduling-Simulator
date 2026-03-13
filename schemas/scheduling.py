from pydantic import BaseModel
from typing import List, Optional, Union

# INPUT
class Process(BaseModel):
    pid: Union[int, str] # Allow both just in case
    arrival_time: int
    burst_time: int
    priority: Optional[int] = 0

class SchedulingRequest(BaseModel):
    processes: List[Process]

# OUTPUT
class GanttBlock(BaseModel):
    pid: Union[int, str]


class SchedulingResponse(BaseModel):
    algorithm: str
    gantt_chart: List[GanttBlock]
    average_waiting_time: float
    average_turnaround_time: float

class ComparisonResponse(BaseModel):
    results: List[SchedulingResponse]
    best_algorithm: str
    worst_algorithm: str