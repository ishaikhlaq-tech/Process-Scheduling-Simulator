from utils.metrics import calculate_metrics

def srtf_scheduling(processes):
    pool = []
    for i, p in enumerate(processes):
        pool.append({
            "original_idx": i,
            "pid": p["pid"],
            "arrival": p["arrival_time"],
            "burst": p["burst_time"],
            "remaining": p["burst_time"]
        })

    current_time = 0
    completed = 0
    n = len(pool)
    gantt_chart = []
    
    pool.sort(key=lambda x: x["arrival"])

    while completed < n:
        ready = [p for p in pool if p["arrival"] <= current_time and p["remaining"] > 0]
        
        if not ready:
            current_time += 1
            continue

        current_p = min(ready, key=lambda x: x["remaining"])
        
        # Add/Merge Gantt Block
        if gantt_chart and gantt_chart[-1]["pid"] == current_p["pid"] and gantt_chart[-1]["end"] == current_time:
            gantt_chart[-1]["end"] += 1
        else:
            gantt_chart.append({
                "pid": current_p["pid"],
                "start": current_time,
                "end": current_time + 1
            })

        current_p["remaining"] -= 1
        current_time += 1

        if current_p["remaining"] == 0:
            completed += 1
            # --- FIX: UPDATE ORIGINAL PROCESS ---
            processes[current_p["original_idx"]]["completion_time"] = current_time
            # ------------------------------------

    return calculate_metrics("SRTF", gantt_chart, processes)