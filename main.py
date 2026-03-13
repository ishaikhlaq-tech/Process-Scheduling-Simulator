from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from schemas.scheduling import SchedulingRequest, SchedulingResponse, ComparisonResponse

# Import algorithms
from algorithms.fcfs import fcfs_scheduling
from algorithms.sjf import sjf_scheduling
from algorithms.srtf import srtf_scheduling
from algorithms.priority import priority_scheduling
from algorithms.round_robin import round_robin_scheduling
from services.simulator import run_all_algorithms

app = FastAPI(title="CPU Scheduling Simulator API")

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------
# Homepage Route (Fix for 404)
# ------------------------------
@app.get("/")
def home():
    return FileResponse("index.html")


# --- COMPATIBILITY FIX ---
# Safely convert Pydantic models to dicts (Works on V1 and V2)
def clean_processes(processes):
    cleaned = []
    for p in processes:
        if hasattr(p, "model_dump"):
            cleaned.append(p.model_dump())
        else:
            cleaned.append(p.dict())
    return cleaned


# ------------------------------
# Scheduling Algorithms Routes
# ------------------------------

@app.post("/schedule/fcfs")
def fcfs(req: SchedulingRequest):
    if not req.processes:
        raise HTTPException(status_code=400, detail="No processes")
    return fcfs_scheduling(clean_processes(req.processes))


@app.post("/schedule/sjf")
def sjf(req: SchedulingRequest):
    if not req.processes:
        raise HTTPException(status_code=400, detail="No processes")
    return sjf_scheduling(clean_processes(req.processes))


@app.post("/schedule/srtf")
def srtf(req: SchedulingRequest):
    if not req.processes:
        raise HTTPException(status_code=400, detail="No processes")
    return srtf_scheduling(clean_processes(req.processes))


@app.post("/schedule/priority")
def priority(req: SchedulingRequest):
    if not req.processes:
        raise HTTPException(status_code=400, detail="No processes")
    return priority_scheduling(clean_processes(req.processes))


@app.post("/schedule/rr/{quantum}")
def rr(req: SchedulingRequest, quantum: int):
    if quantum <= 0:
        raise HTTPException(status_code=400, detail="Quantum must be greater than 0")

    if not req.processes:
        raise HTTPException(status_code=400, detail="No processes")

    return round_robin_scheduling(clean_processes(req.processes), quantum)


@app.post("/schedule/compare/{quantum}")
def compare(req: SchedulingRequest, quantum: int):
    if quantum <= 0:
        raise HTTPException(status_code=400, detail="Quantum must be greater than 0")

    if not req.processes:
        raise HTTPException(status_code=400, detail="No processes")

    return run_all_algorithms(clean_processes(req.processes), quantum)