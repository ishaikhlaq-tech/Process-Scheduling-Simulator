from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schemas.scheduling import SchedulingRequest, SchedulingResponse, ComparisonResponse

# Import algorithms
from algorithms.fcfs import fcfs_scheduling
from algorithms.sjf import sjf_scheduling
from algorithms.srtf import srtf_scheduling
from algorithms.priority import priority_scheduling
from algorithms.round_robin import round_robin_scheduling
from services.simulator import run_all_algorithms

app = FastAPI(title="CPU Scheduling Simulator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- COMPATIBILITY FIX ---
# Safely convert Pydantic models to dicts (Works on V1 and V2)
def clean_processes(processes):
    # This handles both Pydantic V1 (.dict()) and V2 (.model_dump())
    cleaned = []
    for p in processes:
        if hasattr(p, 'model_dump'):
            cleaned.append(p.model_dump())
        else:
            cleaned.append(p.dict())
    return cleaned

@app.post("/schedule/fcfs")
def fcfs(req: SchedulingRequest):
    if not req.processes: raise HTTPException(400, "No processes")
    return fcfs_scheduling(clean_processes(req.processes))

@app.post("/schedule/sjf")
def sjf(req: SchedulingRequest):
    if not req.processes: raise HTTPException(400, "No processes")
    return sjf_scheduling(clean_processes(req.processes))

@app.post("/schedule/srtf")
def srtf(req: SchedulingRequest):
    if not req.processes: raise HTTPException(400, "No processes")
    return srtf_scheduling(clean_processes(req.processes))

@app.post("/schedule/priority")
def priority(req: SchedulingRequest):
    if not req.processes: raise HTTPException(400, "No processes")
    return priority_scheduling(clean_processes(req.processes))

@app.post("/schedule/rr/{quantum}")
def rr(req: SchedulingRequest, quantum: int):
    if quantum <= 0: raise HTTPException(400, "Quantum > 0")
    if not req.processes: raise HTTPException(400, "No processes")
    return round_robin_scheduling(clean_processes(req.processes), quantum)

@app.post("/schedule/compare/{quantum}")
def compare(req: SchedulingRequest, quantum: int):
    if quantum <= 0: raise HTTPException(400, "Quantum > 0")
    if not req.processes: raise HTTPException(400, "No processes")
    return run_all_algorithms(clean_processes(req.processes), quantum)
##uvicorn main:app --reload
