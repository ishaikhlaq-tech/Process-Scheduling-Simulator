from collections import deque
from utils.metrics import calculate_metrics

def round_robin_scheduling(processes, quantum):
    # 1. Sort by arrival time to ensure fair queueing
    processes.sort(key=lambda x: x["arrival_time"])
    
    n = len(processes)
    # Track remaining burst time for each process
    rem_burst = [p["burst_time"] for p in processes]
    
    current_time = 0
    completed = 0
    gantt_chart = []
    
    queue = deque()
    visited = [False] * n

    # 2. Handle Initial Arrival (Start time isn't always 0)
    if n > 0 and processes[0]["arrival_time"] > current_time:
        current_time = processes[0]["arrival_time"]

    # 3. Load initial processes into the queue
    for i in range(n):
        if processes[i]["arrival_time"] <= current_time and not visited[i]:
            queue.append(i)
            visited[i] = True

    # 4. Main Scheduling Loop
    while completed < n:
        # A. IDLE CPU HANDLING (If queue is empty but processes remain)
        if not queue:
            next_arrival = float('inf')
            # Find the next closest arrival time
            for i in range(n):
                if not visited[i]:
                    next_arrival = min(next_arrival, processes[i]["arrival_time"])
            
            if next_arrival == float('inf'): 
                break # Should not happen if completed < n
            
            # Jump time to next arrival
            current_time = next_arrival
            
            # Add the new guy to queue
            for i in range(n):
                if processes[i]["arrival_time"] <= current_time and not visited[i]:
                    queue.append(i)
                    visited[i] = True
            continue

        # B. PROCESS EXECUTION
        idx = queue.popleft()
        p = processes[idx]
        
        # Calculate how long to run (Quantum vs Remaining)
        execute_time = min(quantum, rem_burst[idx])
        
        start = current_time
        end = start + execute_time
        
        # Add to Gantt Chart
        gantt_chart.append({
            "pid": p["pid"],
            "start": start,
            "end": end
        })
        
        # Update State
        current_time = end
        rem_burst[idx] -= execute_time
        
        # C. CHECK FOR NEW ARRIVALS (Before re-queueing current)
        # Standard RR rule: New arrivals get in line before the current process returns
        for i in range(n):
            if not visited[i] and processes[i]["arrival_time"] <= current_time:
                queue.append(i)
                visited[i] = True
        
        # D. RE-QUEUE OR FINISH
        if rem_burst[idx] > 0:
            queue.append(idx)
        else:
            completed += 1
            # --- THIS WAS MISSING ---
            processes[idx]["completion_time"] = current_time 
            # ------------------------

    return calculate_metrics("Round Robin", gantt_chart, processes)