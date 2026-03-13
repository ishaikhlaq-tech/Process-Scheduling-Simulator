import copy

from algorithms.fcfs import fcfs_scheduling
from algorithms.sjf import sjf_scheduling
from algorithms.srtf import srtf_scheduling
from algorithms.priority import priority_scheduling
from algorithms.round_robin import round_robin_scheduling
from services.comparator import compare_algorithms
from schemas.scheduling import ComparisonResponse


def run_all_algorithms(processes, quantum=2):
    results = []

    # DEEP COPY is MANDATORY
    results.append(fcfs_scheduling(copy.deepcopy(processes)))
    results.append(sjf_scheduling(copy.deepcopy(processes)))
    results.append(srtf_scheduling(copy.deepcopy(processes)))
    results.append(priority_scheduling(copy.deepcopy(processes)))
    results.append(round_robin_scheduling(copy.deepcopy(processes), quantum))

    comparison = compare_algorithms(results)

    # FIX: Return a standard dictionary instead of the Pydantic model 
    # to prevent your 'start' and 'end' keys from being stripped out!
    return {
        "results": results,
        "best_algorithm": comparison["best_algorithm"],
        "worst_algorithm": comparison["worst_algorithm"]
    }
